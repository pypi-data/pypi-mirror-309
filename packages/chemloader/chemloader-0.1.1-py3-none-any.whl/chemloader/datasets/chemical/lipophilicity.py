from chemloader import (
    MolDataLoader,
    SmilesCsvToStorage,
    datasets,
)
import os


class Lipo1(MolDataLoader):
    expected_data_size = 4200
    citation = "https://doi.org/10.6019/CHEMBL3301361"

    setup_pipleline = [
        SmilesCsvToStorage(
            file=os.path.join(
                datasets.__path__[0],
                "_local",
                "Lipophilicity.csv",
            ),
            smiles="smiles",
            float_props=["exp"],
            str_props=["CMPD_CHEMBLID"],
        ),
    ]
