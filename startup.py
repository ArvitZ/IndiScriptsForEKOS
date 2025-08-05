#!/home/stellarmate/venvs/bin/python

"""
This scipt is run at startup of a capture session to:

1. move to preset 2 auto focus position 
2. uncap the dust cover
3. cool the camera to -5 degrees

"""

from indiClientAZ import *

indiAZ = IndiClient()
indiAZ.connectLocalServer()

# connect to the auto focuser
aaf = indiAZ.getDevice("ToupTek AAF 2")
# connect to the Excalibur device
excalibur = indiAZ.getDevice("RBF Excalibur")

# unpark cap
cap_parked = excalibur.getSwitch("CAP_PARK")
indiAZ.logger.info(f"AZ --- Current state for CAP_Park: {cap_parked.getState()}")
cap_parked[0].setState(PyIndi.ISS_OFF)
cap_parked[1].setState(PyIndi.ISS_ON)
indiAZ.logger.info(f"AZ --- Set CAP_Park to {cap_parked.getState()}")

# goto preset 2 auto focus position
aaf_goto = aaf.getSwitch("Goto")
indiAZ.logger.info(f"AZ --- Current state for AAF Goto: {aaf_goto.getState()}")
aaf_goto[1].setState(PyIndi.ISS_ON)
indiAZ.logger.info(f"AZ --- Set AAF Goto to {aaf_goto.getState()}")

# send the new states to the Excalibur device
indiAZ.sendNewSwitch(aaf_goto)
indiAZ.sendNewSwitch(cap_parked)

# wait for focuser to move to position and cap to unpark
time.sleep(5)