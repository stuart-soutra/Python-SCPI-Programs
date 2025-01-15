#----------Keysight E4980A Cp-Rp - Single Frequency Sweep----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 03/05/2024
#   - Version: 1.0
#   - Description: This program connects to a Keysight E4980A LCR meter via. LAN, and activates a Cp-Rp single sweep measurement across the following frequencies: 20Hz, 100Hz, 1kHz, 10kHz, 100kHz, 1MHz, 2MHz.




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
	    # Set initial frequency - 20Hz Reading
        lcr.write(":FREQ:CW 20")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")

        # 100Hz Reading
        lcr.write(":FREQ:CW 100")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")

        # 1kHz Reading
        lcr.write(":FREQ:CW 1000")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")

        # 10kHz Reading
        lcr.write(":FREQ:CW 10000")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")

        # 100kHz Reading
        lcr.write(":FREQ:CW 100000")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")

        # 1MHz Reading
        lcr.write(":FREQ:CW 1000000")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")

        # 2MHz Reading
        lcr.write(":FREQ:CW 2000000")
        lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
        imp = lcr.query("*TRG")					# Take impedance measurement
        print("Impedance:", imp, "\n")
        

        # Keep the script running until manually terminated
        input("Press Enter to exit...")

    finally:
        # Close instrument connection
        lcr.close()
        rm.close()
        input()


if __name__ == "__main__":
    main()


