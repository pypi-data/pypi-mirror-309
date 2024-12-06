from chemloader import MolDataLoader, DataDownloader, SmilesExcelToStorage


class BradleyDoublePlusGoodMP(MolDataLoader):
    expected_data_size = 3042
    expected_mol = 3022
    citation = "http://dx.doi.org/10.6084/m9.figshare.1031637"

    setup_pipleline = [
        DataDownloader(
            src="https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/"
            "1503991/BradleyDoublePlusGoodMeltingPointDataset.xlsx",
        ),
        SmilesExcelToStorage(
            smiles="smiles",
            float_props=["mpC", "min", "max", "range"],
            int_props=["key", "csid", "count"],
            str_props={
                "name": "_Name",
                "link": "link",
                "source": "source",
            },
        ),
    ]
