from chemloader import MolDataLoader, DataDownloader, SmilesExcelToStorage


class LogPNadinUlrich(MolDataLoader):
    expected_data_size = 12709
    expected_mol = 12709
    citation = "https://doi.org/10.1038/s42004-021-00528-9"

    setup_pipleline = [
        DataDownloader(
            src="https://github.com/nadinulrich/log_P_prediction/raw/main/Dataset_and_Predictions.xlsx",
        ),
        SmilesExcelToStorage(
            smiles="SMILES",
            float_props={
                "logP\nexperimental\n(corrected)": "logP_exp",
            },
            int_props=["ChemID"],
            str_props=["CAS"],
        ),
    ]
