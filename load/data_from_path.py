import os

from typing import List, Union

from .base_loader import BaseLoader


class DataFromPath(BaseLoader):
    """
    Class to load screw driving data by providing a path to a folder of screw runs.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize DataLoaderFromPath.

        Parameters:
        -----------
        path : str or List[str]
            The path or list of paths from which to load data.

        Returns:
        --------
        None
        """
        super().__init__()
        # Load a list of run ids from the provided path or paths
        self.load_run_ids(path=path)
        # Load screw runs and update loader
        self.load_and_update()

    def load_run_ids(self, path: Union[str, List[str]]) -> None:
        """
        Load screw runs from a specified path or list of paths.

        Parameters:
        -----------
        path : str or List[str]
            The path or list of paths from which to load the runs.

        Returns:
        --------
        None
        """
        # Check if path is a single string or a list of strings
        if isinstance(path, str):
            paths = [path]
        elif isinstance(path, list):
            paths = path
        else:
            raise ValueError(
                "Invalid input type for 'path'. It should be a string or a list of strings."
            )

        # all_run_ids the list to store all runs
        self.all_runs = []

        # Iterate through each path
        for current_path in paths:
            # Check if the current path is valid
            if not os.path.isdir(current_path):
                raise InvalidPathError(
                    f"The specified path '{current_path}' is not a directory."
                )

            # Get all json files from the current path and append to the list
            current_runs = [f for f in os.listdir(current_path) if f.endswith(".json")]
            self.all_run_ids.extend(current_runs)


class InvalidPathError(Exception):
    """
    Exception raised for invalid paths in PathLoader.

    Attributes:
    ----------
    message : str
        Explanation of the error.
    """
