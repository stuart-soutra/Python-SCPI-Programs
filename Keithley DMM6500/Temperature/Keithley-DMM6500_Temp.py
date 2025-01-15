#----------Keithley DMM6500 Temperature - Single Temperature Reading----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 03/05/2024
#   - Version: 1.0
#   - Description: This program connects to a Keithley DMM6500 DMM via. LAN, and activates a single temperature measurement.

import pyvisa

def main():
    # Connect to the Keithley DMM6500
    rm = pyvisa.ResourceManager()
    dmm = rm.open_resource('TCPIP0::169.254.195.199::inst0::INSTR')  # Replace with your instrument's VISA address

    try:

        # Reset DMM
        dmm.write("*RST")

        # Setup DMM for temp measurements
       # dmm.write(:MEAS:TEMP?)
       

        # Take a temp measurement
        temperature = dmm.query(":MEAS:TEMP?")

        print("Temp:", temperature, "Degrees Centigrade")

        # Keep the script running until manually terminated
        input("Press Enter to exit...")

    finally:
        # Close instrument connection
        dmm.close()
        rm.close()

if __name__ == "__main__":
    main()
