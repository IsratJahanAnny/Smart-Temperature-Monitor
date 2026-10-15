"""
sensor_simulator.py

Simulates temperature readings for a set of machines.

This module does NOT know anything about "normal", "warning", or
"critical" thresholds - it only produces realistic-looking numbers,
the way a real sensor would. Classifying those numbers is the job
of analyzer.py.
"""

import random
from datetime import datetime

# The list of machines we are "monitoring".
# Feel free to add more machine names here - the rest of the
# program will automatically pick them up.
MACHINES = ["Machine 01", "Machine 02", "Machine 03"]

# Each machine gets its own "typical" baseline temperature.
# This makes the simulation feel more realistic than pure random noise,
# since real machines usually run around a consistent baseline.
BASELINE_TEMPERATURES = {
    "Machine 01": 65.0,
    "Machine 02": 72.0,
    "Machine 03": 80.0,
}

# Chance (0.0 - 1.0) that a reading will be a random "spike",
# simulating an overheating event. This guarantees we occasionally
# see WARNING/CRITICAL readings instead of only NORMAL ones.
SPIKE_PROBABILITY = 0.25


def generate_temperature(machine_name):
    """
    Generate a single simulated temperature reading for one machine.

    Returns a float temperature in degrees Celsius.
    """
    # Use the machine's baseline if we know it, otherwise default to 65.0
    baseline = BASELINE_TEMPERATURES.get(machine_name, 65.0)

    # Small natural fluctuation around the baseline (like real sensor noise)
    fluctuation = random.uniform(-4.0, 4.0)
    temperature = baseline + fluctuation

    # Occasionally simulate a temperature spike (overheating event)
    if random.random() < SPIKE_PROBABILITY:
        spike = random.uniform(10.0, 25.0)
        temperature += spike

    # Round to 1 decimal place, like a real sensor readout
    return round(temperature, 1)


def generate_all_readings(machines=None):
    """
    Generate one temperature reading for every machine in the given list.

    If no list is given, defaults to the MACHINES list above.

    Returns a list of dictionaries, one per machine, in the form:
        {
            "machine": "Machine 01",
            "temperature": 67.4,
            "timestamp": "2026-09-02 14:35:10"
        }
    """
    if machines is None:
        machines = MACHINES

    readings = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for machine_name in machines:
        temperature = generate_temperature(machine_name)
        readings.append({
            "machine": machine_name,
            "temperature": temperature,
            "timestamp": timestamp,
        })

    return readings
