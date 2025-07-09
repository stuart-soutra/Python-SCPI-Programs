#----------Impedance vs. Temperature Measurement----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 15/01/2025
#   - Version: 1.0
#   - Description: - Program monitors thermocouple temperature (using DMM in temp mode). 
#                  - A lab oven with controllable temperature profile was used to ramp up temperature.
#                  - For every increase in temperature from 30 Degrees Centigrade to 600 Degrees Centigrade, the LCR meter takes a swept impedance measurement (Cp-Rp)
#                    across the following frequencies: 20Hz, 100Hz, 1kHz, 10kHz, 100kHz, 1MHZ, 2MHz.
#                  - Each sweep measurement and the corresponding temperature is output to a .csv file.

#                   Default instrument 1: Keysight E4980A LCR Meter
#                   Default instrument 2: Keithley DMM6500 DMM

#                   Hardware setup:
#                       - Connect measurement default probe to LCR meter front panel inputs
#                       - Connect K-Type thermocouple to DMM + and - (or corresponding thermocouple inputs)
#                       - Connect LCR probe to sample
#                       - Attach K-Type thermocouple to sample
#                       - If using oven - custom fixture may be required to connect LCR probe and thermocouple to sample


import pyvisa
import csv
import time
import math

# Connect to the Keysight E4980 LCR Meter
rm = pyvisa.ResourceManager()
print("Pyvisa resource opened...")
lcr = rm.open_resource('TCPIP0::10.0.0.11::INSTR')    # Open LCR Meter
print("Connected to LCR meter...")
dmm = rm.open_resource('TCPIP0::10.0.0.10::INSTR')         # Open DMM
print("Connected to DMM...")

# Create CSV file for logging
filePath = "/home/napierats/Documents/Automated Test System/SCPI Programs/Imp-vs-temp/results.csv"

csv_file = open(filePath, "w", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Impedance vs. Temperature - impedance specified as Cp(F)-Rp(R) "])
csv_writer.writerow(["Time","Temperature (Deg C)","C_20Hz (F)","R_20Hz (Ohms)","tD_20Hz","Perm_20Hz (F/m)","C_100Hz (F)","R_100Hz (Ohms)","tD_100Hz","Perm_100Hz (F/m)","C_1kHz (F)","R_1kHz (Ohms)","tD_1kHz","Perm_1kHz (F/m)","C_10kHz (F)","R_10kHz (Ohms)","tD_10kHz","Perm_10kHz (F/m)","C_100kHz (F)","R_100kHz (Ohms)","tD_100kHz","Perm_100kHz (F/m)","C_1MHz (F)","R_1MHz (Ohms)","tD_1MHz","Perm_1MHz (F/m)","C_2MHz (F)","R_2MHz (Ohms)","tD_2MHz","Perm_2MHz (F/m)"])
print("Log file created...\n")

# Ask user to set up sample
print("Test Setup:\n")
print("1). Place sample in fixture inside oven and close lid                                (press any key when complete)\n")
input()
print("2). Confirm that thermocouple is correctly connected to wires at oven and to DMM     (press any key when complete)\n")
input()
print("3). Prepare oven heating profile - do not yet activate heating                       (press any key when complete)\n")
input()

# Ask user to input physical characteristics of capacitor/capacitive device
A = float(input("4). Enter the area of the capacitor (in square meters): "))
d = float(input("5). Enter the separation distance of the capacitor plates (in meters): "))

# Ask user to activate profile
print("6). Activate oven heating and PRESS ANY KEY IN THIS CONSOLE WITHIN 5 SECONDS\n")
input()


def freqSweep():            

    class impSpec:
        def __init__(imp_20Hz, imp_100Hz, imp_1kHz, imp_10kHz, imp_100kHz, imp_1MHz, imp_2MHz):
            impSpec.imp_20Hz = 0
            impSpec.imp_100Hz = 0
            impSpec.imp_1kHz = 0
            impSpec.imp_10kHz = 0
            impSpec.imp_100kHz = 0
            impSpec.imp_1MHz = 0
            impSpec.imp_2MHz = 0


    # Set initial frequency - 20Hz Reading
    lcr.write(":FREQ:CW 20")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_20Hz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_20Hz, "\n")

    # 100Hz Reading
    lcr.write(":FREQ:CW 100")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_100Hz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_100Hz, "\n")

    # 1kHz Reading
    lcr.write(":FREQ:CW 1000")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_1kHz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_1kHz, "\n")

    # 10kHz Reading
    lcr.write(":FREQ:CW 10000")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_10kHz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_10kHz, "\n")

    # 100kHz Reading
    lcr.write(":FREQ:CW 100000")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_100kHz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_100kHz, "\n")

    # 1MHz Reading
    lcr.write(":FREQ:CW 1000000")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_1MHz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_1MHz, "\n")

    # 2MHz Reading
    lcr.write(":FREQ:CW 2000000")
    lcr.write(":INIT")					# Re-initialise instrument to WAIT FOR TRIGGER state (see manual - page 247)
    impSpec.imp_2MHz = lcr.query("*TRG")					# Take impedance measurement
    print("Impedance:", impSpec.imp_2MHz, "\n")

    return impSpec

