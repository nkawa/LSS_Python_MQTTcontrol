

# Import LSS library
from vendor import lss 
from vendor import lss_const as lssc

CST_LSS_Port = "COM10"				# For windows platforms
CST_LSS_Baud = lssc.LSS_DefaultBaud

# Create and open a serial port
lss.initBus(CST_LSS_Port, CST_LSS_Baud)

lss.LSS(1).move(0);
lss.LSS(2).move(0);
lss.LSS(3).move(-900);
lss.LSS(4).move(0);
