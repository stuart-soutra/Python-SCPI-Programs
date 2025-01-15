#----------Keysight 34460A - Current Measurement - Bus Triggered - Fixed Sample Count----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 14/01/2025
#   - Version: 1.0
#   - Description: - This program sets up DC current measurements on a Keysight 34460A. Settings are shown below...
#                  - Default Settings:
#                       - Trigger source: BUS
#                       - Default number of readings: 2000          User selectable - change 'user_num_cycles' variable
#                       - Fs = 100Hz                                User selectable - change 'fs' variable
#                       - Results transferred to a .csv file upon reading completion
#                  - Equipment Required:
#                       - Keysight 34460A DMM  (default)
#                  - File structure/Pre-requisites:
#                       - DO NOT DELETE 'test_numbers.txt' file     -       file stores the current test result number
#                       - All test results are saved to the relative directory

import csv
import time
import pyvisa
import os
from datetime import datetime

def check_and_create_test_number_file(file_path='test_number.txt'):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('1')
        print(f"{file_path} not found, File created and initialised to 1.")

def read_test_number(file_path='test_number.txt'):
    with open(file_path, 'r') as file:
        test_number = int(file.read().strip())
    return test_number
    
def update_test_number(test_number, file_path='test_number.txt'):
    with open (file_path, 'w') as file:
        file.write(str(test_number))

def save_current_values_to_csv(current_values):
    check_and_create_test_number_file()
    test_number = read_test_number()
    current_date = datetime.now().strftime('%d-%m-%Y')
    filename = f"CURRENT-MEASURE_{test_number:04d}_{current_date}.csv"
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Current Values (A)"])
        for value in current_values:
            writer.writerow([value])
    print(f"Data saved to {filename}")
    
    update_test_number(test_number + 1)
    

def main():
    ## SETUP ###########
    #setup resource manager
    rm = pyvisa.ResourceManager()
    
    #connect to DMM
    dmm = rm.open_resource('TCPIP::10.0.0.9::INSTR')
        
    #add default string terminators for each instrument
    dmm.read_termination = '\n'
    
    #summary of program operation
    print("--------------------------------------------------------------------------------------------")
    print("-------------------- CURRENT MEASUREMENT - BUS TRIG, FIXED SAMPLE COUNT --------------------")
    print("--------------------------------------------------------------------------------------------")
    print("     This program sets up DC current measurements on a Keysight 34460A. Settings are shown below...")
    print("     Default settings:")
    print("         - Trigger source: BUS")
    print("         - Default number of readings: 2000          User selectable - change 'user_num_cycles' variable")
    print("         - Fs = 100Hz                                User selectable - change 'fs' variable")
    print("         - Results transferred to a .csv file upon reading completion")
    print("\n")
    print("     Equipment required (all must be LXI/VISA capable):")
    print("         - Digital multimeter - Keysight 34460A used by default")
    print("\n")
    print("     File structure/Pre-requisites")
    print("         - DO NOT DELETE 'test_numbers.txt' file")
    print("         - All test results are saved to the relative directory")
    print("\n")
    print("     If an unrecoverable fault occurs on a piece of test equipment - shut this program and power-cycle the device in question.")
    print("\n")
    print("     PLEASE ENSURE THAT NO CONNECTIONS HAVE BEEN MADE TO THE TEST EQUIPMENT UPON BEGINNING THE TEST!")
    print("     To begin the test, please press 'ENTER'")
    input()
    
    #query IDs and complete connection
    print("Connection to Digital Multimeter established")
    print(dmm.query("*IDN?"),"\n")
        
    #reset all instruments
    dmm.write("*RST")
    print("Full reset complete\n")
    print("\n\n\n\n")
    ####################
    
    
    
    
    while True:
        
        user_num_cycles = 2000                                  #ENTER YOUR PREFFERED CYCLE AMOUNT HERE
        fs = 100                                                #ENTER YOUR PREFFERED SAMPLE FREQUENCY HERE
        
        num_cycles = 0
        
        current_values = []
        
        dmm.write("CONF:CURR:DC")                               #set to DC current measurement mode
        dmm.write("CURR:DC:NPLC 0.02")
        
        print("Check that DMM is connected in series with load, press 'ENTER' to confirm.")
        input()
        
        print("Press 'ENTER' to begin readings, or close program to exit.")
        input()
        
        print("Taking ",num_cycles, " Readings")
        while(num_cycles < user_num_cycles):
            reading = float(dmm.query("READ?"))
            current_values.append(reading)
            time.sleep(1/fs)                                        
            num_cycles = num_cycles + 1
            print(num_cycles)

        save_current_values_to_csv(current_values)              #save to .csv

        print("Readings stored successfully, resetting in 5 seconds...")
        time.sleep(5)
        
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        
    
if __name__ == "__main__":
    main()
    
    