def splitString(impSpec):
    class floatValues:
        def __init__(float1_20Hz, float2_20Hz, float1_100Hz, float2_100Hz, float1_1kHz, float2_1kHz, float1_10kHz, float2_10kHz, float1_100kHz, float2_100kHz, float1_1MHz, float2_1MHz, float1_2MHz, float2_2MHz):
            floatValues.float1_20Hz = 0
            floatValues.float2_20Hz = 0
            floatValues.float1_100Hz = 0
            floatValues.float2_100Hz = 0
            floatValues.float1_1kHz = 0
            floatValues.float2_1kHz = 0
            floatValues.float1_10kHz = 0
            floatValues.float2_10kHz = 0
            floatValues.float1_100kHz = 0
            floatValues.float2_100kHz = 0
            floatValues.float1_1MHz = 0
            floatValues.float2_1MHz = 0
            floatValues.float1_2MHz = 0
            floatValues.float2_2MHz = 0

    # Split 20Hz string-----#
    parts_20Hz = impSpec.imp_20Hz.split(',')               # Split string by commas
    part1_20Hz = parts_20Hz[0]
    part2_20Hz = parts_20Hz[1]                             # Extract parts into seperate variables
    floatValues.float1_20Hz = float(part1_20Hz)
    floatValues.float2_20Hz = float(part2_20Hz)                        # Convert to floats
    #-----------------------#

    # Split 100Hz string----#
    parts_100Hz = impSpec.imp_100Hz.split(',')               
    part1_100Hz = parts_100Hz[0]
    part2_100Hz = parts_100Hz[1]                             
    floatValues.float1_100Hz = float(part1_100Hz)
    floatValues.float2_100Hz = float(part2_100Hz)                        
    #-----------------------#

    # Split 1kHz string-----#
    parts_1kHz = impSpec.imp_1kHz.split(',')               
    part1_1kHz = parts_1kHz[0]
    part2_1kHz = parts_1kHz[1]                             
    floatValues.float1_1kHz = float(part1_1kHz)
    floatValues.float2_1kHz = float(part2_1kHz)                        
    #-----------------------#

    # Split 10kHz string-----#
    parts_10kHz = impSpec.imp_10kHz.split(',')               
    part1_10kHz = parts_10kHz[0]
    part2_10kHz = parts_10kHz[1]                             
    floatValues.float1_10kHz = float(part1_10kHz)
    floatValues.float2_10kHz = float(part2_10kHz)                        
    #-----------------------#

    # Split 100kHz string-----#
    parts_100kHz = impSpec.imp_100kHz.split(',')               
    part1_100kHz = parts_100kHz[0]
    part2_100kHz = parts_100kHz[1]                             
    floatValues.float1_100kHz = float(part1_100kHz)
    floatValues.float2_100kHz = float(part2_100kHz)                        
    #-----------------------#

    # Split 1MHz string-----#
    parts_1MHz = impSpec.imp_1MHz.split(',')               
    part1_1MHz = parts_1MHz[0]
    part2_1MHz = parts_1MHz[1]                             
    floatValues.float1_1MHz = float(part1_1MHz)
    floatValues.float2_1MHz = float(part2_1MHz)                        
    #-----------------------#

    # Split 2MHz string-----#
    parts_2MHz = impSpec.imp_2MHz.split(',')               
    part1_2MHz = parts_2MHz[0]
    part2_2MHz = parts_2MHz[1]                             
    floatValues.float1_2MHz = float(part1_2MHz)
    floatValues.float2_2MHz = float(part2_2MHz)                        
    #-----------------------#

    return floatValues

# Calculate loss Tangent for all Impedances
def calcLossTangent(floatValues):
    
    tan_deltas = [0,0,0,0,0,0,0,0] 

    # Calculate tD for 20Hz--#
    currentC = floatValues.float1_20Hz
    currentR = floatValues.float2_20Hz
    currentOmega = 2 * math.pi * 20
    tan_deltas[1] = currentOmega * currentR * currentC
    #------------------------#

    # Calculate tD for 100Hz--#
    currentC = floatValues.float1_100Hz
    currentR = floatValues.float2_100Hz
    currentOmega = 2 * math.pi * 100
    tan_deltas[2] = currentOmega * currentR * currentC
    #------------------------#

    # Calculate tD for 1kHz--#
    currentC = floatValues.float1_1kHz
    currentR = floatValues.float2_1kHz
    currentOmega = 2 * math.pi * 1000
    tan_deltas[3] = currentOmega * currentR * currentC
    #------------------------#

    # Calculate tD for 10kHz--#
    currentC = floatValues.float1_10kHz
    currentR = floatValues.float2_10kHz
    currentOmega = 2 * math.pi * 10000
    tan_deltas[4] = currentOmega * currentR * currentC
    #------------------------#

    # Calculate tD for 100kHz--#
    currentC = floatValues.float1_100kHz
    currentR = floatValues.float2_100kHz
    currentOmega = 2 * math.pi * 100000
    tan_deltas[5] = currentOmega * currentR * currentC
    #------------------------#

    # Calculate tD for 1MHz--#
    currentC = floatValues.float1_1MHz
    currentR = floatValues.float2_1MHz
    currentOmega = 2 * math.pi * 1000000
    tan_deltas[6] = currentOmega * currentR * currentC
    #------------------------#

    # Calculate tD for 2MHz--#
    currentC = floatValues.float1_2MHz
    currentR = floatValues.float2_2MHz
    currentOmega = 2 * math.pi * 2000000
    tan_deltas[7] = currentOmega * currentR * currentC
    #------------------------#

    return tan_deltas

