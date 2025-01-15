import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
scope = rm.open_resource('USB0::0x0699::0x0368::C033702::INSTR')
print(scope.query("*IDN?"))
print(scope.query("MEASUREMENT:MEAS2:TYPE?"))
input()
