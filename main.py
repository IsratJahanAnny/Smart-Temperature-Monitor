"""
main.py

Entry point for the Smart Temperature Monitor.

Run with:
    python main.py

This script ties together the three other modules:
    - sensor_simulator.py  -> generates fake sensor readings
    - analyzer.py          -> classifies readings and saves them to CSV
    - visualizer.py        -> draws a graph of the temperature history

It does not contain any "business logic" itself - it just calls the
right function from the right module and displays the results.
"""

import sensor_simulator
import analyzer
import visualizer

CSV_PATH = "data/sensor_data.csv"
GRAPH_PATH = "data/temperature_graph.png"


def print_header():
    """Print the program's title banner."""
    print("=" * 36)
    print("   SMART TEMPERATURE MONITOR")
    print("=" * 36)


def print_reading(reading):
    """Nicely print a single machine's reading and status."""
    print(reading["machine"])
    print(f"Temperature: {reading['temperature']}°C")
    print(f"Status: {reading['status']}")
    print()


def run_monitoring_cycle():
    """
    Run one full monitoring cycle:
        1. Generate readings for all machines
        2. Classify each reading
        3. Display the results
        4. Report any abnormal (WARNING/CRITICAL) readings
        5. Save all readings to the CSV file
        6. Regenerate the temperature graph
    """
    print_header()

    # Step 1: get fresh simulated readings
    readings = sensor_simulator.generate_all_readings()

    # Step 2: classify each reading and display it
    for reading in readings:
        reading["status"] = analyzer.classify_temperature(reading["temperature"])
        print_reading(reading)

    # Step 3: check for abnormal readings and alert the user
    abnormal_readings = analyzer.detect_abnormal(readings)
    if abnormal_readings:
        print("!!! ALERT: Abnormal temperature(s) detected !!!")
        for reading in abnormal_readings:
            print(f" - {reading['machine']} is {reading['status']} "
                  f"at {reading['temperature']}°C")
        print()
    else:
        print("All machines are operating normally.")
        print()

    # Step 4: save this cycle's readings to the CSV file
    if analyzer.save_readings_to_csv(readings, CSV_PATH):
        print(f"Sensor readings saved to:\n{CSV_PATH}")
    else:
        print("Warning: Sensor readings were NOT saved due to an error.")

    # Step 5: regenerate the graph using the full CSV history
    if visualizer.plot_temperatures(CSV_PATH, GRAPH_PATH):
        print("Temperature graph generated successfully.")
    else:
        print("Warning: Temperature graph could not be generated.")


def main():
    """Main program loop: run cycles until the user chooses to stop."""
    while True:
        run_monitoring_cycle()

        print()
        again = input("Run another monitoring cycle? (y/n): ").strip().lower()
        print()

        if again != "y":
            print("Exiting Smart Temperature Monitor. Goodbye!")
            break


if __name__ == "__main__":
    main()
