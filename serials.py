import serial

ser_port = ""
ser_baudrate = 0

def set_port(port):
    global ser_port
    ser_port = port
    return ser_port
    # set port name
    # e.g.:"COM1"
def set_baudrate(baudrate):
    global ser_baudrate
    ser_baudrate = baudrate
    return ser_baudrate
    # set baudrate
    # e.g.:"9600"

if ser_baudrate == 0:
    print("serial baudrate is not set")
    exit()

if ser_port == "":
    print("serial port is not set")
    exit()

try:
    cat_ser = serial.Serial(set_port(ser_port), set_baudrate(ser_baudrate))
except:
    print("serial port is not available")
    exit()