#!/home/stellarmate/venvs/bin/python
from indiClientAZ import *

TARGET_BRIGHTNESS = 500  # Target brightness for flat lights


indiAZ = IndiClient()
indiAZ.connectLocalServer()

# connect to the Excalibur device
excalibur = indiAZ.getDevice("RBF Excalibur")

# park cap
cap_parked = excalibur.getSwitch("CAP_PARK")
indiAZ.logger.info(f"AZ --- Current state for CAP_Park: {cap_parked.getState()}")
cap_parked[0].setState(PyIndi.ISS_ON)
cap_parked[1].setState(PyIndi.ISS_OFF)
indiAZ.logger.info(f"AZ --- Set CAP_Park to {cap_parked.getState()}")

# set flat lights on
light_toggle = excalibur.getSwitch("FLAT_LIGHT_CONTROL")
indiAZ.logger.info(f"AZ --- Current state for Flat Lights: {light_toggle.getState()}")
light_toggle[0].setState(PyIndi.ISS_ON)
light_toggle[1].setState(PyIndi.ISS_OFF)
indiAZ.logger.info(f"AZ --- Set Flat Lights to {light_toggle.getState()}")

# send the new states to the Excalibur device
indiAZ.sendNewSwitch(cap_parked)
indiAZ.sendNewSwitch(light_toggle)

# wait for closure of the cap
time.sleep(3)

# set brightness for flat lights
brightness = excalibur.getNumber("FLAT_LIGHT_INTENSITY")
indiAZ.logger.info(f"AZ --- Current brightness for Flat Lights: {brightness[0].getValue()}")
brightness[0].setValue(TARGET_BRIGHTNESS)
indiAZ.logger.info(f"AZ --- Set Flat Lights brightness to {brightness[0].getValue()}")

indiAZ.sendNewNumber(brightness)

time.sleep(1)


