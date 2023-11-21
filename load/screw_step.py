from typing import List, Dict, Union, Any


class ScrewStep:
    def __init__(self, step_dict: Dict[str, Any]) -> None:
        """
        Initialize a ScrewStep object.

        Parameters:
        -----------
        step_dict : dict
            Dictionary containing information about the screw step.

        Example:
        --------
        ```
        step_dict = {
            "name": "Finding",
            "graph": {"angle values": [1, 2, 3], "torque values": [4, 5, 6]},
            "step type": "standard",
            "row": 2,
            "column": "A",
            "last cmd": "TF Angle",
            "quality code": "1",
            "speed": 150,
            "category": 0,
            "docu buffer": 0,
            "result": "OK",
            "angle threshold": {"nom": 0, "act": 0.006},
            "tightening functions": [{"name": "TF Angle", "nom": 100, "act": 100.25}],
        }
        screw_step = ScrewStep(step_dict)
        ```

        """
        # Name of the step ["Finding", "Thread forming", "Pre-tightening", "Tightening 1.4"]
        self.name: str = str(step_dict["name"])
        # Values of the screw run, such as angle, torque gradient or time
        self.graph: List[Union[int, float]] = dict(step_dict["graph"])

        # For sake of documentation, the remaining attributes:
        if False:
            # Type of tightening step
            self.step_type = str(step_dict["step type"])  # "standard"
            # Row number
            self.row = int(step_dict["row"])
            # Column letter
            self.column = str(step_dict["column"])
            # Last command executed
            self.last_cmd = str(step_dict["last cmd"])
            # Quality code
            self.quality_code = str(step_dict["quality code"])  # "1"
            # Tightening speed
            self.speed = int(step_dict["speed"])
            # Category of the step
            self.category = int(step_dict["category"])  # "0"
            # Documentation buffer
            self.docu_buffer = int(step_dict["docu buffer"])  # "0"
            # Result of the tightening step
            self.result = str(step_dict["result"])
            # Angle threshold information
            self.angle_threshold = dict(step_dict["angle threshold"])
            # List with dicts of tightening functions
            self.tightening_functions = list(step_dict["tightening functions"])

    def get_graph_values(self, value_type: str) -> List[Union[int, float]]:
        """
        Get values from the graph based on the specified value type.

        Parameters:
        -----------
        value_type : str
            Type of values to retrieve from the graph.

        Returns:
        --------
        List[Union[int, float]]
            List of values from the specified graph.

        Example:
        --------
        ```
        angle_values = screw_step.get_graph_values("angle values")
        ```

        """
        return self.graph[value_type]
