"""
visualizer.py

Reads the full sensor reading history from the CSV file and draws
a simple line chart of temperature over time, one line per machine.

Uses:
    - pandas to load and organize the CSV data
    - matplotlib to draw and save the chart as an image
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend so this works
                        # even without a display (e.g. servers, CI).
import matplotlib.pyplot as plt


def plot_temperatures(csv_path, output_path="data/temperature_graph.png"):
    """
    Create a line chart of temperature vs. time for each machine,
    using all the historical data in the CSV file.

    Returns True if the graph was created successfully, False otherwise.
    """
    try:
        if not os.path.isfile(csv_path):
            print(f"Error: No data file found at '{csv_path}'. "
                  f"Run a monitoring cycle first to generate data.")
            return False

        data = pd.read_csv(csv_path)

        if data.empty:
            print("Error: The sensor data file is empty. Nothing to plot.")
            return False

        # Convert the timestamp column from text into real datetime objects
        # so matplotlib can space them out correctly on the x-axis.
        data["timestamp"] = pd.to_datetime(data["timestamp"])

        plt.figure(figsize=(10, 6))

        # Draw one line per machine, so trends are easy to compare.
        for machine_name, machine_data in data.groupby("machine"):
            plt.plot(
                machine_data["timestamp"],
                machine_data["temperature"],
                marker="o",
                label=machine_name,
            )

        # Reference lines showing where WARNING and CRITICAL start.
        plt.axhline(y=70.0, color="orange", linestyle="--", linewidth=1, label="Warning threshold (70°C)")
        plt.axhline(y=85.0, color="red", linestyle="--", linewidth=1, label="Critical threshold (85°C)")

        plt.title("Machine Temperature History")
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.xticks(rotation=30)
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()

        return True

    except Exception as error:
        # Broad catch here is intentional: plotting can fail for many
        # reasons (bad data, missing folder, etc.) and we don't want
        # a graph error to crash the whole monitoring program.
        print(f"Error: Could not generate graph. Details: {error}")
        return False
