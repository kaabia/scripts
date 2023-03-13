# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PyQt6 port of the bluetooth/heartrate-server example from Qt v6.x"""

import sys
from enum import Enum

from PyQt6.QtBluetooth import (QBluetoothUuid, QLowEnergyAdvertisingData,
                                 QLowEnergyAdvertisingParameters,
                                 QLowEnergyCharacteristic,
                                 QLowEnergyCharacteristicData,
                                 QLowEnergyController,
                                 QLowEnergyDescriptorData,
                                 QLowEnergyServiceData)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QByteArray, QTimer, QLoggingCategory


class ValueChange(Enum):
    VALUE_UP = 1
    VALUE_DOWN = 2


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    QLoggingCategory.setFilterRules("qt.bluetooth* = true")

#! [Advertising Data]
    advertising_data = QLowEnergyAdvertisingData()
    advertising_data.setDiscoverability(QLowEnergyAdvertisingData.Discoverability.DiscoverabilityGeneral)
    advertising_data.setIncludePowerLevel(True)
    advertising_data.setLocalName("badr")
    advertising_data.setServices([QBluetoothUuid(QBluetoothUuid.ServiceClassUuid.HeartRate)])
#! [Advertising Data]

#! [Service Data]
    char_data = QLowEnergyCharacteristicData()
    char_data.setUuid(QBluetoothUuid(QBluetoothUuid.CharacteristicType.HeartRateMeasurement))

    #val =  QByteArray(2, 0)
    val = QByteArray()
    val.append(chr(0).encode())
    val.append(chr(0).encode())
        
    char_data.setValue(val)
    char_data.setProperties(QLowEnergyCharacteristic.PropertyType.Notify)
    client_config = QLowEnergyDescriptorData(QBluetoothUuid(QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration), val)
    char_data.addDescriptor(client_config)

    service_data = QLowEnergyServiceData()
    service_data.setType(QLowEnergyServiceData.ServiceType.ServiceTypePrimary)
    service_data.setUuid(QBluetoothUuid(QBluetoothUuid.ServiceClassUuid.HeartRate))
    service_data.addCharacteristic(char_data)
#! [Service Data]

#! [Start Advertising]
    le_controller = QLowEnergyController.createPeripheral()
    service = le_controller.addService(service_data)
    le_controller.startAdvertising(QLowEnergyAdvertisingParameters(),
                                   advertising_data)
#! [Start Advertising]

    sys.exit(app.exec())
    