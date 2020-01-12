import serial
from serial.tools import list_ports

# An interface script for reading light sensor data from Circuit Playground Express
# Be sure CPE is running the firmware from the accelerometer folder

# TODO: create a class for reading from the arduino?


def get_data(cpe):
    """collect data from ser_dev
    single value of z-accel"""

    cpe.reset_input_buffer()
    next = cpe.readline()
    light = (float(next.decode("ascii"))) # TODO wrap in TRY?

    return light

def main():
    try:
        for port in list_ports.comports():
            if port.description == "Circuit Playground Express":
                cpe_device = port.device
                print("Adafruit board found: " + cpe_device)

        cpe = serial.Serial(cpe_device)
    except Exception as e:
        print(e)
        print("Unable to locate Circuit Playground Express")
        raise

    while(True):
        print(get_data(cpe))

if __name__ == '__main__':
    main()
