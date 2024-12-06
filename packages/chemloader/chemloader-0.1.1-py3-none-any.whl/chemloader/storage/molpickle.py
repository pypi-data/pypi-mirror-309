import os
import pickle
import shutil
from rdkit.Chem import Mol
from .base import BaseStorage


class MolPicklStorage(BaseStorage[Mol]):
    def __init__(self, dataloader):
        self.storage_dir = os.path.join(dataloader.datapath, "molpickle")
        super().__init__(dataloader=dataloader)
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def file_path(self, key: str):
        return os.path.join(self.storage_dir, key)

    def file_to_key(self, file: str):
        return os.path.basename(file)

    def set(self, key: str, value):
        with open(self.file_path(key), "wb+") as f:
            pickle.dump(value, f)

    def get(self, key: str):
        file = self.file_path(key)
        if not os.path.exists(file):
            raise KeyError(f"Key {key} not found in storage")
        with open(file, "rb") as f:
            return pickle.load(f)

    def delete(self, key: str):
        if os.path.exists(os.path.join(self.storage_dir, key)):
            os.remove(os.path.join(self.storage_dir, key))

    def clear(self):
        if os.path.exists(self.storage_dir):
            shutil.rmtree(self.storage_dir)
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def keys(self):
        for file in os.listdir(self.storage_dir):
            yield self.file_to_key(file)

    def values(self):
        for key in self.keys():
            yield self.get(key)

    def __contains__(self, key: str):
        return os.path.exists(self.file_path(key))

    def __len__(self):
        return len(os.listdir(self.storage_dir))
