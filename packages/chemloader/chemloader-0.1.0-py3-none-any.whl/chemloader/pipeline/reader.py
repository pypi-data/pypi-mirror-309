import pandas as pd
from typing import Optional, List, Dict, Union, Literal
from rdkit.Chem import (
    MolFromSmiles,
    SetDefaultPickleProperties,
    PropertyPickleOptions,
    GetDefaultPickleProperties,
    ForwardSDMolSupplier,
    MolToSmiles,
    Mol,
    MolToInchiKey,
    RemoveHs,
)
import hashlib
import json
from tqdm import tqdm
import string
from .setup import SetupPipelineStep, DataLoader, LOGGER
from ..config import MISSMATCH_PREFIX


def check_mol_properties(mol, key, storage_instance, index):
    try:
        oldmol = storage_instance.get(key)
    except KeyError:
        return mol

    if oldmol is None:
        return mol

    oldmolprops = oldmol.GetPropsAsDict()
    molprops = mol.GetPropsAsDict()

    # Check if SMILES match
    if MolToSmiles(oldmol) != MolToSmiles(mol):
        raise ValueError(
            f"SMILES mismatch for {key}: {MolToSmiles(RemoveHs(oldmol))} != {MolToSmiles(RemoveHs(mol))}"
        )

    for k in oldmolprops:
        # Check if property is in molprops and marked as missmatched
        missmatch_key = MISSMATCH_PREFIX + k
        if missmatch_key in oldmolprops and k in molprops:
            # Add new value to missmatched list if not already there
            old_missmatched = json.loads(oldmolprops[missmatch_key])
            old_missmatched[index] = molprops[k]
            old_missmatched.append(molprops[k])

            # Set new missmatched list and remove property from mol
            mol.SetProp(
                missmatch_key,
                json.dumps(old_missmatched),
            )
            mol.ClearProp(k)

        # Check if property is in molprops and missmatches
        elif k in molprops and oldmolprops[k] != molprops[k]:
            LOGGER.warning(
                "Missmatched properties for %s: %s from %s to %s",
                key,
                k,
                oldmolprops[k],
                molprops[k],
            )
            # set new missmatched list and remove property from mol
            mol.SetProp(
                missmatch_key,
                json.dumps([molprops[k], oldmolprops[k]]),
            )
            # oldmol.ClearProp(k) # Remove property from oldmol not needed since it will be overwritten
            mol.ClearProp(k)  # Remove property from mol

        # the property is not in the molprops, or it matches
        else:
            if isinstance(oldmolprops[k], str):
                mol.SetProp(k, oldmolprops[k])
            elif isinstance(oldmolprops[k], int):
                mol.SetIntProp(k, oldmolprops[k])
            elif isinstance(oldmolprops[k], float):
                mol.SetDoubleProp(k, oldmolprops[k])
            elif isinstance(oldmolprops[k], bool):
                mol.SetBoolProp(k, oldmolprops[k])
            else:
                raise ValueError(
                    f"Unknown property type for {k}: {type(oldmolprops[k])}"
                )
        return mol


def fixed_length_hash(input_string: str, length: int) -> str:
    """
    Hash an arbitrary string to a fixed-length hashed version using alphanumeric characters.

    Args:
        input_string (str): The input string to hash.
        length (int): The desired length of the hash.

    Returns:
        str: The fixed-length hashed string.
    """
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    # Alphanumeric characters to use in the hash
    chars = string.ascii_letters + string.digits
    char_count = len(chars)

    # Hash the input string using SHA-256
    sha256_hash = hashlib.sha256(input_string.encode("utf-8")).hexdigest()

    # Convert the hash into a number
    hash_as_int = int(sha256_hash, 16)

    # Generate a fixed-length hash using the alphanumeric characters
    hashed_string = []
    for _ in range(length):
        hashed_string.append(chars[hash_as_int % char_count])
        hash_as_int //= char_count

    return "".join(hashed_string)


