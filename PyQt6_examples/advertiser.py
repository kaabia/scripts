# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PyQt6 port of the bluetooth/heartrate-server example from Qt v6.x"""

from enum import Enum
from PyQt6.QtCore import QByteArray, QCoreApplication, QLoggingCategory
from PyQt6.QtBluetooth import (QBluetoothUuid, QLowEnergyAdvertisingData,
                                 QLowEnergyAdvertisingParameters,
                                 QLowEnergyCharacteristic,
                                 QLowEnergyCharacteristicData,
                                 QLowEnergyController,
                                 QLowEnergyDescriptorData,
                                 QLowEnergyServiceData)

class BluetoothAdvertiser:
    def __init__(self) -> None:
        QLoggingCategory.setFilterRules("qt.bluetooth* = true")
        #! [Advertising Data]
        # Set up Advertising Data
        self.m_advertisingData =  QLowEnergyAdvertisingData()
        # Set discoverability for other devices to establish connection
        self.m_advertisingData.setDiscoverability(QLowEnergyAdvertisingData.Discoverability.DiscoverabilityGeneral)
         # Include power level in advertising payload
        self.m_advertisingData.setIncludePowerLevel(True)
        # Set Device name
        self.m_advertisingData.setLocalName("BLE_ADVERTISER")
        # Set default Heart rate service to offerin its minimal form
        self.m_advertisingData.setServices([QBluetoothUuid(QBluetoothUuid.ServiceClassUuid.HeartRate)])

        # Add caracteristic
        self.charData = QLowEnergyCharacteristicData()
        self.charData.setUuid(QBluetoothUuid(QBluetoothUuid.CharacteristicType.HeartRateMeasurement))
        val = QByteArray()
        val.append(chr(0).encode())
        val.append(chr(0).encode())
        self.charData.setValue(val)
        self.charData.setProperties(QLowEnergyCharacteristic.PropertyType.Notify)
        # Add Service
        self.serviceData = QLowEnergyServiceData()
        self.serviceData.setType(QLowEnergyServiceData.ServiceType.ServiceTypePrimary)
        self.serviceData.setUuid(QBluetoothUuid(QBluetoothUuid.ServiceClassUuid.HeartRate))
        self.serviceData.addCharacteristic(self.charData)
        # Advertising and Listening for Incoming Connections
        self.leController = QLowEnergyController.createPeripheral()
        self.leController.addService(self.serviceData)

    def startAdvertising(self):
        self.leController.connect(self.controller_notification)
        # Start advertising with the given advertising data
        self.leController.startAdvertising(QLowEnergyAdvertisingParameters(),
                                           self.m_advertisingData,
                                           self.m_advertisingData)

    def controller_notification(self, characteristic, newValue):
        print(f"Notification received. Characteristic: {characteristic.uuid()}, Value: {newValue}")


if __name__ == '__main__':
    # Create a QCoreApplication object to run the event loop
    app = QCoreApplication([])
    # Create a BluetoothScanner object
    advertiser = BluetoothAdvertiser()
    # Set advertising
    advertiser.startAdvertising()
    # Run the event loop until the discovery process is finished
    app.exec()