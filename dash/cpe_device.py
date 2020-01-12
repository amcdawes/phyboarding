# TODO: allow option of return as plotly object or raw data.

import serial
from serial.tools import list_ports

class CPEdevice(object):
    def __init__(self):
        try:
            for port in list_ports.comports():
                if port.description == "Circuit Playground Express":
                    cpe_device = port.device
                    print("Adafruit board found: " + cpe_device)

            self.cpe = serial.Serial(cpe_device)
        except Exception as e:
            print(e)
            print("Unable to locate Circuit Playground Express")
            raise
            # TODO display this warning in the app and handle it better

    def get_data(self):
        """collect data from CPE
        one single value from latest serial line"""

        self.cpe.reset_input_buffer()
        next = self.cpe.readline()
        value = (float(next.decode("ascii"))) # TODO wrap in TRY?

        return value

    def get_data_array(self, n=10):
        """collect data from CPE
        n values from single-value-per-line serial output"""
        az = []
        for i in range(n):
            self.cpe.reset_input_buffer()
            next = self.cpe.readline()
            az.append(float(next.decode("ascii"))) # TODO wrap in TRY?
            #print(az)

        # TODO: change this to just return the list?
        return [{'x': list(range(10)),
                 'y': az,
                 'type': 'line',
                 'showscale': False,
                 'colorscale': [[0, 'rgba(255, 255, 255,0)'], [1, 'rgba(0,0,255,1)']]}]
