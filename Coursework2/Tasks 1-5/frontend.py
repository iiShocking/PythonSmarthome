# region IMPORTS
from tkinter import *
from tkinter import messagebox

import backend as b


# endregion IMPORTS

# region PROGRAM WIDE TKINTER FUNCTIONS
def createLabel(text, mainFrame):
    lbl = Label(mainFrame, text=text, font=("Monoton", 16), padx=10, pady=5, background="gray80")
    return lbl


def createButton(text, mainFrame, command):
    btn = Button(mainFrame, text=text, relief='solid', borderwidth=4,
                 font="Monoton", padx=15, pady=5, command=command)
    return btn


def createEntry(mainFrame):
    entry = Entry(mainFrame, relief='solid', borderwidth=2, font=("Monoton", 14))
    return entry


def addToGrid(item, column, row):
    item.grid(column=column, row=row, padx=5, pady=5, sticky="w")


def closeWindow(tkWindow):
    tkWindow.destroy()


# endregion PROGRAM WIDE TKINTER FUNCTIONS
# region UI RELATED FUNCTIONS
def getOnOrOff(device):
    onOrOff = "On" if device.getSwitchedOn() else "Off"
    return onOrOff


def retrieveLabel(device):
    if isinstance(device, b.SmartWashingMachine):
        labelText = f"Washing Machine: {getOnOrOff(device)}, Wash Mode: {device.getOption()}"
    else:
        labelText = f"Plug: {getOnOrOff(device)}, Consumption: {device.getConsumptionRate()}"
    return labelText


def setDeviceStatusFromEdit(button, device):
    device.toggleSwitch()
    button["text"] = getOnOrOff(device).upper()


