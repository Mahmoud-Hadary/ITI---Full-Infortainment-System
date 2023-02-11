import serial
import time

ser = serial.Serial('/dev/ttyS0', 9600)

# if you want to store heart rate data in excel file in example use this
heart_rate_readings = []

while True:
    reading = ser.readline().decode().strip()
    heart_rate = int(reading)
    heart_rate_readings.append(heart_rate)
    print("Heart rate: {} bpm".format(heart_rate))
    #time you need between readings
    time.sleep(1) # pause for 1 second between readings
