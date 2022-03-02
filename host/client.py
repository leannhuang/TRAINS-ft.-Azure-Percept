# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific HTTP endpoint on your IoT Hub.
import sys
# pylint: disable=E0611

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult

from builtins import input
from pyfirmata import Arduino, util
import time
import asyncio
import time
import uuid
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message
from time import sleep


CONNECTION_STRING = "connection string"
DEVICE_ID = "rail"
board = Arduino('/dev/cu.usbmodem301')
pin9 = board.get_pin('d:9:s')

#board.digital[13].write(0)
def iothub_devicemethod_sample_run():
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        # Call the direct method.
        module_method = CloudToDeviceMethod(method_name='anomaly_detect', payload=None, response_timeout_in_seconds=30)

        response = registry_manager.invoke_device_module_method(DEVICE_ID, 'VisionExecuteModule', module_method)
        print ( "Response payload          : {0}".format(response.payload) )
        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(METHOD_NAME) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )

        if response.payload['anomalyAlert']:
            board.digital[13].write(1)
        else:
            board.digital[13].write(0)

        module_method = CloudToDeviceMethod(method_name='motor_activate', payload=None, response_timeout_in_seconds=30)

        response = registry_manager.invoke_device_module_method(DEVICE_ID, 'VisionExecuteModule', module_method)
        print ( "Response payload          : {0}".format(response.payload) )
        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(METHOD_NAME) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )

        print(response.payload['motorActivate'])
        if response.payload['motorActivate']:
            ang = 0 
            for _ in range(5):
                pin9.write(ang)
                ang += 20
                ang %= 180
                sleep(1) 

    except Exception as ex:
        print ( "" )
        print ( "Unexpected error {0}".format(ex) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )


if __name__ == '__main__':
    print ( "IoT Hub Python quickstart #2..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )
    while True:
        time.sleep(0.5)
        iothub_devicemethod_sample_run()
