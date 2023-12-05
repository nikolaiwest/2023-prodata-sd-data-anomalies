import os
from typing import List, Union

from .screw_run import ScrewRun
from .base_loader import BaseLoader

from tqdm import tqdm


class DataFromDmc(BaseLoader):
    """
    Load data by providing a list of DMCs.
    """

    def __init__(self, dmcs_to_load) -> None:
        super().__init__()
        # Load a list of run ids that contain the provided DMCs
        self.load_run_ids(dmcs_to_load)
        # Load screw runs and update loader
        self.load_and_update()

    def load_run_ids(self, dmcs_to_load) -> None:
        self.dmcs_to_load = dmcs_to_load
        ids = []

        path_to_raw_data: str = "data/00_raw-data/"

        # Iterate files and check for dmc name in files
        for file_name in tqdm(
            os.listdir(path_to_raw_data),
            desc="Loading file names by DMCs",
        ):
            current_run = ScrewRun(name=file_name)
            current_dmc = current_run.get_dmc()

            if current_dmc in self.dmcs_to_load:
                # Add to list of ids
                ids.append(file_name)
                # Remove from list of dmcs
                # self.dmcs_to_load.pop(current_dmc)

        # Update all_run_ids
        self.all_run_ids = ids

        print(f"DMCs: {self.dmcs_to_load}")
        print(f"IDs: {ids}")
