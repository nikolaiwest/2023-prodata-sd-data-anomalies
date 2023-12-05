from abc import ABC, abstractmethod
from tqdm import tqdm
from typing import List, Union, Dict

from .screw_run import ScrewRun


class BaseLoader(ABC):
    """
    Abstract base class for data loading of screw runs and scenarios.

    Attributes:
    -----------
        all_runs : List[str]
            A list to store the file names of all screw runs under consideration.
    """

    def __init__(self) -> None:
        """
        Initializie the DataLoader.
        """
        # List of all ids of the screw runs (e.g. ["Ch_300...json", Ch_300...json", ...])
        self.all_run_ids: List[str] = []
        # List of all screw runs, loaded from as ScrewRun objects by their run id from raw data
        self.all_runs: List[ScrewRun] = []
        # Counter variables of OK and NOK labels in the data
        self.count_of_ok: int = 0
        self.count_of_nok: int = 0
        self.count_of_all: int = 0
        # Dicts to track the data matrix codes (DMC) in the data set
        self.counts_of_dmc: dict = {}  # Counts of individual DMCs
        self.labels_of_dmc: Dict[List] = {}  # Lists of their label ("OK" vs. "NOK")
        self.ids_of_dmc: Dict[
            List
        ] = {}  # List of their IDs (aka file names, e.g. "Ch_000...json")
        # Counter variables to track the number of runs and individual DMCs
        self.num_of_runs: int = 0
        self.num_of_dmcs: int = 0
        # Nested lists of time series values from all screw runs
        self.all_time_values: List[List[float]] = [[]]
        self.all_angle_values: List[List[float]] = [[]]
        self.all_torque_values: List[List[float]] = [[]]
        self.all_gradient_values: List[List[float]] = [[]]

    @abstractmethod
    def load_run_ids(self, source: Union[str, List[Union[str, int]]]) -> None:
        """
        Abstract method to load run ids from a specified source.

        Args:
            source (Union[str, List[Union[str, int]]]):
                The source from which to load data that can either be a path, a list
                of scenarios, a list of scenario numbers or a list of screw runs.
        """
        pass

    def load_and_update(self):
        self.load_runs_from_ids()
        self.update()

    def load_runs_from_ids(self):
        self.all_runs = [
            ScrewRun(name=run_id)
            for run_id in tqdm(self.all_run_ids, desc="Loading screw run data")
        ]

    def update(self) -> None:
        """
        Collection of methods to update all additional metrics of the screw run.
        """
        # Update the label counts
        self.update_label_counts()
        # Update the data matrix code dictionaries
        self.update_dmc_dics()
        # Update the number of runs
        self.update_num_of_runs()
        # Update the number of DMCs
        self.update_num_of_dmcs()
        # Update all lists of time series from screw runs
        self.update_series_values()

    def update_label_counts(self) -> None:
        for screw_run in self.all_runs:
            # Update the count of "OK" and "NOK" screw runs
            if screw_run.result == "OK":
                self.count_of_ok += 1
            elif screw_run.result == "NOK":
                self.count_of_nok += 1
            else:
                raise ValueError(
                    f"Unkown label {screw_run.result} in screw run {screw_run.name}"
                )
        self.count_of_all = self.count_of_ok + self.count_of_nok

    def update_dmc_dics(self) -> None:
        for screw_run in self.all_runs:
            # Update the dmc dictionaries for each screw run
            if screw_run.code not in self.counts_of_dmc.keys():
                self.counts_of_dmc[screw_run.code] = 1
                self.labels_of_dmc[screw_run.code] = [screw_run.result]
                self.ids_of_dmc[screw_run.code] = [screw_run.name]
            else:
                self.counts_of_dmc[screw_run.code] += 1
                self.labels_of_dmc[screw_run.code] += [screw_run.result]
                self.ids_of_dmc[screw_run.code] += [screw_run.name]

    def update_num_of_runs(self) -> None:
        """
        Check if the lists all_run_ids and all_runs have the same lengths and assigns it to a new attribute num_of_runs.
        """
        num_of_run_ids = len(self.all_run_ids)
        num_of_runs = len(self.all_runs)
        try:
            # Double check the lengths to avoid missing runs
            assert num_of_run_ids == num_of_runs
            self.num_of_runs = num_of_runs
        except AssertionError:
            raise AssertionError(
                f"The number of run ids {num_of_run_ids} does not match the number of runs {num_of_runs}"
            )

    def update_num_of_dmcs(self) -> None:
        """
        Check if the dicts counts_of_dmc and labels_of_dmc have the same lengths and assigns it to a new attribute num_of_dmcs.
        """
        num_of_dmcs = len(self.counts_of_dmc)
        num_of_dmcs_by_label = len(self.labels_of_dmc)
        try:
            # Double check the lengths to avoid missing runs
            assert num_of_dmcs == num_of_dmcs_by_label
            self.num_of_dmcs = num_of_dmcs
        except AssertionError:
            raise AssertionError(
                f"The number of dmc labels {num_of_dmcs_by_label} does not match the number of dmcs by count {num_of_dmcs}"
            )

    def update_series_values(self) -> None:
        """
        Update the series variables based on the corresponding ScrewRuns in all_runs.
        """
        # List of strings representing different series values
        series_values_as_str = [
            "time values",
            "angle values",
            "torque values",
            "gradient values",
        ]

        # List of lists containing the original series values
        series_values = [
            self.all_time_values,
            self.all_angle_values,
            self.all_torque_values,
            self.all_gradient_values,
        ]

        # Iterate through the series values and update them based on run values
        for i, val_as_str in enumerate(series_values_as_str):
            # Fetch run values for the current series and update the original list
            series_values[i][:] = [
                self.all_runs[j].get_run_values(val_as_str)
                for j in range(self.count_of_all)
            ]

    def get_run_ids(self) -> List[str]:
        """
        Get the loaded run ids.

        Returns:
            List[str]
                The loaded data
        """
        return self.all_run_ids

    def get_screw_runs(self) -> List[ScrewRun]:
        """
        Get the loaded runs.

        Returns:
            List[ScrewRun]
                The loaded data
        """
        return self.all_runs
