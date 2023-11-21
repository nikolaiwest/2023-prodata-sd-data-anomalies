from typing import List, Union

from .data_from_path import DataFromPath
from .scenarios import Scenarios, InvalidScenarioError


class DataFromScenario(DataFromPath):
    """
    Class to load screw driving data by providing scenario numbers or names.

    Attributes:
    -----------
    scenarios : Scenarios
        Instance of the Scenarios class.
    """

    def __init__(
        self, scenarios_to_load: Union[str, int, List[Union[str, int]]]
    ) -> None:
        """
        Initialize DataFromScenario.

        Parameters:
        -----------
        scenarios_to_load : Union[str, int, List[Union[str, int]]]
            The scenario number or name, or a list of scenario numbers or names to load.

        Returns:
        --------
        None
        """

        # Instantiate the Scenarios class
        scenarios = Scenarios()

        # Convert single values to a list for uniform processing
        if not isinstance(scenarios_to_load, list):
            scenarios_to_load = [scenarios_to_load]

        try:
            # Check if all elements in the list are of the same type (int or str)
            if all(isinstance(scenario, int) for scenario in scenarios_to_load):
                paths = [
                    scenarios.get_path_by_number(scenario)
                    for scenario in scenarios_to_load
                ]
            elif all(isinstance(scenario, str) for scenario in scenarios_to_load):
                paths = [
                    scenarios.get_path_by_name(scenario)
                    for scenario in scenarios_to_load
                ]
            else:
                raise ValueError(
                    "Mixed types in scenarios_to_load. Must be all int or all str."
                )
        except InvalidScenarioError as e:
            raise e  # Raise the exception if an error occurs

        # Call the superclass constructor with the paths
        super().__init__(path=paths)
