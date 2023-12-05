import matplotlib.pyplot as plt
from typing import Type

from load.base_loader import BaseLoader


class BasePlotter:
    def __init__(self, base_loader: Type[BaseLoader]):
        """
        Initialize the plotter with a BaseLoader instance.
        Args:
            base_loader (Type[BaseLoader]): An instance of a BaseLoader or its subclass.
        """
        self.base_loader = base_loader

    def plot_dmc_counts(self) -> None:
        """
        Plot a bar chart of the counts of screw runs for each workpiece by DMC.
        """
        x_values = list(self.base_loader.counts_of_dmc.keys())
        y_values = list(self.base_loader.counts_of_dmc.values())
        plt.bar(x=x_values, height=y_values)
        plt.xlabel("Data Matrix Code (DMC) of the workpieces")
        plt.ylabel("Number of occurrences")
        plt.xticks(rotation=45, ha="right")
        plt.title("Number of screw runs for each workpiece by DMC")
        plt.show()

    def plot_dmc_label_ratio(self):
        """
        Plot the ratio of 'OK' and 'NOK' observations with regard to the cycle number.
        """
        max_length = max(
            [len(label) for label in self.base_loader.labels_of_dmc.values()]
        )
        ratios_OK, ratios_NOK = self.calculate_ratios(max_length)
        x_values = range(int(max_length / 2))

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

    def calculate_ratios(self, max_length):
        """
        Calculate the ratio of 'OK' and 'NOK' for each index across the lists.
        Args:
            max_length (int): The maximum length of labels for a workpiece.
        Returns:
            Tuple: Two lists containing ratios for 'OK' and 'NOK'.
        """
        ratios_OK, ratios_NOK = [], []

        for i in range(0, max_length, 2):
            ok_count, nok_count = self.calculate_counts(i)
            total_count = ok_count + nok_count
            ratio_OK = ok_count / total_count if total_count != 0 else 0
            ratio_NOK = nok_count / total_count if total_count != 0 else 0
            ratios_OK.append(ratio_OK)
            ratios_NOK.append(ratio_NOK)

        return ratios_OK, ratios_NOK

    def calculate_counts(self, index):
        """
        Calculate the number of 'OK' and 'NOK' results for one workpiece.
        Args:
            index (int): The index representing a screw cycle.
        Returns:
            Tuple: Two integers representing the counts of 'OK' and 'NOK'.
        """
        ok_count = sum(
            self.base_loader.labels_of_dmc[key][index] == "OK"
            for key in self.base_loader.labels_of_dmc
        ) + sum(
            self.base_loader.labels_of_dmc[key][index + 1] == "OK"
            for key in self.base_loader.labels_of_dmc
        )

        nok_count = sum(
            self.base_loader.labels_of_dmc[key][index] == "NOK"
            for key in self.base_loader.labels_of_dmc
        ) + sum(
            self.base_loader.labels_of_dmc[key][index + 1] == "NOK"
            for key in self.base_loader.labels_of_dmc
        )

        return ok_count, nok_count

    def plot_dmc_label_heatmap(self) -> None:
        """
        Plot a heatmap of 'OK' and 'NOK' observations for the first and second screw holes.
        """
        max_length = max(
            [len(label) for label in self.base_loader.labels_of_dmc.values()]
        )
        labels_even, labels_odd = self.create_heatmap_data(max_length)

        plt.subplot(1, 2, 1)
        plt.imshow(labels_even, cmap="RdYlGn")
        plt.title("First screw hole (left)")
        plt.colorbar()

        plt.subplot(1, 2, 2)
        plt.imshow(labels_odd, cmap="RdYlGn")
        plt.title("Second screw hole (right)")
        plt.colorbar()

        plt.tight_layout()
        plt.show()

    def create_heatmap_data(self, max_length):
        """
        Create data for the heatmap visualization.
        Args:
            max_length (int): The maximum length of labels for a workpiece.
        Returns:
            Tuple: Two lists containing heatmap data for even and odd indices.
        """
        labels_even, labels_odd = [], []

        for i in range(max_length):
            label_even, label_odd = [], []

            for list_of_labels in self.base_loader.labels_of_dmc.values():
                if i % 2 == 0:
                    label_even.append(1 if list_of_labels[i] == "OK" else -1)
                else:
                    label_odd.append(1 if list_of_labels[i] == "OK" else -1)

            if i % 2 == 0:
                labels_even.append(label_even)
            else:
                labels_odd.append(label_odd)

        labels_even = list(map(list, zip(*labels_even)))
        labels_odd = list(map(list, zip(*labels_odd)))

        return labels_even, labels_odd

    def plot_hist_run_lengths(self, how: str = "count", bins: int = 25) -> None:
        """
        Plot a histogram of run lengths or maximum angles.
        Args:
            how (str): Either "count" for run lengths or "angle" for maximum angles.
            bins (int): Number of bins in the histogram.
        """
        if how not in ["count", "angle"]:
            raise ValueError(f"Invalid value for 'how': {how}. Use 'count' or 'angle'.")

        if not self.base_loader.all_runs:
            print("No runs to plot the histogram.")
            return

        run_lengths = self.get_run_lengths(how)
        title, xlabel = self.get_plot_labels(how)

        plt.hist(run_lengths, bins=bins, color="blue", edgecolor="black", alpha=0.7)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("Number of occurrences")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

    def get_run_lengths(self, how):
        """
        Get the lengths or max angles of all screw runs.
        Args:
            how (str): Either "count" for run lengths or "angle" for maximum angles.
        Returns:
            List: A list containing lengths or max angles of all screw runs.
        """
        if how == "count":
            return [len(run.time_values) for run in self.base_loader.all_runs]
        elif how == "angle":
            return [max(run.angle_values) for run in self.base_loader.all_runs]

    def get_plot_labels(self, how) -> None:
        """
        Get the title and xlabel for the histogram plot.
        Args:
            how (str): Either "count" for run lengths or "angle" for maximum angles.
        Returns:
            Tuple: Two strings representing the title and xlabel.
        """
        if how == "count":
            return "Histogram of steps in time series", "Length of all screw runs"
        elif how == "angle":
            return "Histogram of max angles", "Max angle of all screw runs [degree]"

    def plot_avg(self):
        mean_torque, var_torque = self.base_loader.aggregate_all_series(
            self.base_loader.get_torque_values()
        )
        mean_time, var_time = self.base_loader.aggregate_all_series(
            self.base_loader.get_time_values()
        )
        mean_angle, var_angle = self.base_loader.aggregate_all_series(
            self.base_loader.get_angle_values()
        )

        _, ax = plt.subplots()
        ax.fill_between(
            mean_angle, mean_torque + var_torque, mean_torque - var_torque, alpha=0.25
        )
        ax.plot(mean_angle, mean_torque)
        plt.xlabel("Angle [degree]")
        plt.ylabel("Torque [in Nm]")
        plt.title("Average screw run (and variance)")
        plt.show()

    def plot_all(self):
        colors = {
            "OK": "forestgreen",
            "NOK": "firebrick",
        }
        # Iterate all screw runs loaded
        for torques, angles, results in zip(
            self.base_loader.get_torque_values(),
            self.base_loader.get_angle_values(),
            self.base_loader.get_run_results(),
        ):
            plt.plot(
                angles,
                torques,
                color=colors[results],
                alpha=0.5,
                linewidth=0.5,
            )
        plt.xlabel("Angle [degree]")
        plt.ylabel("Torque [in Nm]")
        plt.title("Visualization of all screw runs")
        plt.show()
