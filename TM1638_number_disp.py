from tm1638 import TM1638

# Initialize the TM1638 (GPIO assignments are STB, CLK, DIO)
tm = TM1638(17, 18, 27)

# Display a hexadecimal number
tm.write_number(0x1234)

# Display "HELP" text
tm.write_text("HELP")

# Turn on some LEDs
tm.set_led(True, 0)  # LED at position 0
tm.set_led(True, 7)  # LED at position 7

while True:
    # Scan the buttons
    buttons = tm.read_buttons()
    
    # Check if the first button is pressed
    if (buttons & 1 << 0):
        tm.write_text("BTN 1")
        
    # Check if the second button is pressed
    if (buttons & 1 << 1):
        tm.write_text("BTN 2")

    # ... and so on for other buttons

