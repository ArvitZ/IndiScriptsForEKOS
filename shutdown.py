#!/home/stellarmate/venvs/bin/python

"""
This scipt is run at startup of a capture session to:

1. move to preset 2 auto focus position 
2. uncap the dust cover
3. cool the camera to -5 degrees

"""

from indiClientAZ import *

TARGET_FOCUS_POS = 0

indiAZ = IndiClient()
indiAZ.connectLocalServer()

# connect to the auto focuser
aaf = indiAZ.getDevice("ToupTek AAF 2")
# connect to the Excalibur device
excalibur = indiAZ.getDevice("RBF Excalibur")

# unpark cap
cap_parked = excalibur.getSwitch("CAP_PARK")
indiAZ.logger.info(f"AZ --- Current state for CAP_Park: {cap_parked.getState()}")
cap_parked[0].setState(PyIndi.ISS_ON)
cap_parked[1].setState(PyIndi.ISS_OFF)
indiAZ.logger.info(f"AZ --- Set CAP_Park to {cap_parked.getState()}")

# goto preset 2 auto focus position
aaf_goto = aaf.getNumber("ABS_FOCUS_POSITION")
indiAZ.logger.info(f"AZ --- Current state for AAF Focus Pos: {aaf_goto[0].getValue()}")
aaf_goto[0].setValue(TARGET_FOCUS_POS)
indiAZ.logger.info(f"AZ --- Set AAF Goto to {aaf_goto[0].getValue()}")

# send the new states to the Excalibur device
indiAZ.sendNewNumber(aaf_goto)
indiAZ.sendNewSwitch(cap_parked)

# wait for focuser to move to position and cap to unpark
time.sleep(5)