# endregion UI LABEL RELATED FUNCTIONS
# region Smart Home System App
# CREATE SMART_HOME_SYSTEM CLASS FOR THE GUI
# TASK 4
class SmartHomeSystem:
    def __init__(self, SmartHome):
        self.smartHome = SmartHome
        self.win = Tk()
        self.win.title("Smart Home App")
        self.mainFrame = Frame(self.win)
        self.mainFrame.configure(background="gray80")
        self.mainFrame.grid(column=0, row=0)
        self.row = 1
        self.deviceLabels = []
        self.allDeviceWidgets = []

    # region UI Creation
    # Create the 'turn on all' and 'turn off all' buttons
    # Create the 'add device' button
    def createDefaultWidgets(self):

        btnTurnOnAll = createButton("Turn on all", self.mainFrame, command=self.turnAllOn)
        btnTurnOnAll.configure(width=20)
        addToGrid(btnTurnOnAll, 0, 0)

        btnTurnOffAll = createButton("Turn off all", self.mainFrame, command=self.turnAllOff)
        btnTurnOffAll.configure(width=20)
        btnTurnOffAll.grid(column=1, row=0, padx=5, pady=5, columnspan=2)

        # Setting the grid row to +100, so it will always stay at the very bottom
        btnAddDevice = createButton("Add Device", self.mainFrame, command=self.loadAddWindow)
        addToGrid(btnAddDevice, 0, 100)

    # Create every widget associated to one individual device and adds them to the grid
    def createDeviceWidgets(self, device):
        deviceWidgets = []
        # Retrieve all data for the label to be in the format: {Washing Machine: Off, Wash Mode: Daily Wash}
        labelText = retrieveLabel(device)

        lblDevice = createLabel(labelText, self.mainFrame)
        self.deviceLabels.append(lblDevice)
        deviceWidgets.append(lblDevice)

        btnToggleDevice = createButton("Toggle", self.mainFrame,
                                       command=lambda v=self.row: self.toggleDevice(v - 1))
        btnToggleDevice.configure(padx=20)
        deviceWidgets.append(btnToggleDevice)

        btnEditDevice = createButton("Edit", self.mainFrame,
                                     command=lambda v=self.row: self.loadEditWindow(v - 1))
        deviceWidgets.append(btnEditDevice)

        btnDeleteDevice = createButton("Delete", self.mainFrame,
                                       command=lambda v=self.row: self.deleteDevice(v - 1))
        btnDeleteDevice.configure(padx=20)
        deviceWidgets.append(btnDeleteDevice)

        # Add widgets to the grid
        for i in range(4):
            addToGrid(deviceWidgets[i], i, self.row)
            i += 1

        self.allDeviceWidgets.append(deviceWidgets)

    # Create all the widgets for every device within the Smart Home System
    def createAllDeviceWidgets(self):
        for device in self.smartHome.devices:
            self.createDeviceWidgets(device)
            self.row += 1

    # For every label on the interface, reset the text accordingly
    def updateLabels(self):
        for i in range(0, len(self.deviceLabels)):
            currentDevice = self.smartHome.getDeviceAt(i)
            labelText = retrieveLabel(currentDevice)
            self.deviceLabels[i].configure(text=labelText)

    # Reset all device related widgets
    def refreshUI(self):
        for listOfWidgets in self.allDeviceWidgets:
            for widget in listOfWidgets:
                widget.destroy()
        self.allDeviceWidgets.clear()
        for label in self.deviceLabels:
            label.destroy()
        self.deviceLabels.clear()

        self.row = 1
        self.createAllDeviceWidgets()

    # endregion UI Creation
    # region ADDING FEATURE
    def loadAddWindow(self):
        addDeviceWindow = Toplevel(self.win)
        addDeviceWindow.title("Smart Home: Add Device")
        addDeviceWindow.mainFrame = Frame(addDeviceWindow)
        addDeviceWindow.mainFrame.configure(background="gray80")
        addDeviceWindow.mainFrame.grid(column=0, row=0)

        btnAddWashingMachine = createButton("Add a Washing Machine", addDeviceWindow.mainFrame,
                                            command=lambda: self.addDevice("Washing Machine"))
        addToGrid(btnAddWashingMachine, 0, 0)

        inputConsumptionLbl = createLabel("Please input a consumption rate", addDeviceWindow.mainFrame)
        addToGrid(inputConsumptionLbl, 1, 1)

        plugConsumptionEntry = createEntry(addDeviceWindow.mainFrame)
        addToGrid(plugConsumptionEntry, 1, 2)

        btnAddPlug = createButton("Add a Plug", addDeviceWindow.mainFrame,
                                  command=lambda: self.addDevice("Plug", plugConsumptionEntry.get()))
        addToGrid(btnAddPlug, 1, 0)

        btnClose = createButton("Close", addDeviceWindow.mainFrame,
                                command=lambda: closeWindow(addDeviceWindow))
        addToGrid(btnClose, 0, 2)

    def addDevice(self, device, consumption=""):
        if device == "Washing Machine":
            newDevice = b.SmartWashingMachine()
        else:
            try:
                consumptionInt = int(consumption)
                if consumptionInt not in range(0, 151):
                    messagebox.showinfo("ERROR", "Invalid Consumption Rate!")
                    print("The rate needs to be between 0-150")
                    return
                newDevice = b.SmartPlug(consumptionInt)
            except ValueError:
                messagebox.showinfo("ERROR", "Invalid Input!")
                print("This is not a valid rate!")
                return

        self.smartHome.addDevice(newDevice)
        self.refreshUI()
        self.row += 1

    # endregion ADDING FEATURE
    # region EDITING FEATURE
    def loadEditWindow(self, index):
        editingDevice = self.smartHome.getDeviceAt(index)
        deviceName = type(editingDevice).__name__
        editWindow = Toplevel(self.win)
        editWindow.title(f"Smart Home: Edit {deviceName}")
        editWindow.mainFrame = Frame(editWindow)
        editWindow.mainFrame.configure(background="gray80")
        editWindow.mainFrame.grid(column=0, row=0)

        editTitle = createLabel(deviceName, editWindow.mainFrame)
        addToGrid(editTitle, 1, 0)

        btnClose = createButton("Close", editWindow.mainFrame, command=lambda: closeWindow(editWindow))
        addToGrid(btnClose, 2, 0)

        deviceStatusLbl = createLabel("Device Status:", editWindow.mainFrame)
        addToGrid(deviceStatusLbl, 0, 1)

        btnDeviceStatus = createButton(getOnOrOff(editingDevice).upper(), editWindow.mainFrame, "")
        btnDeviceStatus.configure(command=lambda: setDeviceStatusFromEdit(btnDeviceStatus, editingDevice))
        addToGrid(btnDeviceStatus, 1, 1)

        if deviceName == "SmartWashingMachine":
            deviceOptionLbl = createLabel("Device Setting:", editWindow.mainFrame)
        else:
            deviceOptionLbl = createLabel("Device Consumption:", editWindow.mainFrame)
        addToGrid(deviceOptionLbl, 0, 2)
        deviceOptionEntry = createEntry(editWindow.mainFrame)
        addToGrid(deviceOptionEntry, 1, 2)

        btnSaveOptions = createButton("Save Options", editWindow.mainFrame,
                                      command=lambda: self.saveDeviceOptions(editingDevice, deviceOptionEntry.get()))
        addToGrid(btnSaveOptions, 1, 3)

    def saveDeviceOptions(self, device, option):
        if isinstance(device, b.SmartWashingMachine):
            validOptions = ["1", "2", "3"]
            if option != "":
                if option in validOptions:
                    device.setOption(option)
                else:
                    messagebox.showinfo("ERROR", "Invalid Machine Setting!")
        else:
            if option != "":
                if validateConsumption(option):
                    device.setConsumptionRate(option)
                else:
                    messagebox.showinfo("ERROR", "Invalid Consumption Rate!")

        self.updateLabels()

    # endregion EDITING FEATURE
    # region BACKEND COMMUNICATIONS
    def turnAllOn(self):
        self.smartHome.turnOnAll()
        self.updateLabels()

    def turnAllOff(self):
        self.smartHome.turnOffAll()
        self.updateLabels()

    def toggleDevice(self, index):
        self.smartHome.toggleSwitch(index)
        self.updateLabels()

    def deleteDevice(self, index):
        self.smartHome.removeDeviceAt(index)
        self.refreshUI()

    # endregion BACKEND COMMUNICATIONS
    # region ON START
    # Draw all the widgets onto the TK Interface
    def createAllWidgets(self):
        self.createDefaultWidgets()
        self.createAllDeviceWidgets()

    def run(self):
        self.createAllWidgets()
        self.win.mainloop()
    # endregion ON START