# Calculate Permittivity for all Impedances
def calcPermittivity(floatValues):

    epsilon_O = 8.854e-12                           # F/m
    permittivity = [0,0,0,0,0,0,0,0]

    # Calculate perm for 20Hz--#
    currentC = floatValues.float1_20Hz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[1] = currentEpsilonR * epsilon_O
    #--------------------------#

    # Calculate perm for 100Hz--#
    currentC = floatValues.float1_100Hz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[2] = currentEpsilonR * epsilon_O
    #--------------------------#    

    # Calculate perm for 1kHz--#
    currentC = floatValues.float1_1kHz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[3] = currentEpsilonR * epsilon_O
    #--------------------------#

    # Calculate perm for 10kHz--#
    currentC = floatValues.float1_10kHz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[4] = currentEpsilonR * epsilon_O
    #--------------------------#

    # Calculate perm for 100kHz--#
    currentC = floatValues.float1_100kHz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[5] = currentEpsilonR * epsilon_O
    #--------------------------#

    # Calculate perm for 1MHz--#
    currentC = floatValues.float1_1MHz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[6] = currentEpsilonR * epsilon_O
    #--------------------------#

    # Calculate perm for 2MHz--#
    currentC = floatValues.float1_2MHz  
    currentEpsilonR = currentC * d / (A * epsilon_O)
    permittivity[7] = currentEpsilonR * epsilon_O
    #--------------------------#

    return permittivity


def tempReadingConvert(temperature):
    temperature = temperature.strip()
    temperature = float(temperature)
    return temperature


def main():
    
    # Reset 
    lcr.write("*RST")
    dmm.write("*RST")

    #----LCR SETUP---#
    lcr.write(":TRIG:SOUR BUS")                                             # Set trigger function to WAIT FOR TRIGGER
    # Device waiting for trigger now
    lcr.write(":FUNC:IMP:TYPE CPRP")                                        # Setup LCR for Cp-Rp measurements
    lcr.write(":FORMAT:DATA ASCII")                                         # Change output data type to ASCII
    #----------------#

    #----DMM SETUP----#
    # Only reset required
    #-----------------#

    # Set temperature counter variable (starting temperature)
    tempCount = 30

    # print flag - zero initially
    alreadyWritten = 0

    # Error flag - zero initially
    errorFlag = 0

    while True:
        # Constantly monitor Temperature (specify Fs?)
        temperature = dmm.query(":MEAS:TEMP?")
        temperature = tempReadingConvert(temperature)
        if errorFlag == 0:
            print("Temp:", temperature, "Degrees Centigrade")

        # Once temperature reaches 30 - take reading then continuously check for whole step changes
        if tempCount <= temperature <= (tempCount+1):
            errorFlag = 0
            alreadyWritten = 0
            if alreadyWritten == 0:                                         # Only perfrom frequency sweep once per Degrees C increment
                impValues = freqSweep()
                floatValues = splitString(impValues)
                tan_deltas = calcLossTangent(floatValues)
                permittivity = calcPermittivity(floatValues)
                start_time = time.time()
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
                csv_writer.writerow([timestamp,temperature,floatValues.float1_20Hz,floatValues.float2_20Hz,tan_deltas[1],permittivity[1],floatValues.float1_100Hz,floatValues.float2_100Hz,tan_deltas[2],permittivity[2],floatValues.float1_1kHz,floatValues.float2_1kHz,tan_deltas[3],permittivity[3],floatValues.float1_10kHz,floatValues.float2_10kHz,tan_deltas[4],permittivity[4],floatValues.float1_100kHz,floatValues.float2_100kHz,tan_deltas[5],permittivity[5],floatValues.float1_1MHz,floatValues.float2_1MHz,tan_deltas[6],permittivity[6],floatValues.float1_2MHz,floatValues.float2_2MHz,tan_deltas[7],permittivity[7]])
                csv_file.flush()  # Flush buffer to ensure data is written immediately

                print("Temp:", temperature, "Degrees Centigrade")
                tempCount = tempCount+1
                alreadyWritten = 1
        
        # If reading goes out of range (temperature goes high too quickly so as to not allow imp measurement) - throw error
        if temperature > (tempCount + 1):
            errorFlag = 1
            if errorFlag == 1:
                print("ERROR - Temperature out of range! Please reduce the temperature to between", tempCount, "and",(tempCount + 1))
            
    # Close instrument connection
    lcr.close()
    rm.close()
    csv_file.close()
    input()


if __name__ == "__main__":
    main()

