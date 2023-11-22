from abc import ABC, abstractmethod
from typing import List, Union, Dict

from .screw_run import ScrewRun

from tqdm import tqdm
import matplotlib.pyplot as plt


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
        # Dicts to track the data matrix codes (DMC) in the data set
        self.counts_of_dmc: dict = {}  # Counts of individual DMCs
        self.labels_of_dmc: Dict[List] = {}  # Lists of their label ("OK" vs. "NOK")
        # Counter variables to track the number of runs and individual DMCs
        self.num_of_runs: int = 0
        self.num_of_dmcs: int = 0

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
        self.all_runs = [
            ScrewRun(name=run_id)
            for run_id in tqdm(self.all_run_ids, desc="Loading screw run data")
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

    def update_dmc_dics(self) -> None:
        for screw_run in self.all_runs:
            # Update the dmc dictionaries for each screw run
            if screw_run.code not in self.counts_of_dmc.keys():
                self.counts_of_dmc[screw_run.code] = 1
                self.labels_of_dmc[screw_run.code] = [screw_run.result]
            else:
                self.counts_of_dmc[screw_run.code] += 1
                self.labels_of_dmc[screw_run.code] += [screw_run.result]

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

    def plot_dmc_counts(self) -> None:
        # Get values to plot from the dict counts_of_dmc
        x_values = list(self.counts_of_dmc.keys())
        y_values = list(self.counts_of_dmc.values())
        # Use matplotlib to plot and show the plot
        plt.bar(x=x_values, height=y_values)
        plt.xlabel("Data Matrix Code (DMC) of the workpieces")
        plt.ylabel("Number of occurence")
        plt.xticks(rotation=45, ha="right")
        plt.title("Number of screw runs for each workpiece by DMC")
        plt.show()

    def plot_dmc_label_ratio(self):
        # TODO: Check if all lists are of same length
        # ...

        # Get the max length; e.g. 50 for scenario 1 and 2 -> has to be even
        max_length = max([len(label) for label in self.labels_of_dmc.values()])

        # Calculate the ratio of 'OK' and 'NOK' for each index across the lists
        ratios_OK = []
        ratios_NOK = []

        # Since every workpiece holds two screws, we have to look at the even
        # and the odd indices of, thus cutting in half the number of x values.
        for i in range(0, max_length, 2):  # "0", "2", "4", ... "24"
            # Get the number of OK results for one workpiece (two screw runs)
            ok_count = sum(
                self.labels_of_dmc[key][i] == "OK" for key in self.labels_of_dmc
            ) + sum(
                self.labels_of_dmc[key][i + 1] == "OK" for key in self.labels_of_dmc
            )

            # Get the number of NOK results for one workpiece (again, two screw runs)
            nok_count = sum(
                self.labels_of_dmc[key][i] == "NOK" for key in self.labels_of_dmc
            ) + sum(
                self.labels_of_dmc[key][i + 1] == "NOK" for key in self.labels_of_dmc
            )
            # Get ratio of OK results for the current workpiece
            total_count = ok_count + nok_count
            ratio_OK = ok_count / total_count if total_count != 0 else 0
            ratio_NOK = nok_count / total_count if total_count != 0 else 0
            # Finally, append the current ratios to the result lists
            ratios_OK.append(ratio_OK)
            ratios_NOK.append(ratio_NOK)

        # Get x values to plot from the dict labels_of_dmc
        x_values = range(int(max_length / 2))  # "50"

        # Use matplotlib to plot and show the plot
        plt.bar(
            x=x_values,
            height=ratios_OK,
            label="OK",
            color="forestgreen",
        )
        plt.bar(
            x=x_values,
            height=ratios_NOK,
            label="NOK",
            bottom=ratios_OK,
            color="firebrick",
        )
        plt.xlabel("Number of screw cycles per workpiece")
        plt.ylabel("Ratio of OK and NOK observations")
        plt.title("Ratio of OK and NOK runs with regard to the cycle number")
        plt.show()

    def plot_dmc_label_heatmap(self):
        # Sample data for heatmaps
        labels_even = []
        labels_odd = []

        # Get the length of the workpiece with the most screw runs (and thus most labels)
        max_length = max([len(label) for label in self.labels_of_dmc.values()])

        # Iterate all entries of the label dict by index
        for i in range(max_length):
            label_even = []
            label_odd = []
            for list_of_labels in self.labels_of_dmc.values():
                if i % 2 == 0:  # is even
                    label_even.append(1 if list_of_labels[i] == "OK" else -1)
                else:  # is odd
                    label_odd.append(1 if list_of_labels[i] == "OK" else -1)
            # Add new list to label results
            if i % 2 == 0:
                labels_even.append(label_even)
            else:
                labels_odd.append(label_odd)

        # Transpose data for better visualisation (optional)
        labels_even = list(map(list, zip(*labels_even)))
        labels_odd = list(map(list, zip(*labels_odd)))

        # Create a subplot with 1 row and 2 columns
        plt.subplot(1, 2, 1)
        plt.imshow(labels_even, cmap="RdYlGn")
        plt.title("First screw hole (left)")
        plt.colorbar()

        # Create another subplot in the same row
        plt.subplot(1, 2, 2)
        plt.imshow(labels_odd, cmap="RdYlGn")
        plt.title("Second screw hole (right)")
        plt.colorbar()

        # Adjust layout to prevent clipping of titles and show plot
        # plt.tight_layout()
        plt.show()
