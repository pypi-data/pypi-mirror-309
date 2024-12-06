from chemloader import MolDataLoader, DataDownloader, SDFToStorage, UnzipFile


class Tox21Base(MolDataLoader):
    pass


class Tox21Train(Tox21Base):
    expected_data_size = 11764
    expected_mol = 8039
    mol_properties = {
        "DSSTox_CID": 8039,
        "FW": 8039,
        "Formula": 8039,
        "NR-AR": 7416,
        "NR-AR-LBD": 6906,
        "NR-AhR": 6669,
        "NR-Aromatase": 5938,
        "NR-ER": 6202,
        "NR-ER-LBD": 7083,
        "NR-PPAR-gamma": 6589,
        "SR-ARE": 5909,
        "SR-ATAD5": 7228,
        "SR-HSE": 6573,
        "SR-MMP": 5906,
        "SR-p53": 6907,
        "missmatched_NR-AR": 49,
        "missmatched_NR-AR-LBD": 18,
        "missmatched_NR-AhR": 44,
        "missmatched_NR-Aromatase": 26,
        "missmatched_NR-ER": 137,
        "missmatched_NR-ER-LBD": 54,
        "missmatched_NR-PPAR-gamma": 14,
        "missmatched_SR-ARE": 50,
        "missmatched_SR-ATAD5": 24,
        "missmatched_SR-HSE": 42,
        "missmatched_SR-MMP": 35,
        "missmatched_SR-p53": 20,
    }
    setup_pipleline = [
        DataDownloader(
            src="https://tripod.nih.gov/tox21/challenge/download?id=tox21_10k_data_allsdf",
            raw_file_name="tox21_10k_data_all.sdf.zip",
        ),
        UnzipFile(),
        SDFToStorage(
            key_prop="DSSTox_CID",
        ),
    ]


Tox21 = Tox21Train
