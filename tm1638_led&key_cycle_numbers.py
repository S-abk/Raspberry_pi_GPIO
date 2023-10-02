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
GPIO.setup(data, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # For reading button input

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

def readButtons():
    GPIO.output(strobe, GPIO.LOW)
    shiftOut(data, clock, 0x42)
    GPIO.output(strobe, GPIO.HIGH)
    GPIO.setup(data, GPIO.IN)
    
    buttons = 0
    for i in range(4):
        buttons |= GPIO.input(data) << i
        GPIO.output(clock, GPIO.HIGH)
        GPIO.output(clock, GPIO.LOW)
        
    GPIO.setup(data, GPIO.OUT)
    return buttons

def reset():
    sendCommand(0x40)
    GPIO.output(strobe, GPIO.LOW)
    shiftOut(data, clock, 0xC0)
    for i in range(16):
        shiftOut(data, clock, 0x00)
    GPIO.output(strobe, GPIO.HIGH)

# Initialization
sendCommand(0x8F)
reset()
sendCommand(0x44)

# Initialize display numbers
display_numbers = [0]*8

try:
    # Main loop
    while True:
        buttons = readButtons()
        for i in range(8):
            if buttons & (1 << i):
                display_numbers[i] = (display_numbers[i] + 1) % 10  # Cycle through numbers 0-9
                GPIO.output(strobe, GPIO.LOW)
                shiftOut(data, clock, 0xC0 + i*2)
                shiftOut(data, clock, display_numbers[i])
                GPIO.output(strobe, GPIO.HIGH)
        time.sleep(0.1)  # Poll buttons every 100ms
except KeyboardInterrupt:
    pass

# Cleanup
GPIO.cleanup()
