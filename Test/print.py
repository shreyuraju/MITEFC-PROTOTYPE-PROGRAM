import serial
import time

p=serial.Serial('/dev/ttyAMA0',9600, timeout=5)

def eT(text):
    return text.encode('utf-8')



# Define some commands to send to the printer.
RIGHT_JUSTIFY = b'\x1B\x61\x02'  # Right-justify the text.
RESET_JUSTIFY = b'\x1B\x61\x00'  # Reset the text justification.
# Define the command to center justify the text.
CENTER_JUSTIFY = b'\x1B\x61\x01'

# Define the command to increase the font size.
LARGE_FONT = b'\x1B\x21\x10'

# Define some commands to send to the printer.
RESET = b'\x1B\x40'  # Reset the printer.
SET_FONT_DOUBLE_HEIGHT = b'\x1B\x21\x01'  # Set the font size to double height.
SET_FONT_NORMAL = b'\x1B\x21\x00'  # Set the font size back to normal.
BOLD_ON = b'\x1B\x45\x01'  # Turn bold font on.
BOLD_OFF = b'\x1B\x45\x00'  # Turn bold font off.
FEED_PAPER_CUT = b'\n\n\n\x1D\x56\x41\x30'  # Feed three lines and cut the paper.

# Define some text to print.
total = 10
price = 15.99
line = f'Total: ${price*total:.2f}'

def pprint():
    # Send some text to the printer.
    p.write(b'\x1B\x40') # Reset the printer.
    p.write(b'\x1B\x21\x02') # Set the font size to double height.
    p.write(b'MY EVENT TICKET\n') # Print the title of the ticket.
    p.write(b'\x1B\x21\x00') # Set the font size back to normal.
    p.write(b'Name: John Smith\n') # Print the attendee's name.
    p.write(b'Date: March 8, 2023\n') # Print the date.

    # Print a horizontal line.
    p.write(b'-'*32 + b'\n')  # Print a line of 32 dashes.

    # Feed the paper and cut it.
    p.write(b'\n\n\n\x1D\x56\x41\x30') # Feed three lines and cut the paper.

    p.write(eT("HELLO WORLD"))
    print(1)
#p.close()

while True:
    pprint()
    time.sleep(3)