# endregion Smart Home System App
# region Setting Up Home
def validateConsumption(consumption):
    try:
        consumptionInt = int(consumption)
        if 0 < consumptionInt < 151:
            return True
        else:
            print("Not between 0-150")
            return False
    except ValueError:
        print("This is not a valid input")


def askUserForConsumption():
    while True:
        try:
            consumption = input("Please enter what consumption rate this device has! (0-150)")
            if validateConsumption(consumption):
                return consumption
        except ValueError:
            print(f"\nPlease enter a number from 0-150!")


def askUserForDevice():
    availableChoices = {
        "1": "Smart Plug",
        "2": "Smart Washing Machine"
    }

    while True:
        deviceChoice = input("Please enter the number of the device you would like to connect!\n"
                             "1: Smart Plug\n"
                             "2: Smart Washing Machine\n")

        if deviceChoice in availableChoices:
            if deviceChoice == "1":
                device = b.SmartPlug(askUserForConsumption())
            else:
                device = b.SmartWashingMachine()
            return device
        else:
            print(f"\nInvalid choice! Please choose a valid option.")


def setUpHome():
    mySmartHome = b.SmartHome()

    for _ in range(5):
        deviceChoice = askUserForDevice()
        mySmartHome.addDevice(deviceChoice)
        print("Successfully Connected!")
    print(f"\n!!!!!!!!!!!!!!! APP OPENING !!!!!!!!!!!!!!!")
    return mySmartHome


# endregion Setting Up Home
# region Main
def main():
    print("Opening Frontend")
    mySmartHomeSystem = SmartHomeSystem(setUpHome())
    mySmartHomeSystem.run()


# endregion Main

main()
