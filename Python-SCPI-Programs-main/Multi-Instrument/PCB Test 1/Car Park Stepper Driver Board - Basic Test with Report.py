#----------Engineering Applications Module - Car Park Stepper Motor Driver Board PCB Test with Report----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 15/01/2025
#   - Version: 1.0
#   - Description: - Program runs tests on the stepper motor driver PCB used in the Edinburgh Napier University Engineering Applications module.
#                   Tests Performed:
#                       - Short-circuit/resistance check
#                       - Power up test
#                       - Clock peak-to-peak voltage
#                       - Clock frequency
#                       - Relay operation check
#                       - Board functional test

#                   Default instrument 1: AimTTI CPX400DT DC Power Supply
#                   Default instrument 2: Keysight DSO-X 2004A Oscilloscope
#                   Default instrument 3: Keysight EDU33212A Function Generator
#                   Default instrument 4: Keysight 34460A DMM

#                   Hardware setup described during test operation.

#                   Test report logged to output file in relative folder.

import csv
from datetime import datetime
import os
import time
import pyvisa

#file to store test number
TEST_NUMBER_FILE = "test_number.txt"

#function to init test number file if it doesn't exist
def init_test_number():
    if not os.path.exists(TEST_NUMBER_FILE):
        with open(TEST_NUMBER_FILE, 'w') as file:
            file.write('1')                                     #init test number to '1'
            
#function to read current test number
def get_test_number():
    with open(TEST_NUMBER_FILE, 'r') as file:
        test_number = int(file.read())
    return test_number
    
#function to update the test number
def increment_test_number():
    test_number = get_test_number() +1
    with open(TEST_NUMBER_FILE, 'w') as file:
        file.write(str(test_number))
    
#function to create test report
def create_test_report():
    init_test_number()
    
    test_number = get_test_number()
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    filename = f"STEPPER-PCB-TEST_{test_number:04d}_{current_date}.csv"
    
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    results = run_tests()
    
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    overall_result = "PASS" if all(result['status'] == "PASS" for result in results) else "FAIL"
    
    #prompt user to enter notes
    print("\nPlease enter any notes or observations for this test (or leave blank):")
    user_notes = input("Notes: ").strip()
    
    #create the csv file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        #write header info
        writer.writerow(["Test Number",test_number])
        writer.writerow(["Start Time",start_time])
        writer.writerow(["End Time",end_time])
        writer.writerow([])
        
        #write test results header
        writer.writerow(["Test Name", "Result", "Measurement Values"])
        
        #write each test result
        for result in results:
            writer.writerow([result['test_name'], result['status'],result.get('values',"N/A")])
        
        #write overall result
        writer.writerow([])
        writer.writerow(["Overall Result", overall_result])
        
        #add user notes
        writer.writerow([])
        writer.writerow(["User Notes", user_notes or "No notes provided"])
        
    increment_test_number()
    
    print(f"\nTest report saved as {filename}")