class MolToStoragePipeline(SetupPipelineStep):
    def __init__(
        self,
        key_prop=None,
        leading_zeros=None,
        mol_property_checks=None,
        fallback: Literal[
            "index", "smiles", "inchikey", "smileshash32"
        ] = "smileshash32",
    ):
        if mol_property_checks is None:
            mol_property_checks = [check_mol_properties]
        self.mol_property_checks = mol_property_checks
        self.key_prop = key_prop
        self.leading_zeros_crushed = False
        self.leading_zeros = leading_zeros
        if fallback not in ["index", "smiles", "inchikey", "smileshash32"]:
            raise ValueError(
                f"Invalid fallback: {fallback}, must be index, smiles, smileshash32 or inchikey"
            )
        self.fallback = fallback

    def presetup(self, dataloader: DataLoader):
        self.leading_zeros_crushed = False
        if self.leading_zeros is None:
            self.leading_zeros = len(str(dataloader.expected_data_size)) + 1

        # store current pickle properties
        self.default_pickle_props = GetDefaultPickleProperties()

        # set all properties to be pickled
        SetDefaultPickleProperties(PropertyPickleOptions.AllProps)

        # clear storage
        dataloader.storage_instance.clear()

    def postsetup(self):
        # restore pickle properties
        SetDefaultPickleProperties(self.default_pickle_props)

    def setupstep(
        self, dataloader: DataLoader, mol: Mol, key: str = None, index: int = None
    ):
        if key is None:
            key = self.get_key(mol, index=index)
        for check in self.mol_property_checks:
            mol = check(mol, key, dataloader.storage_instance, index=index)

        dataloader.storage_instance.set(key, mol)
        return mol

    def get_key(self, mol, index: int):
        if self.key_prop is not None:
            new_key = mol.GetProp(self.key_prop)
        elif self.fallback == "index":
            new_key = index
        elif self.fallback == "smiles":
            new_key = MolToSmiles(mol)
        elif self.fallback == "smileshash32":
            new_key = fixed_length_hash(MolToSmiles(mol), 32)
        elif self.fallback == "inchikey":
            new_key = MolToInchiKey(mol)
        else:
            raise ValueError(f"Invalid fallback: {self.fallback}")

        try:
            new_key = str(int(new_key)).zfill(self.leading_zeros)
            if len(new_key) > self.leading_zeros and not self.leading_zeros_crushed:
                self.leading_zeros_crushed = True
                LOGGER.warning(
                    "Leading zeros crushed, consider using an index prop or increasing leading_zeros"
                )
        except Exception:
            pass

        return new_key


