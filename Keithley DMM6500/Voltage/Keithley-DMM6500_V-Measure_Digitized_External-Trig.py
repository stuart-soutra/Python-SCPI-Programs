#----------Keithley DMM6500 - Voltage Measurement - Digitized Reading - External Trigger----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 14/01/2025
#   - Version: 1.0
#   - Description: - Program takes digitized voltage readings on a Keithley DMM6500, using an external trigger to begin the readings.
#		   - Users can specify the sample rate and number of samples to read.
#		   - Output data is stored as a .csv file with each entry being a double precision float.



import csv
import time
import pyvisa
from tqdm import tqdm


# Program description
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("----Keithley DMM6500 - Voltage Measurement - Digitized Reading - External Trigger----")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("\n")
print("    - Author: Stuart Thomas")
print("    - Date: 14/01/2025")
print("    - Version: 1.0")
print("    - Description:")
print("        - Program takes digitized voltage readings on a Keithley DMM6500, using an external trigger to begin the readings.")
print("        - Users can specify the sample rate and number of samples to read.")
print("        - Output data is stored as a .csv file with each entry being a double precision float.")
print("    - Pre-requisites:")
print("        - pyvisa Python library")
print("        - NI-VISA drivers")
print("        - tqdm Python library")
print("\n\n")

# Calibration prompt
print("Please ensure DMM has an up-to-date calibration and record")
input("Press any key when complete...")
print("\n\n")


# Prompt user to connect instrument to DUT
print("Please make the following physical connections:")
print("     - DMM HI Input (Red)                   -->     Positive voltage ref to read")
print("     - DMM LOW Input (Black)                -->     Negative voltage ref to read")
print("     - DMM EXT TRIG IN (back of unit)       -->     TTL trigger source (rising edge activated)")
input("Press any key when complete...")
print("\n\n")

# Prompt user to set sample rate
sample_rate = int(input("Please enter the desired sample rate (between 1000Hz and 1000000Hz): "))
print("\n\n")

# Prompt user to set number of samples
num_samples = int(input("Please enter the desired number of samples to be acquired (between 1 and 100000): "))
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def main():
    # Connect to the Keithley DMM6500
    rm = pyvisa.ResourceManager()
    dmm = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')     # See PyVisa main webpage for setup information

    # Setup DMM for voltage measurements
    dmm.write("*RST")
    dmm.write(":DIG:FUNC 'VOLT'")					# Digitize mode - voltage measurements
    dmm.write(f":DIG:VOLT:SRATE {sample_rate}")				# Digitize mode - sample rate
    dmm.write(":DIG:VOLT:APER AUTO")					# Digitize mode - auto aperture setting
    dmm.write(f":DIG:COUNT {num_samples}")				# Digitize mode - number of samples to take (to be stored in 'defbuffer1')

    # Setup trigger
    dmm.write(":TRIG:EXT:IN:CLE")					# Clear previous ext trigger flags
    dmm.write(":TRIG:EXT:IN:EDGE RIS")

    # Setup TriggerFlow Block - 0=IDLE, 1=WAIT, 2=MEASURE/DIGITIZE
    dmm.write(":TRIG:BLOCK:BUFF:CLEAR 1")				# Clear defbuffer1
    dmm.write(":TRIG:BLOCK:WAIT 1, EXT")				# Add 'WAIT' block - make external 'Ext In' break
    dmm.write(f":TRIG:BLOCK:MDIG 2, 'defbuffer1', {num_samples}")	        # Add 'MDIG' block - store digitized measurement in 'defbuffer1'

    # Initilise DMM - wait for external trigger
    dmm.write("INIT")
    print("Waiting for external trigger activation...")
    print("\n\n")

    # Wait for buffer to be full...
    with tqdm(total=num_samples, desc="Readings Taken: ", ncols=100) as pbar:    # Add tqdm prog bar
        while int(dmm.query(":TRAC:ACTUAL?")) < num_samples:
            current_sample = int(dmm.query(":TRAC:ACTUAL?"))
            pbar.update(current_sample - pbar.n)

    # Read buffer
    v_data = dmm.query(f":TRAC:DATA? 1, {num_samples}, 'defbuffer1', READ")
    v_data_floats = parse_data(v_data)					# Convert multi-row string into single row float for each element

    # Create CSV file for logging
    csv_file = open("V_DMM6500_b.csv", "w", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([f"Sample Rate: {sample_rate}"])
    csv_writer.writerow([f"No. Samples: {num_samples}"])
    csv_writer.writerow(["Voltage (V)"])
    for data in v_data_floats:
    	csv_writer.writerow([data])

    # Close CSV file and instrument connection
    csv_file.close()
    dmm.close()
    rm.close()

    print("Measurement complete - see 'V_DMM6500_b' (in relative folder) for output.")

def parse_data(v_data):
    """
    Parses the voltage data array where each number is represented as a list of characters
    and returns a list of floating-point numbers. Handles negative numbers and skips malformed entries.
    """
    v_data_floats = []

    # First, join the list of characters into a string, then split by commas to separate each number
    voltage_string = ''.join(v_data)  # Join all characters into a single string

    # Split the string by commas to separate each voltage reading
    voltage_entries = voltage_string.split(',')

    for voltage_str in voltage_entries:
        # Skip empty entries or malformed entries
        if not voltage_str or voltage_str in ['-', '.', 'E', '-.', '.E', 'E-']:
            print(f"Skipping invalid string: {voltage_str}")
            continue
        
        # Try to convert the valid voltage string to a float
        try:
            voltage_float = float(voltage_str)
            v_data_floats.append(voltage_float)
        except ValueError:
            print(f"Error converting voltage string to float: {voltage_str}")

    return v_data_floats
    

if __name__ == "__main__":
    main()

