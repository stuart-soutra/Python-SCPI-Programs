#!/usr/bin/env python3

import csv
import time
import pyvisa
import os
from datetime import datetime

def process_scope_data(voltage_values):
    
    data = voltage_values[10:]          #strip header
    
    data_str = ''.join(data).replace(' ', '').replace('\n', '')     #clean up any spaces or newlines
    numbers = []
    
    while data_str:
        comma_index = data_str.find(',') if ',' in data_str else len(data_str)
        number_str = data_str[:comma_index].strip()
        
        if number_str:
            number = float(number_str)
            numbers.append(f"{number:.16f}")
            
        data_str = data_str[comma_index + 1:]
    return numbers

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
    
def save_current_and_voltage_to_csv(current_values, voltage_values, c_fs, v_fs):
    check_and_create_test_number_file()
    test_number = read_test_number()
    current_date = datetime.now().strftime('%d-%m-%Y')
    
    filename = f"CURRENT-AND-VOLTAGE-MEASURE_{test_number:04d}_{current_date}.csv"
    
    # Pad the shorter list with zeros to match the length of the longer list
    max_length = max(len(current_values), len(voltage_values))
    current_values += [0] * (max_length - len(current_values))
    voltage_values += [0] * (max_length - len(voltage_values))
    
    # Write the data to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the sample rates for each (current and voltage)
        writer.writerow(["Current FS (Hz)", "Voltage FS (Hz)"])
        writer.writerow([c_fs, v_fs])
        
        # Write the header row
        writer.writerow(["Current Values (A)", "Voltage Values (V)"])
        
        
        # Write each pair of values to the CSV
        for current, voltage in zip(current_values, voltage_values):
            writer.writerow([current, voltage])
    
    print(f"Data saved to {filename}")
    
    # Update the test number for future uses
    update_test_number(test_number + 1)
    

def main():
    ## SETUP ###########
    #setup resource manager
    rm = pyvisa.ResourceManager()
    
    #connect to DMM
    dmm = rm.open_resource('TCPIP::10.0.0.9::INSTR')
    
    #connect to scope
    scope = rm.open_resource('TCPIP::10.0.0.5::INSTR')
        
    #add default string terminators for each instrument
    dmm.read_termination = '\n'
    scope.read_termination = '\n'
    
    #summary of program operation
    print("--------------------------------------------------------------------------------------------")
    print("-------------- CURRENT AND VOLTAGE MEASUREMENT - BUS TRIG, FIXED SAMPLE COUNT --------------")
    print("--------------------------------------------------------------------------------------------")
    print("     This program sets up DC current and voltage measurements on a Keysight 34460A. Settings are shown below...")
    print("     Default settings:")
    print("         - Trigger source: BUS")
    print("         - Default number of readings: 2000          User selectable - change 'user_num_cycles' variable")
    print("         - Fs = 100Hz                                User selectable - change 'fs' variable")
    print("         - Results transferred to a .csv file upon reading completion")
    print("\n")
    print("     Equipment required (all must be LXI/VISA capable):")
    print("         - Digital multimeter - Keysight 34460A used by default")
    print("         - Oscilloscope - Keysight DSOX2004A 4-Channel Scope used by default")
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
    print("Connection to Oscilloscope established")
    print(scope.query("*IDN?"),"\n")
        
    #reset all instruments
    dmm.write("*RST")
    scope.write("*RST")
    print("Full reset complete\n")
    print("\n\n\n\n")
    ####################
    
    
    
    
    while True:
        
        user_num_cycles = 6000                                  #ENTER YOUR PREFFERED CYCLE AMOUNT HERE
        #c_fs = 100                                                #ENTER YOUR PREFFERED SAMPLE FREQUENCY HERE
        
        num_cycles = 0
        
        current_values = []
        voltage_values = []
        
        dmm.write("CONF:CURR:DC")                               #set to DC current measurement mode
        dmm.write("CURR:DC:NPLC 0.02")
        
        #setup scope
        scope.write(":CHAN1:SCALE 2\n")
        scope.write(":TIMEBASE:MAIN:SCALE 12\n")                 #######MIGHT NOT LIKE THIS
        scope.write(":TIM:REF LEFT\n")
        scope.write(":TIMEBASE:MODE MAIN")
        scope.write(":ACQ:TYPE NORM\n")
        scope.write(":WAV:FORM ASCII")
        scope.write(":WAV:POIN 50000")
        
        print("Scope Settings: 5s/div     1V/div      no trigger\n")
        
        print("Check that DMM is connected in series with load, press 'ENTER' to confirm.")
        input()
        print("Check that scope is connected in parallel with the load, press 'ENTER' to confirm.")
        input()
        print("Press 'ENTER' to begin readings, or close program to exit.")
        input()
        
        print("Taking ",num_cycles, " Readings")
        
        scope.write("STOP")  
        time.sleep(0.1)
        #take scope readings - digitize - start reading just before current measurements
        scope.write(":DIG CHAN1")
        
        start_time = datetime.now()
        
        
        #do current measurements
        while(num_cycles < user_num_cycles):
            readingC = float(dmm.query("READ?"))
            current_values.append(readingC)
            #time.sleep(0.04)                                                     #calculate fs rather than select                                        
            num_cycles = num_cycles + 1
            print(num_cycles,"    ",readingC)
        
        end_time = datetime.now()
        
        print(type(start_time))
        print(type(end_time))
        time.sleep(10)
        
        elapsed_time = end_time - start_time
        elapsed_s = elapsed_time.total_seconds()
        
        c_fs = user_num_cycles / elapsed_s

        print("Scope digitising waveform, please wait...")
        time.sleep(50)
        
        v_fs = scope.query(":ACQ:SRATE?")
        
        voltage_values = scope.query(":WAV:DATA?")  
        output_voltage_values = process_scope_data(voltage_values)
        #CONVERT VOLTAGE VALUES HERE
        
        save_current_and_voltage_to_csv(current_values, output_voltage_values, c_fs, v_fs)             #save to .csv

        print("Readings stored successfully, resetting in 5 seconds...")
        time.sleep(5)
        
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        
    
if __name__ == "__main__":
    main()
    
    
