import RPi.GPIO as GPIO
import time

# Define pin numbers
strobe = 7
clock = 9
data = 8

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(strobe, GPIO.OUT)
GPIO.setup(clock, GPIO.OUT)
GPIO.setup(data, GPIO.OUT)

def sendCommand(value):
    GPIO.output(strobe, GPIO.LOW)
    shiftOut(data, clock, value)
    GPIO.output(strobe, GPIO.HIGH)

def shiftOut(dataPin, clockPin, value):
    for i in range(8):
        bit = (value >> i) & 1
        GPIO.output(dataPin, bit)
        GPIO.output(clockPin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(clockPin, GPIO.LOW)

def reset():
    sendCommand(0x40)
    GPIO.output(strobe, GPIO.LOW)
    shiftOut(data, clock, 0xC0)
    for i in range(16):
        shiftOut(data, clock, 0x00)
    GPIO.output(strobe, GPIO.HIGH)

# Setup
sendCommand(0x8F)
reset()
sendCommand(0x44)

# Main loop
while True:
    for i in range(0, 16, 2):
        GPIO.output(strobe, GPIO.LOW)
        shiftOut(data, clock, 0xC1 + i)
        shiftOut(data, clock, 1)
        GPIO.output(strobe, GPIO.HIGH)
        time.sleep(0.1)
        
        GPIO.output(strobe, GPIO.LOW)
        shiftOut(data, clock, 0xC1 + i)
        shiftOut(data, clock, 0)
        GPIO.output(strobe, GPIO.HIGH)
        time.sleep(0.01)

# Cleanup
GPIO.cleanup()
