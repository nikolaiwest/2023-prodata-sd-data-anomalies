class PathNames:
    def __init__(self):
        # Scenario 1: Repeated screw runs with 25 repetitions each
        self.path_01_01 = "data/01_repeated-runs-x25/01_base-line"
        self.path_01_02 = "data/01_repeated-runs-x25/02_with-drilling"
        self.scenario_01 = [
            self.path_01_01,
            self.path_01_02,
        ]

        # Scenario 2: Manipulation of the surface friction with 25 repetitions each
        self.path_02_01 = "data/02_surface-friction-x25/01_base-line"
        self.path_02_02 = "data/02_surface-friction-x25/02_up-to-fifty"
        self.path_02_03 = "data/02_surface-friction-x25/03_with-lubricant"
        self.path_02_04 = "data/02_surface-friction-x25/04_sand-paper-40"
        self.path_02_05 = "data/02_surface-friction-x25/05_sand-paper-400"
        self.scenario_02 = [
            self.path_02_01,
            self.path_02_02,
            self.path_02_03,
            self.path_02_04,
            self.path_02_05,
        ]
