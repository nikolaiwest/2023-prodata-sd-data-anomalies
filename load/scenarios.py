from typing import List


class InvalidScenarioError(Exception):
    """
    Exception raised for invalid scenarios in Scenarios.

    Attributes:
    ----------
    message : str
        Explanation of the error.
    """


class Scenarios:
    """
    Class containing information about available scenarios and methods to retrieve paths.

    Attributes:
    -----------
    numbers : List[int]
        List of scenario numbers.
    names : List[str]
        List of scenario names.
    paths : List[str]
        List of scenario paths.
    """

    def __init__(self) -> None:
        """
        Initialize Scenarios.

        Returns:
        --------
        None
        """
        self.numbers: List[int] = [
            1,
            2,
        ]

        self.names: List[str] = [
            "Wiederholte Verschraubungen x25",
            "Wiederholte Verschraubungen x25 mit Aufbohrung",
        ]

        self.paths: List[str] = [
            "data/01_repeated-screw-runs-x25",
            "data/02_repeated-screw-runs-x25-with-drilling",
        ]

    def get_path_by_number(self, number: int) -> str:
        """
        Get the scenario path based on the scenario number.

        Parameters:
        -----------
        number : int
            The scenario number.

        Returns:
        --------
        str
            The scenario path.

        Raises:
        -------
        InvalidScenarioError
            If the provided number is not in the list of all numbers.
        """
        if number not in self.numbers:
            raise InvalidScenarioError(
                f"The selected number {number} is not in the list of all numbers."
            )
        try:
            return self.paths[self.numbers.index(number)]
        except ValueError:
            raise InvalidScenarioError(
                f"The index of {number} is not in the list of all paths."
            )

    def get_path_by_name(self, name: str) -> str:
        """
        Get the scenario path based on the scenario name.

        Parameters:
        -----------
        name : str
            The scenario name.

        Returns:
        --------
        str
            The scenario path.

        Raises:
        -------
        InvalidScenarioError
            If the provided name is not in the list of all names.
        """
        if name not in self.names:
            raise InvalidScenarioError(
                f"The selected name {name} is not in the list of all names."
            )
        try:
            return self.paths[self.names.index(name)]
        except ValueError:
            raise InvalidScenarioError(
                f"The index of {name} is not in the list of all paths."
            )
