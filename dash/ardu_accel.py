import serial
from serial.tools import list_ports

# rewrite this to read the arduino data

# create a class for reading from the arduino?


def get_data(cpe):
    """collect data from ser_dev
    single value of z-accel"""
    az = []
    for i in range(10):
        cpe.reset_input_buffer()
        next = cpe.readline()
        az.append(float(next.decode("ascii"))) # TODO wrap in TRY?
        #print(az)

    return [{'x': list(range(10)),
             'y': az,
             'type': 'line',
             'showscale': False,
             'colorscale': [[0, 'rgba(255, 255, 255,0)'], [1, 'rgba(0,0,255,1)']]}]

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
        get_data(cpe)

if __name__ == '__main__':
    main()