def run_tests(): 
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")       #enough new line to force it to a 'fresh' screen
    test_results = []

    #while True:
    ## TEST 1 - Check +12V Resistance ##
    print("----TEST 1----\n")
    print("----Check Power Supply Resistances----\n")
    print("             ++Connect RED terminal of DMM to CTS and BLACK to P2 on the DUT\n")     
    print("             ++Press 'ENTER' when complete...\n")
    input()
    dmm.write("CONF:RES")                                           #set DMM to R mode
    R_12V_Reading = float(dmm.query("READ?"))
    if R_12V_Reading > 100.0:
        print("+12V to ground resistance = ",R_12V_Reading,"\n")
        print("TEST PASSED\n")
        status = "PASS"
    elif R_12V_Reading < 100.0:
        print("+12V to ground resistance = ",R_12V_Reading,"\n")
        print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
        status = "FAIL"
    test_results.append({
        "test_name": "Test 1a: +12V to GND Resistance Test",
        "status": status,
        "values": f"{R_12V_Reading}Ohms"
    })
    print("             ++Disconnect RED terminal of DMM from CTS\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect RED terminal of DMM to IC1 Pin 16 (use a pin clip test lead)\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    R_VDD_Reading = float(dmm.query("READ?"))
    if R_VDD_Reading > 100.0:
        print("Vdd to ground resistance = ",R_VDD_Reading," Ohms\n")
        print("TEST PASSED\n")
        status = "PASS"
    elif R_VDD_Reading < 100.0:
        print("Vdd to ground resistance = ",R_VDD_Reading," Ohms\n")
        print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
        status = "FAIL"
    test_results.append({
        "test_name": "Test 1b: Vdd to GND Resistance Test",
        "status": status,
        "values": f"{R_VDD_Reading}Ohms"
    })
    print("--------------------")
    time.sleep(3)
    countdown_to_next_test()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ####################

    ## TEST 2 - Power Up ##
    print("----TEST 2----\n")
    print("----Power Up Test----\n")
    supply.write("OP1 0")                                            #confirm that OP is OFF
    print("             ++Confirm that DMM RED probe is connected to IC1 Pin 16\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect DMM BLACK probe to IC1 Pin 8\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect supply positive terminal to CTS\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect supply negative terminal to P2\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    dmm.write("CONF:VOLT")                                              #switch back to voltage test mode
    supply.write("V1V 12")                                            #set V1 to 12V
    supply.write("OCP1 3")                                          #set I1 OCP to 3A
    print("Supply output 1 set to 12V, 3A\n")
    supply.write("OP1 1\n")                                             #turn OP ON
    voltageReading = float(dmm.query("READ?"))                             #query current supply voltage
    loop_start_time = time.time()                                           #set loop timer starting time
    while voltageReading < 5.0:
        voltageReading = float(dmm.query("READ?"))                          #keep reading until supply definitely on
        elapsed_time = time.time() - loop_start_time
        if elapsed_time > 10:
            print("Voltage measurement timeout - probably low voltage")
            break
    print("Supply output 1 activated\n")
    print("Vdd output voltage = ", voltageReading," V\n")
    if 5.0 < voltageReading < 9.0:
        print("Vdd voltage = ",voltageReading," V\n")
        print("TEST PASSED\n")
        status = "PASS"
    else:
        print("Vdd voltage = ",voltageReading," V\n")
        print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
        status = "FAIL"
    test_results.append({
        "test_name": "Test 2: Power-up Voltage Test",
        "status": status,
        "values": f"{voltageReading}V"
    })
    print("--------------------")
    print("--------------------")
    time.sleep(3)
    countdown_to_next_test()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ####################



    ## TEST 3 - Measure clock P-P voltage ##
    print("----TEST 3----\n")
    print("----Clock Peak-to-Peak Voltage----\n")
    supply.write("OP1 0\n") 
    print("             ++Connect scope positive probe to P17\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect scope ground clip to P6\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    supply.write("OP1 1\n") 
    scope.write(":CHAN1:SCALE 2\n")
    scope.write(":TIMEBASE:MAIN:SCALE 0.05\n")
    scope.write(":TRIGGER:MAIN:TYPE EDGE\n")
    scope.write(":TRIGGER:MAIN:EDGE:SLOPE RISING\n")
    scope.write(":TRIGGER:MAIN:EDGE:SOURCE 1\n")
    scope.write(":TRIGGER:LEVEL 6\n")
    print("Scope Settings: 50ms/div     2V/div      rising edge trigger\n")
    vPp = float(scope.query(":MEAS:VPP?"))
    print("Clock Vp-p = ", vPp," Vpp\n")
    if 5.0 < vPp < 9.0:
        print("TEST PASSED\n")
        status = "PASS"
    else:
        print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
        status = "FAIL"
    print("             ++Check oscilloscope Vp-p visually, press 'Enter' when complete\n")
    input()
    test_results.append({
        "test_name": "Test 3: Vp-p Measurement",
        "status": status,
        "values": f"{vPp}V"
    })
    print("--------------------")
    print("--------------------")
    print("--------------------")
    time.sleep(3)
    countdown_to_next_test()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ####################
    
    ## TEST 4 - Measure clock Frequency ##
    print("----TEST 4----\n")
    print("----Clock Frequency Check----\n")
    scope.write(":CHAN1:SCALE 2\n")
    scope.write(":TIMEBASE:MAIN:SCALE 0.05\n")
    scope.write(":TRIGGER:MAIN:TYPE EDGE\n")
    scope.write(":TRIGGER:MAIN:EDGE:SLOPE RISING\n")
    scope.write(":TRIGGER:MAIN:EDGE:SOURCE 1\n")
    scope.write(":TRIGGER:LEVEL 6\n")
    print("Scope Settings: 50ms/div     2V/div      rising edge trigger\n")
    print("             ++Turn RV1 potentiometer fully CCW\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    lFreq = float(scope.query(":MEAS:FREQ?"))
    print("Clock Freq (Low) = ", lFreq, " Hz\n")
    if 1.0 < lFreq < 10.0:
        print("TEST PASSED\n")
        status = "PASS"
    else:
        print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
        status = "FAIL"
    test_results.append({
        "test_name": "Test 4a: Clock Freq (Low)",
        "status": status,
        "values": f"{lFreq}Hz"
    })
    print("             ++Turn RV1 potentiometer fully CW\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    scope.write(":TIMEBASE:MAIN:SCALE 0.005\n")                                  #change timebase for higher frequency
    hFreq = float(scope.query(":MEAS:FREQ?"))
    print("Clock freq (high) = ", hFreq," Hz\n")
    if 10.0 < hFreq < 200.0:
        print("TEST PASSED\n")
        status = "PASS"
    else:
        print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
        status = "FAIL"
    test_results.append({
        "test_name": "Test 4b: Clock Freq (High)",
        "status": status,
        "values": f"{hFreq}Hz"
    })
    print("             ++Visually check that frequency changes linearly when pot is swept from fully CCW to fully CW\n")
    user_input = input("             ++Type - 'y' for YES     'n' for NO    then press 'ENTER':    ")
    if user_input == 'y':
        status = "PASS"
    if user_input == 'n':
        status = "FAIL"
    test_results.append({
        "test_name": "Test 4c: Pot. Frequency Sweep (Manual)",
        "status": status,
        "values": "PASS"
    })
    print("             ++Set RV1 roughly in the middle of travel range\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    test_results.append({
        "test_name": "Test 4d: Pot. Calibrate",
        "status": status,
        "values": "COMPLETE"
    })
    print("--------------------")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    time.sleep(3)
    countdown_to_next_test()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ####################




    ## TEST 5 - Motor Direction Change Relay Check ##
    print("----TEST 5----\n")
    print("----Motor Dir. Relay Check----\n")
    funcGen.write(":FUNC SQU\n")
    funcGen.write(":FREQ +2.0\n")
    funcGen.write(":VOLT:HIGH +5.0\n")
    funcGen.write(":VOLT:LOW 0\n")
    supply.write("OP1 0\n") 
    print("             ++Connect a function generator positive output to P3\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect a function generator negative output to P4\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    supply.write("OP1 1\n") 
    print("Func. Gen. output: 2Hz square wave to relay for 5 seconds...\n")
    funcGen.write(":OUTP 1\n")
    time.sleep(5)
    funcGen.write(":OUTP 0\n")
    supply.write("OP1 0\n")
    time.sleep(5)
    print("Test is a PASS if relay is heard audibly clicking on PCB...")
    user_input = input("             ++Type - 'y' for YES     'n' for NO    then press 'ENTER':    ")
    if user_input == 'y':
        status = "PASS"
    if user_input == 'n':
        status = "FAIL"
    test_results.append({
        "test_name": "Test 5: Direction Change Relay Check",
        "status": status,
        "values": "COMPLETE"
    })
    print("--------------------")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    time.sleep(3)
    countdown_to_next_test()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ####################
    
    
    
    ## TEST 6 - Stepper Motor Functional Test ##
    print("----TEST 5----\n")
    print("----Stepper Motor Functional Test----\n")
    supply.write("OP1 0\n") 
    print("             ++Connect a jumper between P17 and P18\n")                  #ensure clock propagates to logic from the beginning of test
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Confirm that supply positive is connected to CTS\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Confirm that supply negative is connected to P2\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    print("             ++Connect a stepper motor test jig to the following outputs:\n")
    print("P8\n")
    print("P9\n")
    print("P11\n")
    print("P12\n")
    print("P13\n")
    print("P14\n")
    print("P15\n")
    print("P16\n")
    print("             ++Press 'ENTER' when complete...\n")
    input()
    supply.write("OP1 1\n")
    print("             ++Ensure that the stepper motor rotates as expected\n")
    user_input = input("             ++Type - 'y' for YES     'n' for NO    then press 'ENTER':    ")
    if user_input == 'y':
        status = "PASS"
    if user_input == 'n':
        status = "FAIL"
    test_results.append({
        "test_name": "Test 6: Stepper Functional Test",
        "status": status,
        "values": "COMPLETE"
    })
    supply.write("OP1 0\n")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    print("--------------------")
    time.sleep(3)
    countdown_to_next_test()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    ####################
    
    print("TEST COMPLETE\n")
    return test_results
    
        
def countdown_to_next_test():
    print("Tests continuing in ")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)







## SETUP ###########
#setup resource manager
rm = pyvisa.ResourceManager()
    
#connect to power supply
supply = rm.open_resource('TCPIP::10.0.0.8::9221::SOCKET')
    
#connect to scope
scope = rm.open_resource('TCPIP::10.0.0.5::INSTR')
    
#connect to func. gen.
funcGen = rm.open_resource('TCPIP::10.0.0.7::INSTR')

#connect to DMM
dmm = rm.open_resource('TCPIP::10.0.0.9::INSTR')
    
#add default string terminators for each instrument
supply.read_termination = '\n'
scope.read_termination = '\n'
funcGen.read_termination = '\n'
dmm.read_termination = '\n'

#summary of program operation
print("-------------------------------------------------------------------------------")
print("-------------------- CAR PARK STEPPER MOTOR DRIVE PCB TEST --------------------")
print("-------------------------------------------------------------------------------")
print("     This program runs a functional test on the 'Stepper Motor Drive PCB' used in Engineering Applications.")
print("     The following tests are performed:")
print("         - Unpowered power supply resistance measurements")
print("         - Power up tests (testing power supply)")
print("         - Clock pulse test (voltage and frequency)")
print("         - Relay mechanical operation check")
print("         - Stepper motor functional test in circuit")
print("\n")
print("     Equipment required (all must be LXI/VISA capable):")
print("         - Oscilloscope")
print("         - Power supply")
print("         - Digital multimeter")
print("         - Function generator")
print("         NOTE: You must replace the resource strings (e.g. 'TCPIP::x.x.x.x::INSTR') with that of your instrument if you want to")
print("         use a another piece of test equipment. Check that all SCPI commands used in this program are compatible with your instrument.")
print("\n")
print("     File structure/Pre-requisites")
print("         - DO NOT DELETE 'test_numbers.txt' file")
print("         - All test reports are saved to the relative directory")
print("\n")
print("     If an unrecoverable fault occurs on a piece of test equipment - shut this program and power-cycle the device in question.")
print("\n")
print("     PLEASE ENSURE THAT NO CONNECTIONS HAVE BEEN MADE TO THE TEST EQUIPMENT UPON BEGINNING THE TEST!")
print("     To begin the test, please press 'ENTER'")
input()

#query IDs and complete connection
print("Connection to Power Supply established")
print(supply.query("*IDN?"),"")
print("Connection to Power Supply established")
print(scope.query("*IDN?"),"")
print("Connection to Function Generator established")
print(funcGen.query("*IDN?"),"")
print("Connection to Digital Multimeter established")
print(dmm.query("*IDN?"),"\n")
    
#reset all instruments
supply.write("*RST")
scope.write("*RST")
funcGen.write("*RST")
dmm.write("*RST")
print("Full reset complete\n")
print("\n\n\n\n")
####################

create_test_report()




    
#if __name__ == "__main__":
    #main()
    
    
