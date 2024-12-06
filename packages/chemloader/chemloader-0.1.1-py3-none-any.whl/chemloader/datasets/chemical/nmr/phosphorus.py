from chemloader import MolDataLoader, DataDownloader, SDFToStorage


class Ilm_NMR_P31(MolDataLoader):
    expected_data_size = 14250
    citation = "https://doi.org/10.1186/s13321-023-00792-y"
    expected_mol = 13349

    setup_pipleline = [
        DataDownloader(
            src="https://zenodo.org/records/8260783/files/Ilm-NMR-P31.sdf?download=1",
            raw_file_name="Ilm_NMR_P31.sdf",
        ),
        SDFToStorage(),
    ]
