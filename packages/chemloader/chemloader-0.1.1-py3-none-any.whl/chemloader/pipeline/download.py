from tqdm import tqdm
import requests
import os
import zipfile
import shutil
import tarfile
from .setup import SetupPipelineStep, DataLoader, LOGGER


class DataDownloader(SetupPipelineStep):
    def __init__(self, src, raw_file_name=None):
        self.download_src = src

        self.raw_file_name = raw_file_name
        self.raw_file = None

    def setup(
        self,
        dataloader: DataLoader,
        previous_step=None,
        force: bool = False,
    ):
        """for DataDownloader, download the data from the source
        use tqdm to show the progress bar
        """
        if self.raw_file_name is None:
            self.raw_file_name = os.path.basename(self.download_src)
        self.raw_file = os.path.join(dataloader.datapath, self.raw_file_name)
        if os.path.exists(self.raw_file):
            if force:
                LOGGER.info("Forced download, removing existing file")
                os.remove(self.raw_file)
            else:
                LOGGER.info("Data already downloaded, skipping download")
                return

        LOGGER.info("Downloading data from %s", self.download_src)
        response = requests.get(self.download_src, stream=True)
        total_length = response.headers.get("content-length")
        if total_length:
            total_length_kb = int(int(total_length) / 1024) + 1
        else:
            total_length_kb = None

        with open(self.raw_file, "wb") as handle:
            for data in tqdm(
                response.iter_content(chunk_size=1024),
                total=total_length_kb,
                unit="KB",
                desc="Downloading",
            ):
                handle.write(data)


class UnzipFile(SetupPipelineStep):
    def __init__(self, zip_file=None, raw_file_name=None, keep_single_file=None):
        self.zip_file = zip_file
        self.raw_file_name = raw_file_name
        self.keep_single_file = keep_single_file

    def setup(self, dataloader: DataLoader, previous_step=None, force=False):
        if self.zip_file is None:
            self.zip_file = getattr(previous_step, "raw_file", None)
        if self.raw_file_name is None:
            self.raw_file_name = os.path.basename(self.zip_file).rsplit(".zip", 1)[0]

        self.raw_file = os.path.join(dataloader.datapath, self.raw_file_name)

        if os.path.exists(self.raw_file) and not os.path.isdir(self.raw_file):
            LOGGER.info("Data already unzipped, skipping unzip")
            return

        LOGGER.info("Unzipping file %s to %s", self.zip_file, self.raw_file)
        with zipfile.ZipFile(self.zip_file, "r") as zip_ref:
            zip_ref.extractall(self.raw_file)

        # if the zip file contains only one file, replace the unziiped folder with the file

        files = os.listdir(self.raw_file)
        if len(files) == 1:
            file = os.path.join(self.raw_file, files[0])
            shutil.move(file, self.raw_file + "__tmp")
            shutil.rmtree(self.raw_file)
            os.rename(self.raw_file + "__tmp", self.raw_file)
        if self.keep_single_file:
            shutil.move(
                os.path.join(self.raw_file, self.keep_single_file),
                self.raw_file + "__tmp",
            )
            shutil.rmtree(self.raw_file)
            os.rename(self.raw_file + "__tmp", self.raw_file)


class UnTarFile(SetupPipelineStep):
    def __init__(self, tar_file=None, raw_file_name=None, keep_single_file=None):
        self.tar_file = tar_file
        self.raw_file_name = raw_file_name
        self.keep_single_file = keep_single_file

    def setup(self, dataloader: DataLoader, previous_step=None, force=False):
        if self.tar_file is None:
            self.tar_file = getattr(previous_step, "raw_file", None)
        if self.raw_file_name is None:
            self.raw_file_name = os.path.basename(self.tar_file).rsplit(".tar", 1)[0]

        self.raw_file = os.path.join(dataloader.datapath, self.raw_file_name)

        if os.path.exists(self.raw_file):
            if os.path.isdir(self.raw_file):
                if force:
                    LOGGER.info("Forced untar, removing existing folder")
                    shutil.rmtree(self.raw_file)
                else:
                    LOGGER.info("Raw data already present as folder, counting entries")
                    if len(os.listdir(self.raw_file)) == dataloader.expected_data_size:
                        LOGGER.info("Data already untarred, skipping untar")
                        return
                    with tarfile.open(self.tar_file) as archive:
                        count = sum(1 for member in archive if member.isreg())
                    if count == len(os.listdir(self.raw_file)):
                        LOGGER.info("Data already untarred, skipping untar")
                        return
                    else:
                        LOGGER.info(
                            "Data already untarred, but missing files, untarring"
                        )
                        shutil.rmtree(self.raw_file)
            else:
                if force:
                    LOGGER.info("Forced untar, removing existing file")
                    os.remove(self.raw_file)
                else:
                    LOGGER.info("Data already untarred, skipping untar")
                    return

        LOGGER.info("Untarring file %s to %s", self.tar_file, self.raw_file)
        if not os.path.exists(self.raw_file):
            os.makedirs(self.raw_file)

        with tarfile.open(self.tar_file, "r") as tar_ref:
            # Get the list of members in the tar file
            members = tar_ref.getmembers()
            total_files = len(members)

            # Initialize tqdm progress bar
            with tqdm(total=total_files, desc="Extracting files", unit="file") as pbar:
                for member in members:
                    tar_ref.extract(member, path=self.raw_file)
                    pbar.update(1)

        files = os.listdir(self.raw_file)
        if len(files) == 1:
            file = os.path.join(self.raw_file, files[0])
            shutil.move(file, self.raw_file + "__tmp")
            shutil.rmtree(self.raw_file)
            os.rename(self.raw_file + "__tmp", self.raw_file)
        if self.keep_single_file:
            shutil.move(
                os.path.join(self.raw_file, self.keep_single_file),
                self.raw_file + "__tmp",
            )
            shutil.rmtree(self.raw_file)
            os.rename(self.raw_file + "__tmp", self.raw_file)
