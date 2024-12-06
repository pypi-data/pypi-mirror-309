from chemloader import (
    MolDataLoader,
    DataDownloader,
    SmilesCsvToStorage,
    UnzipFile,
)


class IUPAC_DissociationConstantsV1_0(MolDataLoader):
    expected_data_size = 21147
    expected_mol = 21147
    citation = "https://doi.org/10.5281/zenodo.7236453"

    setup_pipleline = [
        DataDownloader(
            src="https://zenodo.org/records/7236453/files/IUPAC/"
            "Dissociation-Constants-v1-0_initial-release.zip?download=1",
            raw_file_name="Dissociation-Constants-v1-0_initial-release.zip",
        ),
        UnzipFile(
            keep_single_file="iupac_high-confidence_v1_0.csv",
            raw_file_name="IUPAC_DissociationConstantsV1_0.csv",
        ),
        SmilesCsvToStorage(smiles="SMILES", fallback="index"),
    ]


class HybridpKaDatasetforAcidMolecules(MolDataLoader):
    expected_data_size = 13460
    expected_mol = 13411
    citation = "https://doi.org/10.5281/zenodo.10551522"

    setup_pipleline = [
        DataDownloader(
            src="https://zenodo.org/records/10551522/files/Dataset%20V1.csv?download=1",
            raw_file_name="Dataset_V1.csv",
        ),
        SmilesCsvToStorage(
            smiles="SMILES",
            reader_kwargs={"encoding": "ISO-8859-1", "sep": ";"},
            fallback="index",
        ),
    ]
