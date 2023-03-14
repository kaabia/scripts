# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PyQt6 port of the bluetooth/heartrate-server example from Qt v6.x"""

from enum import Enum
from PyQt6.QtCore import QByteArray, QCoreApplication, QLoggingCategory, QTimer
from PyQt6.QtBluetooth import (QBluetoothUuid, QLowEnergyAdvertisingData,
                                 QLowEnergyAdvertisingParameters,
                                 QLowEnergyCharacteristic,
                                 QLowEnergyCharacteristicData,
                                 QLowEnergyController,
                                 QLowEnergyServiceData)

class BluetoothAdvertiser:
    def __init__(self) -> None:
        #QLoggingCategory.setFilterRules("qt.bluetooth* = true")
        #! [Advertising Data]
        # Set up Advertising Data
        self.m_advertisingData =  QLowEnergyAdvertisingData()
        # Set discoverability for other devices to establish connection
        self.m_advertisingData.setDiscoverability(QLowEnergyAdvertisingData.Discoverability.DiscoverabilityGeneral)
         # Include power level in advertising payload
        self.m_advertisingData.setIncludePowerLevel(True)
        # Set Device name
        self.m_advertisingData.setLocalName("CONTI_CDD")
        # Set default Heart rate service to offerin its minimal form

        # Add caracteristic
        self.charData = QLowEnergyCharacteristicData()
        self.charData.setUuid(QBluetoothUuid(QBluetoothUuid.CharacteristicType.HeartRateMeasurement))
        val = QByteArray()
        val.append(chr(0).encode())
        val.append(chr(0).encode())
        self.charData.setValue(val)
        self.charData.setProperties(QLowEnergyCharacteristic.PropertyType.Read)

        # Add Service
        self.serviceData = QLowEnergyServiceData()
        self.serviceData.setType(QLowEnergyServiceData.ServiceType.ServiceTypePrimary)
        self.serviceData.setUuid(QBluetoothUuid(QBluetoothUuid.ServiceClassUuid.HeartRate))
        self.serviceData.addCharacteristic(self.charData)
        # Advertising and Listening for Incoming Connections
        self.leController = QLowEnergyController.createPeripheral()
        # Connect leController signal to callback functions
        self.leController.connected.connect(self.connected)
        self.leController.disconnected.connect(self.disconnected_from_device)
        self.leController.stateChanged.connect(self.state_changed)
        self.leController.errorOccurred.connect(self.error_hander)
        # Add service
        self.leController.addService(self.serviceData)

    # Controller signals
    def error_hander(self):
        print("Error Occured !")
        QCoreApplication.quit()

    def state_changed(self, *args, **Kwargs):
        if args[0] == QLowEnergyController.ControllerState.AdvertisingState:
            print("ADVERTISER STATE >> ADVERTISING ")
        elif args[0] == QLowEnergyController.ControllerState.UnconnectedState:
            print("ADVERTISER STATE >> IDLE ")
        elif args[0] == QLowEnergyController.ControllerState.ConnectingState:
            print("ADVERTISER STATE >> CONNECTING ")
        elif args[0] == QLowEnergyController.ControllerState.ConnectedState:
            print("ADVERTISER STATE >> CONNECTED ")
            # Disconnet device after 10 seconds
            QTimer.singleShot(10000, self.disconnect)
        elif args[0] == QLowEnergyController.ControllerState.DiscoveringState:
            print("ADVERTISER STATE >> DISCOVERING ")
        elif args[0] == QLowEnergyController.ControllerState.DiscoveredState:
            print("ADVERTISER STATE >> DISCOVERED ")
        elif args[0] == QLowEnergyController.ControllerState.ClosingState:
            print("ADVERTISER STATE >> CLOSING ")

    def disconnected_from_device(self):
        print("Device Disconnected")

    def connected(self):
        print("Device Connected")

    # APIs
    def startAdvertising(self):
        # Start advertising with the given advertising data
        self.leController.startAdvertising(QLowEnergyAdvertisingParameters(),
                                           self.m_advertisingData, self.m_advertisingData)

    def stopAdvertising(self):
        # Stop advertising 
        print("Stop advertising is requested ")
        self.leController.stopAdvertising()

    def disconnect(self):
        # Disconnect from remote BLE device
        print("Disconnect from device is requested ")
        self.leController.disconnectFromDevice()

if __name__ == '__main__':
    # Create a QCoreApplication object to run the event loop
    app = QCoreApplication([])
    # Create a BluetoothScanner object
    advertiser = BluetoothAdvertiser()
    # Set advertising
    advertiser.startAdvertising()
    # Run the event loop until the discovery process is finished
    app.exec()
