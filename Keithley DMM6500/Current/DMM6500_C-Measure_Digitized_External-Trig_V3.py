#----------Keithley DMM6500 - Voltage Measurement - Digitized Reading - External Trigger----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 21/01/2026
#   - Version: 3.0
#    - Changelog: 2.0 -> 3.0
#          - Digitisation current range increased from default (1A) to 3A
#   - Description: - Program takes digitized current readings on a Keithley DMM6500, using an external trigger to begin the readings.
#		   - Users can specify the sample rate and number of samples to read.
#		   - Output data is stored as a .csv file with each entry being a double precision float.


import csv
import os
import time
import pyvisa
from tqdm import tqdm


# Program description
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("----Keithley DMM6500 - Current Measurement - Digitized Reading - External Trigger----")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("\n")
print("    - Author: Stuart Thomas")
print("    - Date: 23/06/2025")
print("    - Version: 2.0")
print("    - Description:")
print("        - Program takes digitized current readings on a Keithley DMM6500, using an external trigger to begin the readings.")
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
print("     - DMM HI Input (Red)                   -->     Positive side current to read (in series)")
print("     - DMM LOW AMPS Input (White)           -->     Negative side current to read (in series)")
print("     - DMM EXT TRIG IN (back of unit)       -->     TTL trigger source (rising edge activated)")
input("Press any key when complete...")
print("\n\n")

# Sample rate set to 1kHz by default
sample_rate = 1000

# Num samples set to 100000 by default (max digitisation value)
num_samples = 10000
buffer_size = num_samples + 5                                           # Make buffer size slightly larger than number of samples to be collected
#buffer_size = num_samples

def main():
    # Connect to the Keithley DMM6500
    rm = pyvisa.ResourceManager()
    dmm = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')     # See PyVisa main webpage for setup information

    # Setup DMM for voltage measurements
    dmm.write("*RST")
    dmm.write(":DIG:FUNC 'CURR'")					   # Digitize mode - current measurements

    # Set buffer name and size
    dmm.write(f":TRACE:MAKE 'cDataBuffer', {buffer_size}")

    # Set digitize parameters
    dmm.write(f":DIG:CURR:SRATE {sample_rate}")				# Digitize mode - sample rate
    dmm.write(":DIG:CURR:APER AUTO")					# Digitize mode - auto aperture setting
    dmm.write(f":DIG:COUNT {num_samples}")				# Digitize mode - number of samples to take (to be stored in 'defbuffer1')
    dmm.write(f":DIG:CURR:RANGE 3")                                     # Digitize mode - Current amplitude range (3A)
    
    
    # Setup trigger
    dmm.write(":TRIG:EXT:IN:CLE")					# Clear previous ext trigger flags
    dmm.write(":TRIG:EXT:IN:EDGE RIS")

    # Setup TriggerFlow Block - 0=IDLE, 1=WAIT, 2=MEASURE/DIGITIZE
    dmm.write(":TRIG:BLOCK:BUFF:CLEAR 1")				# Clear defbuffer1
    dmm.write(":TRIG:BLOCK:WAIT 1, EXT")				# Add 'WAIT' block - make external 'Ext In' break
    dmm.write(f":TRIG:BLOCK:MDIG 2, 'cDataBuffer', {num_samples}")	        # Add 'MDIG' block - store digitized measurement in 'defbuffer1'
    dmm.write(":TRIG:BLOCK:NOTIFY 3, 1")                # Create Notify block for block 3, call it 'Notify1'
    dmm.write(":TRIG:EXT:OUT:LOG POS")                  # Set ext out trigger to positive pulse logic
    dmm.write("TRIG:EXT:OUT:STIM NOTIFY1")              #Stimulus for ext trigger is assertion of 'Notify1' Triggerflow block

    # Initilise DMM - wait for external trigger
    dmm.write("INIT")
    print("Waiting for external trigger activation...")
    print("\n\n")

    # Wait for buffer to be full...
    with tqdm(total=num_samples, desc="Readings Taken: ", ncols=100) as pbar:    # Add tqdm prog bar
        while int(dmm.query(":TRAC:ACTUAL? 'cDataBuffer'")) < num_samples:
            current_sample = int(dmm.query(":TRAC:ACTUAL? 'cDataBuffer'"))
            pbar.update(current_sample - pbar.n)

    # Read buffer
    c_data = dmm.query(f":TRAC:DATA? 1, {num_samples}, 'cDataBuffer', READ")
    c_data_floats = parse_data(c_data)					# Convert multi-row string into single row float for each element

    # File to store the current test number
    test_number_file = "test_number.txt"

    # Check if the file exists, if not create it with test number 1
    if not os.path.exists(test_number_file):
        with open(test_number_file, "w") as f:
            f.write("1")

    # Read the current test number
    with open(test_number_file, "r") as f:
        test_number = int(f.read().strip())

    # Create a unique filename based on the test number
    csv_filename = f"C_DMM6500_c_{test_number}.csv"

    # Write data to CSV file
    with open(csv_filename, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([f"Sample Rate: {sample_rate}"])
        csv_writer.writerow([f"No. Samples: {num_samples}"])
        csv_writer.writerow(["Current (A)"])
        for data in c_data_floats:
            csv_writer.writerow([data])

    # Update test number for next run
    with open(test_number_file, "w") as f:
        f.write(str(test_number + 1))

 

    # Close CSV file and instrument connection
    #csv_file.close()
    dmm.close()
    rm.close()

    print(f"Measurement complete - see 'C_DMM6500_c_{test_number}.csv' (in relative folder) for output.")

def parse_data(c_data):
    """
    Parses the current data array where each number is represented as a list of characters
    and returns a list of floating-point numbers. Handles negative numbers and skips malformed entries.
    """
    c_data_floats = []

    # First, join the list of characters into a string, then split by commas to separate each number
    current_string = ''.join(c_data)  # Join all characters into a single string

    # Split the string by commas to separate each voltage reading
    current_entries = current_string.split(',')

    for current_str in current_entries:
        # Skip empty entries or malformed entries
        if not current_str or current_str in ['-', '.', 'E', '-.', '.E', 'E-']:
            print(f"Skipping invalid string: {current_str}")
            continue
        
        # Try to convert the valid voltage string to a float
        try:
            current_float = float(current_str)
            c_data_floats.append(current_float)
        except ValueError:
            print(f"Error converting current string to float: {current_str}")

    return c_data_floats
    

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nScript aborted by user.")

