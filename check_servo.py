import time
import serial

# Import LSS library
from vendor import lss 
from vendor import lss_const as lssc

CST_LSS_Port = "COM10"				# For windows platforms
CST_LSS_Baud = lssc.LSS_DefaultBaud

# Create and open a serial port
lss.initBus(CST_LSS_Port, CST_LSS_Baud)

# Create LSS objects

lsss = []
for i in range(1,6):
    myLSS = lss.LSS(i)
    lsss.append(myLSS)
    pos = myLSS.getPosition()
    rpm= myLSS.getSpeedRPM()
    curr = myLSS.getCurrent()
    volt = myLSS.getVoltage()
    temp = myLSS.getTemperature()
    range = myLSS.getAngularRange()
	
	# Display the values in terminal
    print(f"{i} ---- Telemetry ----")
    print("Position  (1/10 deg) = " + str(pos));
#    print("Speed          (rpm) = " + str(rpm));
    print("Curent          (mA) = " + str(curr));
#    print("Voltage         (mV) = " + str(volt));
    print("Temperature (1/10 C) = " + str(temp));
    print("Range              = " ,range);
    
#myLSS1.reset()
#myLSS2.reset()

# Destroy objects

# Destroy the bus
lss.closeBus()
