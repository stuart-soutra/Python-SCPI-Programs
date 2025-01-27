#----------Sequential Polled Current and Voltage Measurement - Low Frequency----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 27/01/2025
#   - Version: 1.0
#   - Changelog: 
#   - Description: - Program takes sequential current readings and voltage measurements.
#                   - Users can specify the sample rate and number of samples to read (<10Hz).
#                   - Output data is stored as a .csv file with each entry being a double precision float.
#                   - Default Current Measurement device:    Keithley DMM6500
#                   - Default Voltage Measurement device:    Keysight 34460A

import csv
import time
import pyvisa

# Program description
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-----------Sequential Polled Current and Voltage Measurement - Low Frequency---------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("\n")
print("    - Author: Stuart Thomas")
print("    - Date: 27/01/2025")
print("    - Version: 1.0")
print("    - Description:")
print("        - Program takes sequential current readings and voltage measurements.")
print("        - Users can specify the sample rate and number of samples to read (<10Hz).")
print("        - Output data is stored as a .csv file with each entry being a double precision float.")
print("    - Default Current Measurement device:    Keithley DMM6500")
print("    - Default Voltage Measurement device:    Keysight 34460A")
print("    - Pre-requisites:")
print("        - pyvisa Python library")
print("        - NI-VISA drivers")
print("\n\n")

# Calibration prompt
print("Please ensure instruments have an up-to-date calibrations")
input("Press any key when complete...")
print("\n\n")


# Prompt user to connect instrument to DUT
print("Please make the following physical connections:")

print("     - Current DMM HI Input (Red)                   -->     Positive side current to read (in series)")
print("     - Current DMM LOW AMPS Input                   -->     Negative side current to read (in series)")
print("     - Voltage DMM HI Input (Red)                   -->     Positive voltage reference to read (in parallel)")
print("     - Voltage DMM LOW Input                        -->     Negative voltage reference to read (in parallel)")
input("Press any key when complete...")
print("\n\n")

# Prompt user to set sample rate
sample_period = int(input("Please enter the desired sample period (in seconds): "))
print("\n\n")

# Prompt user to set number of samples
num_samples = int(input("Please enter the desired number of samples to be acquired: "))
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def main():
    # Connect to the measurement instruments
    rm = pyvisa.ResourceManager()
    dmm_c = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')  # Current measurement (DMM1) - Keithley DMM6500 - replace with your instrument's VISA address
    dmm_v = rm.open_resource('USB0::0x2A8D::0x1601::MY60089707::INSTR')  # Voltage measurement - Keysight 34460A (DMM2) - Replace with your instrument's VISA address

    # Setup DMM1 for current measurements
    dmm_c.write("*RST")
    dmm_c.write(":SENS:FUNC:CURR:DC")

    # Setup DMM2 for voltage measurements
    dmm_v.write("*RST")
    dmm_v.write("CONF:VOLT:DC")                               #set to DC voltage measurement mode

    # Create CSV file for logging
    csv_file = open("CV_Log.csv", "w", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Timestamp", "Current (A)", "Voltage (V)"])

    try:
        print("Measurements being taken...")
        print("Press any key to abort.")
        cycle_count = 0                                             # Current measurement number
        # Collect readings
        while cycle_count < num_samples:
            start_time = time.time()

            # Query current reading from DMM1
            current = float(dmm_c.query(":MEAS:CURR:DC?"))
            # Query voltage reading from DMM2
            voltage = float(dmm_v.query("READ?"))

            # Log timestamp and current to CSV file with milliseconds
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
            csv_writer.writerow([timestamp, current, voltage])
            csv_file.flush()  # Flush buffer to ensure data is written immediately

            # Wait for next reading
            time.sleep(sample_period)  # user specified collection rate
            cycle_count = cycle_count + 1

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        print("\n\n")
        print("Measurements Complete!")
        print("Results stored in 'CV_Log.csv'")
        # Close CSV file and instrument connection
        csv_file.close()
        dmm_c.close()
        dmm_v.close()
        rm.close()

if __name__ == "__main__":
    main()
