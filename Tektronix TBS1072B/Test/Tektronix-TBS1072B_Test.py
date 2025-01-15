#----------Tektronix TBS1072B Oscilloscope Test----------#
#
#
#
#
#   - Author: Stuart Thomas
#   - Date: 15/01/2025
#   - Version: 1.0
#   - Description: - Program tests connection to a Tektronix TBS1072B Oscilloscope

import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
scope = rm.open_resource('USB0::0x0699::0x0368::C033702::INSTR')
print(scope.query("*IDN?"))
print(scope.query("MEASUREMENT:MEAS2:TYPE?"))
input()
