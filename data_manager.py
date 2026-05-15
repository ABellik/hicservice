from pathlib import Path
from fastapi import HTTPException

from cooler_file import CoolFile


class DataManager:
    data_dir = ""
    datasets: dict[str, CoolFile] = dict()

    def __init__(self, settings):
        self.data_dir = settings.data_dir
        self.fetch_datasets()

    def fetch_datasets(self):
        for file in Path(self.data_dir).iterdir():
            filename = file.name
            if filename.endswith(".cool") or filename.endswith(".mcool"):
                dataset = CoolFile(file)
                self.datasets[dataset.get_identifier()] = dataset

    def get_dataset_ids(self):
        return list(self.datasets.keys())

    def get_dataset(self, identifier):
        return self.datasets[identifier]

    def get_dataset_info(self, identifier):
        dataset = self.datasets[identifier]
        if dataset is None:
            raise HTTPException(status_code=404, detail=f"Dataset with identifier {identifier} not found.")
        return dataset.get_info()