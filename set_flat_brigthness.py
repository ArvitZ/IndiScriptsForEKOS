from indiClientAZ import *


indiAZ = IndiClient()
indiAZ.connectLocalServer()

# connect to the Excalibur device
excalibur = indiAZ.getDevice("RBF Excalibur")

# park cap
cap_parked = excalibur.getSwitch("CAP_PARK")
indiAZ.logger.info(f"AZ --- Current state for CAP_Park: {cap_parked.getState()}")
cap_parked.setState(1)
indiAZ.logger.info(f"AZ --- Set CAP_Park to {cap_parked.getState()}")

# set flat lights on
lights_off = excalibur.getSwitch("FLAT_LIGHT_CONTROL")
indiAZ.logger.info(f"AZ --- Current state for Flat Lights: {lights_off.getState()}")
lights_off.setState(0)
indiAZ.logger.info(f"AZ --- Set Flat Lights to {lights_off.getState()}")

indiAZ.sendNewSwitch(cap_parked)
indiAZ.sendNewSwitch(lights_off)

for i in range(5):

    # set brightness for flat lights
    brightness = excalibur.getNumber("FLAT_LIGHT_INTENSITY")
    indiAZ.logger.info(f"AZ --- Current brightness for Flat Lights: {brightness.getValue()}")
    brightness.setValue(1000)
    indiAZ.logger.info(f"AZ --- Set Flat Lights brightness to {brightness.getValue()}")

    indiAZ.sendNewNumber(brightness)

    time.sleep(5)

    # set brightness for flat lights
    brightness = excalibur.getNumber("FLAT_LIGHT_INTENSITY")
    indiAZ.logger.info(f"AZ --- Current brightness for Flat Lights: {brightness.getValue()}")
    brightness.setValue(100)
    indiAZ.logger.info(f"AZ --- Set Flat Lights brightness to {brightness.getValue()}")

    indiAZ.sendNewNumber(brightness)


# unpark cap
cap_parked.setState(0)
indiAZ.sendNewSwitch(cap_parked)

