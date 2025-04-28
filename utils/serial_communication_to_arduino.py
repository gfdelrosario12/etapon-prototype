import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()
print("Serial communication started")

#Sends Signal To Arduino
def sendSignalToArduino(data):
    ser.write(str(data).encode('utf-8'))

def closeSerialCommunication():
    ser.close()