class _PandasSmilesToStorage(MolToStoragePipeline):
    def __init__(
        self,
        smiles="smiles",
        file=None,
        reader_kwargs=None,
        float_props: Union[List[str], Dict[str, str], None] = None,
        int_props: Union[List[str], Dict[str, str], None] = None,
        str_props: Union[List[str], Dict[str, str], None] = None,
        bool_props: Union[List[str], Dict[str, str], None] = None,
        store_others=True,
        **kwargs,
    ):
        self.file = file
        self.reader_kwargs = reader_kwargs or {}
        self.smiles = smiles
        self.store_others = store_others

        float_props = float_props or []
        if isinstance(float_props, list):
            float_props = {prop: prop for prop in float_props}
        self.float_props = float_props

        int_props = int_props or []
        if isinstance(int_props, list):
            int_props = {prop: prop for prop in int_props}
        self.int_props = int_props

        str_props = str_props or []
        if isinstance(str_props, list):
            str_props = {prop: prop for prop in str_props}
        self.str_props = str_props

        bool_props = bool_props or []
        if isinstance(bool_props, list):
            bool_props = {prop: prop for prop in bool_props}
        self.bool_props = bool_props

        super().__init__(**kwargs)

    def setup(
        self,
        dataloader: DataLoader,
        previous_step: Optional[SetupPipelineStep] = None,
        force: bool = False,
    ) -> None:
        self.presetup(dataloader)

        if self.file is None:
            self.file = getattr(previous_step, "raw_file", None)

        if self.file is None:
            raise ValueError("No excel file provided")

        LOGGER.info("Reading excel file %s", self.file)

        self.df = self.readfile()

        other_props = set(self.df.columns) - set(
            [
                self.smiles,
                *self.float_props.keys(),
                *self.int_props.keys(),
                *self.str_props.keys(),
                *self.bool_props.keys(),
            ]
        )
        # estimate other types
        if self.store_others:
            for prop in other_props:
                if self.df[prop].dtype == "float64":
                    self.float_props[prop] = prop
                elif self.df[prop].dtype == "int64":
                    self.int_props[prop] = prop
                elif self.df[prop].dtype == "bool":
                    self.bool_props[prop] = prop
                else:
                    print(f"Unknown type for {prop}: {self.df[prop].dtype}")
                    self.str_props[prop] = prop
        try:
            for index, row in tqdm(
                self.df.iterrows(), total=len(self.df), desc="Storing SMILES"
            ):
                mol = MolFromSmiles(row[self.smiles])

                if mol is None:
                    LOGGER.warning("Invalid SMILES %s", row[self.smiles])
                    continue

                try:
                    for prop, prop_name in self.float_props.items():
                        mol.SetDoubleProp(prop_name, float(row[prop]))
                except Exception as exc:
                    LOGGER.warning(
                        "Error setting float prop '%s' with value '%s': '%s'",
                        prop,
                        row[prop],
                        exc,
                    )
                    raise
                try:
                    for prop, prop_name in self.int_props.items():
                        mol.SetIntProp(prop_name, int(row[prop]))
                except Exception as exc:
                    LOGGER.warning(
                        "Error setting int prop '%s' with value '%s': '%s'",
                        prop,
                        row[prop],
                        exc,
                    )
                    raise

                try:
                    for prop, prop_name in self.str_props.items():
                        mol.SetProp(prop_name, str(row[prop]))
                except Exception as exc:
                    LOGGER.warning(
                        "Error setting str prop '%s' with value '%s': '%s'",
                        prop,
                        row[prop],
                        exc,
                    )
                    raise

                try:
                    for prop, prop_name in self.bool_props.items():
                        mol.SetBoolProp(prop_name, bool(row[prop]))
                except Exception as exc:
                    LOGGER.warning(
                        "Error setting bool prop '%s' with value '%s': '%s'",
                        prop,
                        row[prop],
                        exc,
                    )
                    raise
                self.setupstep(dataloader, mol, index=index)
        finally:
            self.postsetup()

    def readfile(self):
        raise NotImplementedError


class SmilesExcelToStorage(_PandasSmilesToStorage):
    def readfile(self):
        return pd.read_excel(self.file, **self.reader_kwargs)


class SmilesCsvToStorage(_PandasSmilesToStorage):
    def readfile(self):
        return pd.read_csv(self.file, **self.reader_kwargs)


class SmilesJSONToStorage(_PandasSmilesToStorage):
    def readfile(self):
        return pd.read_json(self.file, **self.reader_kwargs)


class SDFToStorage(MolToStoragePipeline):
    def __init__(
        self,
        sdf_file=None,
        **kwargs,
    ):
        self.sdf_file = sdf_file

        super().__init__(**kwargs)

    def setup(
        self,
        dataloader: DataLoader,
        previous_step: Optional[SetupPipelineStep] = None,
        force: bool = False,
    ) -> None:
        self.presetup(dataloader)
        if self.sdf_file is None:
            self.sdf_file = getattr(previous_step, "raw_file", None)

        if self.sdf_file is None:
            raise ValueError("No SDF file provided")

        LOGGER.info("Reading SDF file %s", self.sdf_file)

        # mols might  be pickled, and we need to preserve the properties

        try:
            for i, mol in tqdm(
                enumerate(ForwardSDMolSupplier(self.sdf_file, removeHs=False)),
                desc="Storing SDF",
                total=dataloader.expected_data_size,
            ):
                if mol is None:
                    LOGGER.warning("Invalid mol at index %d", i)
                    continue

                self.setupstep(dataloader, mol, index=i)

        finally:
            self.postsetup()
