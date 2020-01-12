# Test script to locate and print output from Circuit Playground Express

import serial
from serial.tools import list_ports

for port in list_ports.comports():
    if port.description == "Circuit Playground Express":
        cpe_device = port.device

print(cpe_device)
cpe = serial.Serial(cpe_device)

while(True):
    line = cpe.readline()
    if(line == b'DATA\n'):
        datastring = cpe.readline()
        data = datastring.split(b' ')[:-1] # strip last newline char
        datafloats = [float(i) for i in data]
        print(datafloats)
