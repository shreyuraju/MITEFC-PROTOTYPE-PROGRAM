import serial

p=serial.Serial('/dev/ttyAMA0',9600, timeout=5)
def eT(text):
    return text.encode('utf-8')

NFCUSN="1TE23ST001"
mealsAmt="Meals : Rs. "+str(50)
date="2023-03-08 11:15"
utr="UTR :"+"1TE23ST00120230308103843"



# Print a horizontal line.
#p.write(b'-'*32 + b'\n')  # Print a line of 32 dashes.

# Define some commands to send to the printer.
RIGHT_JUSTIFY = b'\x1B\x61\x02'  # Right-justify the text.
RESET_JUSTIFY = b'\x1B\x61\x00'  # Reset the text justification.
CENTER_JUSTIFY = b'\x1B\x61\x01' # Define the command to center justify the text.


# Define the command to increase the font size.
LARGE_FONT = b'\x1B\x21\x34'

# Define some commands to send to the printer.
RESET = b'\x1B\x40'  # Reset the printer.
SET_FONT_DOUBLE_HEIGHT = b'\x1B\x21\x01'  # Set the font size to double height.
SET_FONT_NORMAL = b'\x1B\x21\x00'  # Set the font size back to normal.
BOLD_ON = b'\x1B\x45\x02'  # Turn bold font on.
BOLD_OFF = b'\x1B\x45\x00'  # Turn bold font off.
FEED_PAPER_CUT = b'\n\n\n\x1D\x56\x41\x30'  # Feed three lines and cut the paper.

#PRINTING FORMAT
p.write(b'\n\n')
p.write(b'\x1B\x61\x01') # Define the command to center justify the text.
p.write(b'\x1B\x21\x34') #increase the font size.
p.write(b'\x1B\x45\x02') # Turn bold font on.
p.write(eT("MITE"))
p.write(b'\n')

#
token ="TOKEN NO :"+str(0)+str(0)+str(1)
p.write(b'\x1B\x21\x10') #Set the font size
p.write(b'\x1B\x45\x02') # Turn bold font on.
p.write(eT(token))

#
p.write(b'\n')
p.write(b'\x1B\x61\x01') #center justify 
p.write(b'\x1B\x21\x00') # Set the font size
p.write(b'\x1B\x45\x02') # Turn bold font on.
p.write(eT(utr))

#
p.write(b'\n')
p.write(b'\x1B\x61\x01') #center justify 
line2 = date+"  "+NFCUSN
p.write(eT(line2))

#
p.write(b'\n')
p.write(b'\x1B\x61\x01') #center justify 
p.write(b'\x1B\x21\x34') #increase the font size
p.write(b'\x1B\x21\x10')
p.write(eT(mealsAmt))

# Feed the paper and cut it.
p.write(b'\n\n\n\n\x1D\x56\x41\x30') # Feed three lines and cut the paper.

p.close()
