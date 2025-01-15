Description:	Program monitors thermocouple temperature (using DMM in temp mode). For every increase in temperature from 30 Degrees Centigrade to 600 Degrees Centigrade, the LCR meter takes a swept impedance measurement (Cp-Rp)
		across the following frequencies: 20Hz, 100Hz, 1kHz, 10kHz, 100kHz, 1MHZ, 2MHz.
		Each sweep measurement and the corresponding temperaute is output to a .csv file.

Default instrument 1:	Keysight E4980A LCR Meter
Default instrument 2:	Keithley DMM6500 DMM





Setup:
- Setup LAN communication to device
- Install NI-VISA
- Install Python
- Install Pyvisa
	https://stackoverflow.com/questions/36835341/pip-is-not-recognized


