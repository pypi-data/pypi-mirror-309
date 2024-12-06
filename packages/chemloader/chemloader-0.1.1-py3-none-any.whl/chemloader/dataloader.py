from __future__ import annotations
from typing import (
    List,
    Any,
    Set,
    Literal,
    Iterator,
    Tuple,
    TYPE_CHECKING,
)
from abc import ABC
import os
from rdkit import Chem
import json
from statistics import mean, median
from .storage import MolPicklStorage, InMemoryStorage, BaseStorage
from .config import LOGGER, get_data_path, MISSMATCH_PREFIX


_ASKED_FOR_CITATION: Set[DataLoader] = set()

if TYPE_CHECKING:
    from .pipeline.setup import SetupPipelineStep


class DataLoader(ABC):
    expected_data_size: int = None
    citation: str = None
    _first_instance_created = False  # Class variable to track instance creation
    setup_pipleline: List[SetupPipelineStep] = []
    storage = InMemoryStorage

    def __init__(self, datapath=None, expected_data_size=None):
        if expected_data_size is not None:
            self.expected_data_size = expected_data_size

        if self.expected_data_size is None:
            raise ValueError(
                f"expected_data_size must be defined for {self.__class__.__name__}"
            )
        self.true_data_size: int = self.expected_data_size
        if self.citation is not None and self.__class__ not in _ASKED_FOR_CITATION:
            LOGGER.info(
                "You are using a citable datasource ('%s'), please consider citing '%s'!",
                self.__class__.__name__,
                self.citation,
            )
            _ASKED_FOR_CITATION.add(self.__class__)

        if datapath is None:
            datapath = get_data_path()
        self._datapath = os.path.join(datapath, self.__class__.__name__)
        if not os.path.exists(self._datapath):
            os.makedirs(self._datapath)

        self._storage_instance = None

    @property
    def storage_instance(self) -> BaseStorage:
        if self._storage_instance is None:
            self._storage_instance = self.storage(self)
        return self._storage_instance

    @property
    def datapath(self):
        return self._datapath

    def is_ready(self):
        if len(self.storage_instance) == 0:
            return False
        if len(self.storage_instance) != self.expected_data_size:
            LOGGER.warning(
                "DataLoader %s has %s/%s entries",
                self.__class__.__name__,
                len(self.storage_instance),
                self.expected_data_size,
            )
            return False

    def __iter__(self):
        if not self.is_ready():
            self.setup()

        return iter(self.storage_instance)

    def setup(self, force=False):
        prev_step = None
        for step in self.setup_pipleline:
            step.setup(self, previous_step=prev_step, force=force)
            prev_step = step

    def __len__(self):
        return self.expected_data_size


class MolDataLoader(DataLoader):
    expected_mol = None
    storage = MolPicklStorage

    def __init__(
        self,
        storage=None,
    ):
        super().__init__()
        if self.expected_mol is None:
            self.expected_mol = self.expected_data_size
        if storage is not None:
            self.storage = storage

    def is_ready(self):
        if len(self.storage_instance) == 0:
            return False
        if len(self.storage_instance) != self.expected_mol:
            LOGGER.warning(
                "DataLoader %s has %s/%s molecules",
                self.__class__.__name__,
                len(self.storage_instance),
                self.expected_mol,
            )
            return False
        return True

    def __len__(self):
        return self.expected_mol

    def iterate_with_property(
        self,
        prop: str,
        handle_missmatched: Literal["ignore", "mean", "median"] = "mean",
        return_list: bool = False,
    ) -> Iterator[Tuple[Chem.Mol, Any]]:
        for mol in self:
            propdict = mol.GetPropsAsDict()
            if prop in propdict:
                val = propdict[prop]
                if return_list:
                    yield mol, [val]
                else:
                    yield mol, val
            elif handle_missmatched == "ignore":
                continue
            elif MISSMATCH_PREFIX + prop in propdict:
                val = json.loads(propdict[MISSMATCH_PREFIX + prop])
                if return_list:
                    yield mol, val
                elif handle_missmatched == "mean":
                    yield mol, mean(val)
                elif handle_missmatched == "median":
                    yield mol, median(val)
                else:
                    raise ValueError(
                        f"Unknown value for handle_missmatched: {handle_missmatched}"
                    )


class AtomDataLoader(MolDataLoader):
    expected_mol = None
