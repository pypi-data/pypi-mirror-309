from chemloader import (
    MolDataLoader,
    SmilesCsvToStorage,
    datasets,
)
import os


class ESOL(MolDataLoader):
    raw_file = "delaney_data.sdf"
    expected_data_size = 1144
    expected_mol = 1117
    citation = "https://doi.org/10.1021/ci034243x"
    setup_pipleline = [
        SmilesCsvToStorage(
            file=os.path.join(
                datasets.__path__[0],
                "_local",
                "ci034243xsi20040112_053635.txt",
            ),
            smiles="SMILES",
            float_props={
                "measured log(solubility:mol/L)": "measured_log_solubility",
                "ESOL predicted log(solubility:mol/L)": "ESOL_predicted_log_solubility",
            },
            str_props=["Compound ID"],
        ),
    ]
