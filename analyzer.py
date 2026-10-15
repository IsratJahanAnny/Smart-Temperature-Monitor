"""
analyzer.py

Contains the "decision-making" logic of the project:
- Classifying a temperature reading as NORMAL / WARNING / CRITICAL
- Detecting abnormal readings out of a batch
- Saving readings to a CSV file for record-keeping

Keeping this logic separate from sensor_simulator.py means the
thresholds and file-saving code could be reused even if the data
came from a real sensor instead of a simulated one.
"""

import csv
import os

# Temperature thresholds in degrees Celsius.
# These are the only numbers you'd need to change to
# tune the system for a different type of machine.
WARNING_THRESHOLD = 70.0    # 70.0 - 84.9 -> WARNING
CRITICAL_THRESHOLD = 85.0   # 85.0 and above -> CRITICAL

CSV_FIELDNAMES = ["timestamp", "machine", "temperature", "status"]


def classify_temperature(temperature):
    """
    Classify a single temperature reading into a status string.

    Rules:
        < 70.0          -> "NORMAL"
        70.0 - 84.9     -> "WARNING"
        >= 85.0         -> "CRITICAL"
    """
    if temperature >= CRITICAL_THRESHOLD:
        return "CRITICAL"
    elif temperature >= WARNING_THRESHOLD:
        return "WARNING"
    else:
        return "NORMAL"


def detect_abnormal(readings):
    """
    Given a list of reading dictionaries (each already containing a
    "status" key), return only the ones that are WARNING or CRITICAL.

    This is useful for printing an "ALERT" summary to the user.
    """
    abnormal = []
    for reading in readings:
        if reading["status"] in ("WARNING", "CRITICAL"):
            abnormal.append(reading)
    return abnormal


def save_readings_to_csv(readings, filepath):
    """
    Append a list of readings to a CSV file, creating the file
    (with a header row) if it doesn't exist yet.

    Basic error handling is included so a permissions problem or
    missing folder doesn't crash the whole program.
    """
    try:
        # Make sure the folder for the CSV file exists.
        folder = os.path.dirname(filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        file_already_exists = os.path.isfile(filepath)

        with open(filepath, mode="a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)

            # Only write the header once, when the file is first created.
            if not file_already_exists:
                writer.writeheader()

            for reading in readings:
                writer.writerow({
                    "timestamp": reading["timestamp"],
                    "machine": reading["machine"],
                    "temperature": reading["temperature"],
                    "status": reading["status"],
                })

        return True

    except (IOError, OSError) as error:
        print(f"Error: Could not save readings to '{filepath}'. Details: {error}")
        return False
