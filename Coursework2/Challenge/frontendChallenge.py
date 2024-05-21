# region IMPORTS
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
import backendChallenge as b


# endregion IMPORTS

# region PROGRAM WIDE TKINTER FUNCTIONS
def addToGrid(item, column, row):
    item.grid(column=column, row=row, padx=5, pady=5, sticky="W")


def closeWindow(tkWindow):
    tkWindow.destroy()


# endregion PROGRAM WIDE TKINTER FUNCTIONS
# region UI RELATED FUNCTIONS
def getOnOrOff(device):
    onOrOff = "On" if device.getSwitchedOn() else "Off"
    return onOrOff


def retrieveLabel(device):
    if isinstance(device, b.SmartWashingMachine):
        labelText = f"{device.getName()}: {getOnOrOff(device)}, Wash Mode: {device.getOption()}"
    else:
        labelText = f"{device.getName()}: {getOnOrOff(device)}, Consumption: {device.getConsumptionRate()}"
    return labelText


def setDeviceStatusFromEdit(button, device):
    device.toggleSwitch()
    button["text"] = getOnOrOff(device).upper()


def askForColour(title):
    color_code = colorchooser.askcolor(title=title)
    return color_code


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
        self.mainFrame.grid(column=0, row=0)
        self.row = 1
        self.deviceLabels = []
        self.deviceCheckboxes = []
        self.deviceSpinboxes = []
        self.allDeviceWidgets = []
        self.defaultButtons = []
        self.time = -1
        self.clockLabel = []
        self.loadedFile = ""
        # Accessibility Properties
        self.textSize = 16
        self.textColour = "#000000"
        self.backgroundColour = "#FFFFFF"
        self.foregroundColour = "#F4F4F4"
        self.win.configure(background=self.backgroundColour)
        self.mainFrame.configure(background=self.backgroundColour)
        # Image References
        self.washingMachineIcon = PhotoImage(file="Images/WM.png")
        self.displayWMImage = self.washingMachineIcon.subsample(14, 14)
        self.plugIcon = PhotoImage(file="Images/Plug.png")
        self.displayPlugImage = self.plugIcon.subsample(7, 7)
        self.addIcon = PhotoImage(file="Images/AddIcon.png")
        self.displayAddIcon = self.addIcon.subsample(7, 7)
        self.removeIcon = PhotoImage(file="Images/DeleteIcon.png")
        self.displayRemoveIcon = self.removeIcon.subsample(14, 14)
        self.saveIcon = PhotoImage(file="Images/SaveIcon.png")
        self.displaySaveIcon = self.saveIcon.subsample(9, 9)
        self.loadIcon = PhotoImage(file="Images/LoadIcon.png")
        self.displayLoadIcon = self.loadIcon.subsample(7, 7)
        self.settingsIcon = PhotoImage(file="Images/SettingsIcon.png")
        self.displaySettingsIcon = self.settingsIcon.subsample(14, 14)
        self.accessIcon = PhotoImage(file="Images/AccessIcon.png")
        self.displayAccessIcon = self.accessIcon.subsample(14, 14)

    # region UI Functions
    def createLabel(self, text, mainFrame):
        lbl = Label(mainFrame, text=text, relief='solid', borderwidth=2,
                    font=("Monoton", self.textSize), padx=10, pady=5, fg=self.textColour, bg=self.foregroundColour)
        return lbl

    def createButton(self, text, mainFrame, command):
        btn = Button(mainFrame, text=text, relief='solid', borderwidth=2,
                     font=("Monoton", self.textSize), padx=5, pady=5, command=command,
                     fg=self.textColour, bg=self.foregroundColour)
        return btn

    def createEntry(self, mainFrame):
        entry = Entry(mainFrame, relief='solid', borderwidth=2, font=("Monoton", self.textSize),
                      fg=self.textColour, bg=self.foregroundColour)
        return entry

    def createSpinbox(self, mainFrame, fromVar, toVar, defaultValue):
        spinbox = Spinbox(mainFrame, relief='solid', borderwidth=2, font=("Monoton", self.textSize),
                          from_=fromVar, to=toVar, textvariable=defaultValue,
                          fg=self.textColour, bg=self.foregroundColour)
        return spinbox

    def createCheckbox(self, mainFrame, text, command):
        checkbox = Checkbutton(mainFrame, relief='solid', borderwidth=2, font=("Monoton", self.textSize), text=text,
                               fg=self.textColour, bg=self.foregroundColour, command=command)
        return checkbox

    def createRadioButton(self, mainFrame, text, var, val, command):
        radioButton = Radiobutton(mainFrame, relief='solid', borderwidth=2, font=("Monoton", self.textSize),
                                  text=text, variable=var, value=val, command=command,
                                  fg=self.textColour, bg=self.foregroundColour)
        return radioButton

    # endregion UI Functions
    # Create all default widgets
    def createDefaultWidgets(self):

        # Turn On All Button
        btnTurnOnAll = self.createButton("Turn on all", self.mainFrame, command=self.turnAllOn)
        addToGrid(btnTurnOnAll, 1, 0)
        self.defaultButtons.append(btnTurnOnAll)

        # Turn Off All Button
        btnTurnOffAll = self.createButton("Turn off all", self.mainFrame, command=self.turnAllOff)
        addToGrid(btnTurnOffAll, 2, 0)
        self.defaultButtons.append(btnTurnOffAll)

        # Device Scheduler
        clockLbl = self.createLabel("00:00", self.mainFrame)
        clockLbl.configure(width=8)
        addToGrid(clockLbl, 4, 0)
        self.clockLabel.append(clockLbl)

        # Permanent Data Storage
        btnLoadFromFile = self.createButton("Load", self.mainFrame, command=self.openFromFile)
        btnLoadFromFile.configure(image=self.displayLoadIcon)
        addToGrid(btnLoadFromFile, 3, 100)
        self.defaultButtons.append(btnLoadFromFile)

        btnSaveToFile = self.createButton("Save Setup", self.mainFrame, command=self.saveToFile)
        btnSaveToFile.configure(image=self.displaySaveIcon)
        addToGrid(btnSaveToFile, 2, 100)
        self.defaultButtons.append(btnSaveToFile)

        # Accessibility
        btnLoadIandEWindow = self.createButton("Accessibility", self.mainFrame, command=self.loadAccessibilityWindow)
        btnLoadIandEWindow.configure(image=self.displayAccessIcon)
        addToGrid(btnLoadIandEWindow, 4, 100)
        self.defaultButtons.append(btnLoadIandEWindow)

        # Setting the grid row to +100, so it will always stay at the very bottom
        btnAddDevice = self.createButton("Add Device", self.mainFrame, command=self.loadAddWindow)
        btnAddDevice.configure(image=self.displayAddIcon)
        addToGrid(btnAddDevice, 1, 100)
        self.defaultButtons.append(btnAddDevice)

    # Create all the widgets for every device within the Smart Home System
    def createAllDeviceWidgets(self):

        for device in self.smartHome.devices:
            self.createDeviceWidgets(device)
            self.row += 1

    # Create every widget associated to one individual device and adds them to the grid
    def createDeviceWidgets(self, device):

        defaultSpinboxValue = IntVar()
        maxValue = 150
        if isinstance(device, b.SmartWashingMachine):
            deviceLogo = Label(self.mainFrame, image=self.displayWMImage, relief='solid', borderwidth=2,
                               font=("Monoton", self.textSize), padx=10, pady=5, fg=self.textColour,
                               bg=self.foregroundColour)
            defaultSpinboxValue.set(b.getOptionKey(device.getOption()))
            maxValue = 3
            settingSpinbox = self.createSpinbox(self.mainFrame, 1, maxValue, defaultSpinboxValue)
            settingSpinbox.configure(command=lambda: [device.setOption(settingSpinbox.get()), self.updateLabels()],
                                     width=4)
        else:
            deviceLogo = Label(self.mainFrame, image=self.displayPlugImage, relief='solid', borderwidth=2,
                               font=("Monoton", self.textSize), padx=10, pady=5, fg=self.textColour,
                               bg=self.foregroundColour)
            defaultSpinboxValue.set(device.getConsumptionRate())
            settingSpinbox = self.createSpinbox(self.mainFrame, 1, maxValue, defaultSpinboxValue)
            settingSpinbox.configure(command=lambda: [device.setConsumptionRate(settingSpinbox.get()),
                                                      self.updateLabels()], width=4)
        addToGrid(deviceLogo, 0, self.row)
        self.allDeviceWidgets.append(deviceLogo)

        # Retrieve all data for the label to be in the format: {Washing Machine: Off, Wash Mode: Daily Wash}
        labelText = retrieveLabel(device)

        lblDevice = self.createLabel(labelText, self.mainFrame)
        lblDevice.configure(width=40)
        self.deviceLabels.append(lblDevice)
        self.allDeviceWidgets.append(lblDevice)

        cbToggleDevice = self.createCheckbox(self.mainFrame, "Toggle",
                                             command=lambda v=self.row: self.toggleDevice(v - 1))
        self.allDeviceWidgets.append(cbToggleDevice)
        self.deviceCheckboxes.append(cbToggleDevice)

        self.allDeviceWidgets.append(settingSpinbox)
        self.deviceSpinboxes.append(settingSpinbox)

        btnEditDevice = self.createButton("Edit", self.mainFrame,
                                          command=lambda v=self.row: self.loadEditWindow(v - 1))
        btnEditDevice.configure(image=self.displaySettingsIcon)
        self.allDeviceWidgets.append(btnEditDevice)

        btnDeleteDevice = self.createButton("Delete", self.mainFrame,
                                            command=lambda v=self.row: self.deleteDevice(v - 1))
        btnDeleteDevice.configure(image=self.displayRemoveIcon)

        self.allDeviceWidgets.append(btnDeleteDevice)

        # Add widgets to the grid
        addToGrid(lblDevice, 1, self.row)
        addToGrid(cbToggleDevice, 2, self.row)
        addToGrid(settingSpinbox, 3, self.row)
        addToGrid(btnEditDevice, 4, self.row)
        addToGrid(btnDeleteDevice, 5, self.row)

    # For every label on the interface, reset the text accordingly
    def updateLabels(self):
        for i in range(0, len(self.deviceLabels)):
            currentDevice = self.smartHome.getDeviceAt(i)
            labelText = retrieveLabel(currentDevice)
            self.deviceLabels[i].configure(text=labelText)
            if currentDevice.switchedOn:
                self.deviceCheckboxes[i].select()
            else:
                self.deviceCheckboxes[i].deselect()

    # Reset all device related widgets
    def refreshUI(self):
        for widget in self.allDeviceWidgets:
            widget.destroy()
        self.allDeviceWidgets.clear()

        for label in self.deviceLabels:
            label.destroy()
        self.deviceLabels.clear()

        for checkbox in self.deviceCheckboxes:
            checkbox.destroy()
        self.deviceCheckboxes.clear()

        for spinbox in self.deviceSpinboxes:
            spinbox.destroy()
        self.deviceSpinboxes.clear()

        self.row = 1
        self.createAllDeviceWidgets()

    # endregion UI Creation
    # region ADDING FEATURE
    def loadAddWindow(self):
        addDeviceWindow = Toplevel(self.win)
        addDeviceWindow.title(f"Smart Home: Add Device")
        addDeviceWindow.mainFrame = Frame(addDeviceWindow)
        addDeviceWindow.mainFrame.grid(column=0, row=0)
        addDeviceWindow.configure(bg=self.backgroundColour)
        addDeviceWindow.mainFrame.configure(bg=self.backgroundColour)

        btnAddWashingMachine = self.createButton("Add a Washing Machine", addDeviceWindow.mainFrame,
                                                 command=lambda: self.addDevice("Washing Machine"))
        addToGrid(btnAddWashingMachine, 0, 0)

        inputConsumptionLbl = self.createLabel("Please input a consumption rate", addDeviceWindow.mainFrame)
        addToGrid(inputConsumptionLbl, 1, 1)

        plugConsumptionEntry = self.createEntry(addDeviceWindow.mainFrame)
        addToGrid(plugConsumptionEntry, 1, 2)

        btnAddPlug = self.createButton("Add a Plug", addDeviceWindow.mainFrame,
                                       command=lambda: self.addDevice("Plug", plugConsumptionEntry.get()))
        addToGrid(btnAddPlug, 1, 0)

        btnClose = self.createButton("Close", addDeviceWindow.mainFrame,
                                     command=lambda: closeWindow(addDeviceWindow))
        addToGrid(btnClose, 0, 2)

    def addDevice(self, device, consumption=""):
        if device == "Washing Machine":
            newDevice = b.SmartWashingMachine("Washing Machine")
        else:
            try:
                consumptionInt = int(consumption)
                if consumptionInt not in range(0, 151):
                    print("The rate needs to be between 0-150")
                    return
                newDevice = b.SmartPlug("Plug", consumptionInt)
            except ValueError:
                print("This is not a valid rate!")
                return

        self.smartHome.addDevice(newDevice)
        self.refreshUI()
        self.row += 1

    # endregion ADDING FEATURE
    # region EDITING FEATURE
    def loadEditWindow(self, index):
        editingDevice = self.smartHome.getDeviceAt(index)
        deviceName = editingDevice.getName()
        editWindow = Toplevel(self.win)
        editWindow.title(f"Smart Home: Edit {deviceName}")
        editWindow.mainFrame = Frame(editWindow)
        editWindow.mainFrame.grid(column=0, row=0)
        editWindow.configure(bg=self.backgroundColour)
        editWindow.mainFrame.configure(bg=self.backgroundColour)

        editTitle = self.createLabel(deviceName, editWindow.mainFrame)
        addToGrid(editTitle, 1, 0)

        btnClose = self.createButton("Close", editWindow.mainFrame, command=lambda: closeWindow(editWindow))
        addToGrid(btnClose, 2, 0)

        deviceNameLbl = self.createLabel(f"Device Name:", editWindow.mainFrame)
        addToGrid(deviceNameLbl, 0, 1)
        deviceNameEntry = self.createEntry(editWindow.mainFrame)
        addToGrid(deviceNameEntry, 1, 1)

        deviceStatusLbl = self.createLabel("Device Status:", editWindow.mainFrame)
        addToGrid(deviceStatusLbl, 0, 2)

        btnDeviceStatus = self.createButton(getOnOrOff(editingDevice).upper(), editWindow.mainFrame, "")
        btnDeviceStatus.configure(command=lambda: setDeviceStatusFromEdit(btnDeviceStatus, editingDevice))
        addToGrid(btnDeviceStatus, 1, 2)

        if isinstance(editingDevice, b.SmartWashingMachine):
            deviceOptionLbl = self.createLabel("Device Setting:", editWindow.mainFrame)
        else:
            deviceOptionLbl = self.createLabel("Device Consumption:", editWindow.mainFrame)
        addToGrid(deviceOptionLbl, 0, 3)
        deviceOptionEntry = self.createEntry(editWindow.mainFrame)
        addToGrid(deviceOptionEntry, 1, 3)

        # DEVICE SCHEDULER CHALLENGE
        automaticScheduler = self.createLabel("Device Scheduler", editWindow.mainFrame)
        addToGrid(automaticScheduler, 0, 4)

        times = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                 "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                 "20:00", "21:00", "22:00", "23:00"]

        selectedOnTime = StringVar()
        selectedOnTime.set(editingDevice.getOnSchedule())

        automaticallyTurnOnCB = OptionMenu(editWindow.mainFrame, selectedOnTime, *times)
        automaticallyTurnOnCB.configure(relief='solid', borderwidth=2, font=("Monoton", self.textSize),
                                        padx=10, pady=5, bg=self.foregroundColour, fg=self.textColour)
        addToGrid(automaticallyTurnOnCB, 1, 4)

        selectedOffTime = StringVar()
        selectedOffTime.set(editingDevice.getOffSchedule())

        automaticallyTurnOffCB = OptionMenu(editWindow.mainFrame, selectedOffTime, *times)
        automaticallyTurnOffCB.configure(relief='solid', borderwidth=2, font=("Monoton", self.textSize),
                                         padx=10, pady=5, bg=self.foregroundColour, fg=self.textColour)
        addToGrid(automaticallyTurnOffCB, 1, 5)

        btnSaveOptions = self.createButton("Save Options", editWindow.mainFrame,
                                           command=lambda: self.saveDeviceOptions(editingDevice, deviceNameEntry.get(),
                                                                                  deviceOptionEntry.get(),
                                                                                  selectedOnTime.get(),
                                                                                  selectedOffTime.get()))
        addToGrid(btnSaveOptions, 1, 100)

    def saveDeviceOptions(self, device, deviceName, option, onSchedule, offSchedule):
        if deviceName != "":
            device.setName(deviceName)
        if isinstance(device, b.SmartWashingMachine):
            if option != "":
                device.setOption(option)
        else:
            if option != "":
                if validateConsumption(option):
                    device.setConsumptionRate(option)
        device.setOnSchedule(onSchedule)
        device.setOffSchedule(offSchedule)
        self.refreshUI()

    # endregion EDITING FEATURE

    def loadAccessibilityWindow(self):
        accessibilityWindow = Toplevel(self.win)
        accessibilityWindow.title(f"Smart Home: Add Device")
        accessibilityWindow.mainFrame = Frame(accessibilityWindow)
        accessibilityWindow.mainFrame.grid(column=0, row=0)
        accessibilityWindow.configure(bg=self.backgroundColour)
        accessibilityWindow.mainFrame.configure(bg=self.backgroundColour)

        # The user should be able to alter text size, change between light and dark mode, and also define a custom
        # colour scheme (consisting of a background and text colour)
        titleLbl = self.createLabel("Interface & Accessibility", accessibilityWindow.mainFrame)
        addToGrid(titleLbl, 1, 0)

        textSizeLbl = self.createLabel("Text Size:", accessibilityWindow.mainFrame)
        addToGrid(textSizeLbl, 0, 1)

        defaultSpinboxValue = IntVar()
        defaultSpinboxValue.set(self.textSize)
        textSizeSpinbox = self.createSpinbox(accessibilityWindow.mainFrame, 6, 24, defaultSpinboxValue)
        addToGrid(textSizeSpinbox, 1, 1)

        colourSchemeLbl = self.createLabel("Colour Scheme:", accessibilityWindow.mainFrame)
        addToGrid(colourSchemeLbl, 0, 2)

        colourScheme = StringVar()

        lightModeColourSchemeRB = self.createRadioButton(accessibilityWindow.mainFrame, 'Light Mode', colourScheme, "1",
                                                         "")
        addToGrid(lightModeColourSchemeRB, 1, 2)

        darkModeColourSchemeRB = self.createRadioButton(accessibilityWindow.mainFrame, 'Dark Mode', colourScheme, "2",
                                                        "")
        addToGrid(darkModeColourSchemeRB, 1, 3)

        customModeColourSchemeRB = self.createRadioButton(accessibilityWindow.mainFrame,
                                                          'Custom', colourScheme, "3", "")
        addToGrid(customModeColourSchemeRB, 1, 4)

        btnSaveSettings = self.createButton("Save", accessibilityWindow.mainFrame,
                                            command=lambda: self.saveAccessibilityOptions(colourScheme.get(),
                                                                                          textSizeSpinbox.get(),
                                                                                          accessibilityWindow))
        addToGrid(btnSaveSettings, 1, 5)

    def saveAccessibilityOptions(self, colourScheme, fontSize, window):
        if colourScheme == "1":
            self.textColour = "#000000"
            self.backgroundColour = "#FFFFFF"
            self.foregroundColour = "#F4F4F4"
        elif colourScheme == "2":
            self.textColour = "#C1C1C1"
            self.backgroundColour = "#282828"
            self.foregroundColour = "#515151"
        elif colourScheme == "3":
            self.textColour = askForColour("Choose a TEXT colour")[1]
            self.backgroundColour = askForColour("Choose a BACKGROUND colour")[1]
            self.foregroundColour = askForColour("Choose a FOREGROUND colour")[1]
        else:
            pass
        closeWindow(window)
        self.textSize = fontSize
        self.updateAccessibility()

    def updateAccessibility(self):
        for button in self.defaultButtons:
            button.configure(fg=self.textColour, font=("Monoton", self.textSize), bg=self.foregroundColour)
        for widget in self.allDeviceWidgets:
            widget.configure(fg=self.textColour, font=("Monoton", self.textSize), bg=self.foregroundColour)
        self.win.configure(background=self.backgroundColour)
        self.mainFrame.configure(background=self.backgroundColour)
        self.clockLabel[0].configure(font=("Monoton", self.textSize), fg=self.textColour, bg=self.foregroundColour)
        self.refreshUI()

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
        self.smartHome.devices.pop(index)
        self.refreshUI()

    def clock(self):
        self.time += 1
        if self.time == 24:
            self.time = 0

        if self.time < 10:
            currentTimeStr = f"0{self.time}:00"
        else:
            currentTimeStr = f"{self.time}:00"
        self.clockLabel[0].configure(text=currentTimeStr)
        self.checkSchedules(currentTimeStr)
        self.autoSave()
        self.win.after(3000, self.clock)

    def checkSchedules(self, time):
        for device in self.smartHome.devices:
            if device.getOnSchedule() == time:
                device.switchedOn = True
                print(f"Turned {device.getName()} on automatically")
                self.updateLabels()
            if device.getOffSchedule() == time:
                device.switchedOn = False
                print(f"Turned {device.getName()} off automatically")
                self.updateLabels()

    def openFromFile(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("Text Files", "*.txt"), ("CSV Files", "*.csv*")))
        if filename != "":
            self.smartHome.collectDevicesFromFile(filename)
            print(f"LOADED FROM {filename}")
            self.loadedFile = filename
            self.refreshUI()
        else:
            print("Invalid File")

    def saveToFile(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("Text Files", "*.txt"), ("CSV Files", "*.csv*")))
        if filename != "":
            self.smartHome.saveDevicesToFile(filename)
            print(f"SAVED TO {filename}")
        else:
            print("Invalid File")

    def autoSave(self):
        if self.loadedFile == "":
            filename = "SmartHouses/DefaultSave.txt"
            self.smartHome.saveDevicesToFile(filename)
        else:
            self.smartHome.saveDevicesToFile(self.loadedFile)

    # endregion BACKEND COMMUNICATIONS
    # region ON START
    # Draw all the widgets onto the TK Interface
    def createAllWidgets(self):
        self.createDefaultWidgets()
        self.createAllDeviceWidgets()

    def runDefaultSave(self):
        print(f"\n!!!!!!!!!!!!!!! APP OPENING !!!!!!!!!!!!!!!")
        self.loadedFile = "SmartHouses//DefaultSave.txt"
        self.smartHome.collectDevicesFromFile(self.loadedFile)
        self.createAllWidgets()
        self.clock()
        self.win.mainloop()

    def run(self):
        print(f"\n!!!!!!!!!!!!!!! APP OPENING !!!!!!!!!!!!!!!")
        self.createAllWidgets()
        self.clock()
        self.win.mainloop()
    # endregion ON START


# endregion Smart Home System App
# region Setting Up Home
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
                device = b.SmartPlug("Plug", askUserForConsumption())
            else:
                device = b.SmartWashingMachine("Washing Machine")
            return device
        else:
            print(f"\nInvalid choice! Please choose a valid option.")


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


def setUpHome():
    mySmartHome = b.SmartHome()
    return mySmartHome


# endregion Setting Up Home
# region Main
def main():
    while True:
        print("Please select one of the following options:\n"
              "1: Load Default Save\n"
              "2: New SmartHouse")
        userChoice = input()
        try:
            userChoice = int(userChoice)
            if userChoice == 1:
                newSmartHome = b.SmartHome()
                mySmartHomeSystem = SmartHomeSystem(newSmartHome)
                mySmartHomeSystem.runDefaultSave()
                break
            elif userChoice == 2:
                mySmartHomeSystem = SmartHomeSystem(setUpHome())
                mySmartHomeSystem.run()
                break
            else:
                print("Must be 1 or 2!")
        except ValueError:
            print("Input MUST be a number!")


# endregion Main

main()
