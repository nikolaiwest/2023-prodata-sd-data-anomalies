from abc import ABC, abstractmethod
from typing import List, Union

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
        self.all_run_ids: List[str] = []
        self.all_runs: List[ScrewRun] = []

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

    def load_runs(self):
        self.all_runs = [ScrewRun(name=run_id) for run_id in self.all_run_ids]

    def get_run_ids(self) -> List[str]:
        """
        Get the loaded run ids.

        Returns:
            List[str]
                The loaded data
        """
        return self.all_run_ids

    def get_screw_runs(self) -> None:
        """
        Get the loaded runs.

        Returns:
            List[ScrewRun]
                The loaded data
        """
        return self.all_runs
