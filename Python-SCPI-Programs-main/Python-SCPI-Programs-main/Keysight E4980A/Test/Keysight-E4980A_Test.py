#----------Keysight E4980A LCR Meter - Test----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 15/01/2025
#   - Version: 1.0
#   - Description: - Program tests connection and impedance reading setup from the meter.

import pyvisa

def main():
    # Connect to the Keysight E4980 LCR Meter
    rm = pyvisa.ResourceManager()
    lcr = rm.open_resource('TCPIP0::K-E4980A-22227.local::inst0::INSTR')  # Replace with your instrument's VISA address
    
    # Reset meter
    lcr.write("*RST")
	
    # Set trigger function to WAIT FOR TRIGGER
    lcr.write(":TRIG:SOUR BUS")

    # Device waiting for trigger now

    # Setup LCR for Cp-Rp measurements
    lcr.write(":FUNC:IMP:TYPE CPRP")

    # Change output data type to ASCII
    lcr.write(":FORMAT:DATA ASCII")

    try:
	# Set initial frequency
        lcr.write(":FREQ:CW 20")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement



        print("Impedance:", imp, "F")

        # Keep the script running until manually terminated
        input("Press Enter to exit...")

    finally:
        # Close instrument connection
        lcr.close()
        rm.close()
        input()


if __name__ == "__main__":
    main()


