# region TASK 1
# CREATE SMART-PLUG CLASS
class SmartPlug:

    def __init__(self, consumptionRate):
        self.switchedOn = False
        if str(consumptionRate).isnumeric() and 0 < int(consumptionRate) <= 150:
            self.consumptionRate = consumptionRate
        else:
            raise ValueError("MUST be a NUMBER between 0-150")

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        return self.switchedOn

    def getConsumptionRate(self):
        return self.consumptionRate

    def setConsumptionRate(self, consumptionRate):
        try:
            if int(consumptionRate) in range(0, 151):
                self.consumptionRate = consumptionRate
            else:
                print("It must be a number from 0-150!")
        except ValueError:
            print("It must be a number!")

    def __str__(self):
        output = f"A SmartPlug with a consumption rate of {self.getConsumptionRate()}"
        return output


# TEST SMART-PLUG CLASS
def testSmartPlug():
    print("\nTEST 1\n")
    mySmartPlug = SmartPlug(45)
    mySmartPlug.toggleSwitch()
    print(mySmartPlug.getSwitchedOn())
    print(mySmartPlug.getConsumptionRate())
    mySmartPlug.setConsumptionRate(120)
    print(mySmartPlug.getConsumptionRate())
    print(mySmartPlug)


testSmartPlug()


# endregion TASK 1
# region TASK 2
# CREATE CUSTOM DEVICE
class SmartWashingMachine:
    options = {
        "1": "Daily Wash",
        "2": "Quick Wash",
        "3": "Eco"
    }

    def __init__(self):
        self.switchedOn = False
        self.option = self.options["1"]

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        return self.switchedOn

    def getOption(self):
        return self.option

    def setOption(self, option):
        if option not in self.options:
            valid_options = "\n".join([f"{k}: {v}" for k, v in self.options.items()])
            print(f"This is an invalid option!\n"
                  f"Please choose a number between the following options:\n"
                  f"{valid_options}\n")
            return
        self.option = self.options[option]

    def __str__(self):
        onOrOff = "On" if self.getSwitchedOn() else "Off"
        output = f"A Smart Washing Machine, with the setting {self.getOption()}, currently {onOrOff}"
        return output


# TEST CUSTOM DEVICE
def testSmartWashingMachine():
    print("\nTEST 2\n")
    mySmartWashingMachine = SmartWashingMachine()
    mySmartWashingMachine.toggleSwitch()
    print(mySmartWashingMachine.getSwitchedOn())
    print(mySmartWashingMachine.getOption())
    mySmartWashingMachine.setOption("3")
    print(mySmartWashingMachine.getOption())
    print(mySmartWashingMachine)


testSmartWashingMachine()


# endregion TASK 2
# region TASK 3
# CREATE SMART_HOME CLASS
class SmartHome:

    def __init__(self):
        self.devices = []

    def getDevices(self):
        return [device for device in self.devices]

    def getDeviceAt(self, index):
        try:
            return self.devices[index]
        except IndexError:
            print(f"Index {index} is outside the valid range. Please provide a valid index.")

    def removeDeviceAt(self, index):
        try:
            self.devices.pop(index)
        except IndexError:
            print(f"Index {index} is outside the valid range. Please provide a valid index.")

    def addDevice(self, device):
        self.devices.append(device)

    def toggleSwitch(self, index):
        try:
            self.devices[index].toggleSwitch()
        except IndexError:
            print(f"Index {index} is outside the valid range. Please provide a valid index.")

    def turnOnAll(self):
        for device in self.devices:
            if not device.getSwitchedOn():
                device.toggleSwitch()

    def turnOffAll(self):
        for device in self.devices:
            if device.getSwitchedOn():
                device.toggleSwitch()

    def __str__(self):
        output = f"This SmartHome has the following devices:\n"
        for device in self.devices:
            output += str(device) + "\n"
        return output


# TEST SMART_HOME CLASS
def testSmartHome():
    print("\nTEST 3\n")
    mySmartHome = SmartHome()
    mySmartPlug1 = SmartPlug(45)
    mySmartPlug2 = SmartPlug(45)
    mySmartWashingMachine = SmartWashingMachine()

    mySmartPlug1.toggleSwitch()
    mySmartPlug1.setConsumptionRate(150)
    mySmartPlug2.setConsumptionRate(25)
    mySmartWashingMachine.setOption("3")

    mySmartHome.addDevice(mySmartPlug1)
    mySmartHome.addDevice(mySmartPlug2)
    mySmartHome.addDevice(mySmartWashingMachine)

    mySmartHome.toggleSwitch(1)
    print(mySmartHome)
    mySmartHome.turnOnAll()
    print(mySmartHome)
    mySmartHome.removeDeviceAt(0)
    print(mySmartHome)


testSmartHome()
# endregion TASK 3
