# Python SCPI Programs
This project contains a number of Python-based SCPI programs that I have written to use with various pieces 
of LXI/GPIB/RS232/USB enabled electronic test equipment.

The setup and running of the programs has been tested on Windows 10 and Ubuntu 24.04.1.

Some of these programs are pretty generic and can easily be ported to be used on other pieces of test equipment with similar 
functionalities, by modifying the SCPI commands used.

The programs mostly cover single-parameter measurement (current/voltage etc..), however there are also multi-instrument 
programs that perform full custom tests.

I struggled to find full examples for SCPI programs when I initially started making automated tests, so hopefully these can 
be of some use if you are starting out.

## Prerequisites
- NI-VISA drivers install
- Py-VISA install
- Python install (3.6+)

## Hardware Setup
1. Connect your instrument via. your desired interface to the PC
2. Install any drivers required for your instrument
3. Setup your instrument (on the instrument itself) for the type of communication protocol you are using -
note any details (IP addresses etc...)

## PyVISA/NI-VISA Setup
1. Go to the [PyVISA Landing Page](https://pyvisa.readthedocs.io/en/latest)  (use as reference)
2. Install latest version of Python
3. Install latest [NI-VISA instrument drivers](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#521671)  (more infor for Ubuntu install can be found in
'VISA-Instrument-Setup-Steps-and-Issues.docx'
5. Run the following commands (in Windows):
```cmd
py -m pip install -U pyvisa
py -m pip install -U pyvisa-py
```
or the following in Ubuntu:
```bash
sudo apt install python3-pyvisa
```
5. Test setup by opening Python and running the following commands sequentially (also available on the [PyVISA landing page](https://pyvisa.readthedocs.io/en/latest):
```python
import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()                               # outputs VISA instrument ID - will be different depending on whether you use GPIB/USB/LAN etc...    (example: GPIB::12::INSTR)
instr = rm.open_resource('*YOUR INSTRUMENT ID*')  # replace *YOUR INSTRUMENT ID* with instrument ID from above output
print(instr.query("*IDN?"))                       # if this returns the manufacturer details from your instrument, you're good to go
```
## Porting SCPI Program to Alternative Instrument
In theory, you should be able to using any SCPI programs on another similar instrument as long as it has similar enough functionality.
So you could port a voltage measurement program written for a Keithley DMM6500 DMM to a Keysight 34460A as long as it used similar functionality.

In the example of the above instruments, you could not port a digitizing voltage measurement program from the Keithley to the Keysight DMM, 
as there is no digitizing function on the Keysight 34460A.

To port code to another instrument, perform the following steps in whichever program you are modifying:
1. Replace the VISA instrument address of the current instrument with that of the new instrument. For example:
```python
dmm = rm.open_resource('USB0::0x05E6::0x6500::04536806::INSTR')  # Replace USB0::0x05E6::0x6500::04536806::INSTR with your instrument's VISA address
```
2. Ensure that any SCPI commands sent to the instrument are available on the replacement instrument
(see your instruments' user manual for a list of SCPI commands).

## Instruments Currently Supported
I have written some form of program for the following list of instruments:
- Keithley DMM6500 Digital Multimeter
- Keysight E4980A LCR Meter
- Tektronix TBS1072B Oscilloscope
- Agilent/Keysight DSO-X 2004A Oscilloscope
- Keysight EDU33212A Function Generator
- Keysight 34460A Digital Multimeter
- AimTTI CPX400DP Dual DC Power Supply

## Recommendations
- If using a number of instruments via. LAN/LXI, change all of the IP addresses to static (e.g. 10.0.0.x) and keep track of these.
I have tried to keep any multi-instrument programs to a 10.0.0.x subnet, but you will have to modify these in each program.
- Although most manufacturers offer SCPI command reference manuals for their products, there can be some differences
in the way the each instrument interpates certain commands, so switching manufacturer may require some further debugging when
porting commands
- Default to specifying a termination character when sending SCPI query messages. Although some instruments do not require it,
I have had issues with some when I have not specified this (I'm looking at you AimTTI!!).
PyVISA allows this definition using the following command:
```python
my_instr.read_termination = '\n'
```

## Contribution
I have limited this repo to pull only. Feel free to download and use these programs for your own use.
