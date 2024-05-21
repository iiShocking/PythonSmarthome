# region INHERITANCE
# CREATE SMART-DEVICE CLASS
class SmartDevice:

    def __init__(self, name):
        self.switchedOn = False
        self.name = name
        self.onSchedule = "ON"
        self.offSchedule = "OFF"

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        return self.switchedOn

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setOnSchedule(self, time):
        if time != "" and time != "ON" and time != self.offSchedule:
            self.onSchedule = time

    def setOffSchedule(self, time):
        if time != "" and time != "OFF" and time != self.onSchedule:
            self.offSchedule = time

    def getOnSchedule(self):
        return self.onSchedule

    def getOffSchedule(self):
        return self.offSchedule

    def getOnOrOff(self):
        onOrOff = "On" if self.getSwitchedOn() else "Off"
        return onOrOff

    def __str__(self):
        output = f"A Smart Device named {self.getName()}, currently switched"
        return output


class SmartPlug(SmartDevice):

    def __init__(self, name, consumptionRate):
        super().__init__(name)
        self.consumptionRate = consumptionRate

    def setConsumptionRate(self, consumptionRate):
        if 0 <= int(consumptionRate) <= 150:
            self.consumptionRate = int(consumptionRate)
        else:
            print("That consumption rate is invalid!\nIt must be between 0-150")

    def getConsumptionRate(self):
        return self.consumptionRate

    def __str__(self):
        output = (f"A SmartPlug with a consumption rate of {self.getConsumptionRate()},"
                  f"currently switched {self.getOnOrOff()}")
        return output


# TEST SMART-PLUG CLASS
def testSmartPlug():
    mySmartPlug = SmartPlug("Plug", 45)
    mySmartPlug.toggleSwitch()
    print(mySmartPlug.getSwitchedOn())
    print(mySmartPlug.getConsumptionRate())
    mySmartPlug.setConsumptionRate(120)
    print(mySmartPlug.getConsumptionRate())
    print(mySmartPlug)


testSmartPlug()


# CREATE CUSTOM DEVICE
def getOptionKey(value):
    if value == "Daily Wash":
        return "1"
    elif value == "Quick Wash":
        return "2"
    elif value == "Eco":
        return "3"
    else:
        return


class SmartWashingMachine(SmartDevice):
    options = {
        "1": "Daily Wash",
        "2": "Quick Wash",
        "3": "Eco"
    }

    def __init__(self, name):
        super().__init__(name)
        self.option = self.options["1"]

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
    mySmartWashingMachine = SmartWashingMachine("Washing Machine")
    mySmartWashingMachine.toggleSwitch()
    print(mySmartWashingMachine.getSwitchedOn())
    print(mySmartWashingMachine.getOption())
    mySmartWashingMachine.setOption("3")
    print(mySmartWashingMachine.getOption())
    print(mySmartWashingMachine)


testSmartWashingMachine()


# endregion INHERITANCE
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

    def saveDevicesToFile(self, file):
        linesToWrite = []
        writeFile = open(file, "w+")
        for device in self.devices:
            if isinstance(device, SmartWashingMachine):
                line = (f"Washing Machine,{device.getName()},{getOptionKey(device.getOption())},"
                        f"{device.getOnSchedule()},{device.getOffSchedule()}")
            else:
                line = (f"Smart Plug,{device.getName()},{device.getConsumptionRate()},"
                        f"{device.getOnSchedule()},{device.getOffSchedule()}")
            linesToWrite.append(line)
            for line in linesToWrite:
                writeFile.write(f"{line}\n")

    def collectDevicesFromFile(self, file):
        self.devices.clear()
        file = open(file, "r")
        devices = file.read().splitlines()
        for device in devices:
            deviceDetails = device.split(",")
            if deviceDetails[0] == "Washing Machine":
                deviceToBeMade = SmartWashingMachine(deviceDetails[1])
                deviceToBeMade.setOption(deviceDetails[2])
            elif deviceDetails[0] == "Smart Plug":
                deviceToBeMade = SmartPlug(deviceDetails[1], deviceDetails[2])
            else:
                print("NOTHING HERE!")
                break
            deviceToBeMade.setOnSchedule(deviceDetails[3])
            deviceToBeMade.setOffSchedule(deviceDetails[4])
            self.addDevice(deviceToBeMade)
        file.close()

    def __str__(self):
        output = f"This SmartHome has the following devices:\n"
        for device in self.devices:
            output += str(device) + "\n"
        return output


# TEST SMART_HOME CLASS
def testSmartHome():
    mySmartHome = SmartHome()
    mySmartPlug1 = SmartPlug("Plug", 45)
    mySmartPlug2 = SmartPlug("Plug", 45)
    mySmartWashingMachine = SmartWashingMachine("Washing Machine")
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


testSmartHome()
