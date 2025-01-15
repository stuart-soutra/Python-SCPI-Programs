#----------Engineering Applications Module - Car Park Stepper Motor Driver Board PCB Test----------#
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

import csv
import time
import pyvisa

def main():
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
    
    
    
    
    while True:

        ## TEST 1 - Check +12V Resistance ##
        print("----TEST 1----\n")
        print("----Check Power Supply Resistances----\n")
        print("             ++Connect RED terminal of DMM to P1 and BLACK to P2 on the DUT\n")     
        print("             ++Press 'ENTER' when complete...\n")
        input()
        dmm.write("CONF:RES")                                           #set DMM to R mode
        resistanceReading = float(dmm.query("READ?"))
        if resistanceReading > 100.0:
            print("+12V to ground resistance = ",resistanceReading,"\n")
            print("TEST PASSED\n")
        elif resistanceReading < 100.0:
            print("+12V to ground resistance = ",resistanceReading,"\n")
            print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
            break
        print("             ++Disconnect RED terminal of DMM from P1\n")
        print("             ++Press 'ENTER' when complete...\n")
        input()
        print("             ++Connect RED terminal of DMM to IC1 Pin 16 (use a pin clip test lead)\n")
        print("             ++Press 'ENTER' when complete...\n")
        input()
        resistanceReading = float(dmm.query("READ?"))
        if resistanceReading > 100.0:
            print("Vdd to ground resistance = ",resistanceReading," Ohms\n")
            print("TEST PASSED\n")
        elif resistanceReading < 100.0:
            print("Vdd to ground resistance = ",resistanceReading," Ohms\n")
            print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
            break
        print("--------------------")
        print("\n\n\n\n")
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
        while voltageReading < 5.0:
            voltageReading = float(dmm.query("READ?"))                          #keep reading until supply definitely on
        print("Supply output 1 activated\n")
        
        print("Vdd output voltage = ", voltageReading," V\n")
        if 5.0 < voltageReading < 9.0:
            print("Vdd voltage = ",voltageReading," V\n")
            print("TEST PASSED\n")
        else:
            print("Vdd voltage = ",voltageReading," V\n")
            print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
            break
        print("--------------------")
        print("--------------------")
        print("\n\n\n\n")
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
        else:
            print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
            break
        print("             ++Check oscilloscope Vp-p visually, press 'Enter' when complete\n")
        input()
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("\n\n\n\n")
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
        freq = float(scope.query(":MEAS:FREQ?"))
        print("Clock Freq (Low) = ", freq, " Hz\n")
        if 1.0 < freq < 10.0:
            print("TEST PASSED\n")
        else:
            print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
            break
        print("             ++Turn RV1 potentiometer fully CW\n")
        print("             ++Press 'ENTER' when complete...\n")
        input()
        scope.write(":TIMEBASE:MAIN:SCALE 0.005\n")                                  #change timebase for higher frequency
        freq = float(scope.query(":MEAS:FREQ?"))
        print("Clock freq (high) = ", freq," Hz\n")
        if 10.0 < freq < 200.0:
            print("TEST PASSED\n")
        else:
            print("TEST FAILED - SEE REPORT FOR MORE DETAILS")
            break
        print("             ++Visually check that frequency changes linearly when pot is swept from fully CCW to fully CW\n")
        print("             ++Press 'ENTER' when complete...\n")
        input()
        print("             ++Set RV1 roughly in the middle of travel range\n")
        print("             ++Press 'ENTER' when complete...\n")
        input()
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("\n\n\n\n")
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
        print("             ++If TEST PASSED, press 'ENTER'")
        input()
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("\n\n\n\n")
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
        print("             ++If test passed, press 'ENTER'")
        input()
        supply.write("OP1 0\n")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("--------------------")
        print("\n\n\n\n")
        ####################
        
        print("TEST COMPLETE - REPORT AVAILABLE IN RELATIVE FOLDER\n")
        print("Press 'ENTER' to exit...\n")
        input()
        break
        
    
if __name__ == "__main__":
    main()
    
    
