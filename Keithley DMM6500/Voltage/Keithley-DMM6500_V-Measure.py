import csv
import time
import pyvisa

def main():
    # Connect to the Keithley DMM6500
    rm = pyvisa.ResourceManager()
    dmm = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')  # Replace with your instrument's VISA address

    # Setup DMM for voltage measurements
    dmm.write("*RST")
    dmm.write(":SENS:FUNC:VOLT:DC")

    # Create CSV file for logging
    csv_file = open("V_DMM6500.csv", "w", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Timestamp", "Voltage (V)"])

    try:
        # Continuously collect voltage readings
        while True:
            start_time = time.time()

            # Query voltage reading from DMM
            voltage = float(dmm.query(":MEAS:VOLT:DC?"))

            # Log timestamp and voltage to CSV file
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
            csv_writer.writerow([timestamp, voltage])
            csv_file.flush()  # Flush buffer to ensure data is written immediately

            # Wait for next reading
            elapsed_time = time.time() - start_time
            time.sleep(max(0, 0.1 - elapsed_time))  # Ensure 10 readings per second

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        # Close CSV file and instrument connection
        csv_file.close()
        dmm.close()
        rm.close()

if __name__ == "__main__":
    main()
