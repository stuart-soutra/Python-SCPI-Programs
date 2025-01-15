#import pyvisa
#rm = pyvisa.ResourceManager()
#rm.list_resources()
#dmm = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')
#print(dmm.query("*IDN?"))
#input()


import pyvisa

def main():
    # Connect to the Keithley DMM6500
    rm = pyvisa.ResourceManager()
    dmm = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')  # Replace with your instrument's VISA address

    try:
        # Setup DMM for voltage measurements
        dmm.write(":CONF:VOLT:DC")
       # dmm.write(":SENS:VOLT:DC:NPLC 1")  # Set integration time for faster readings

        # Take a voltage measurement
        voltage = float(dmm.query(":READ?"))

        print("Voltage:", voltage, "V")

        # Keep the script running until manually terminated
        input("Press Enter to exit...")

    finally:
        # Close instrument connection
        dmm.close()
        rm.close()

if __name__ == "__main__":
    main()
