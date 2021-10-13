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

# this is a timetable that maps time to mileage for look-up, as a simulation. For example [t, m] mean at time t the current travel mileage is m
TIMETABLE = [[0.4,0], [1.16,1], [1.46,2], [1.7,3], [1.9,4], [2.1,5], [2.23,6], [2.4,7], [2.53,8], [2.66,9], [2.8,10], [2.93,11], [3.06,12], [3.2,13], [3.36,14], [3.5,15], [3.6,16], [3.73,17], [3.86,18], [4,19], [4.13,20], [4.26,21], [4.36,22], [4.5,23], [4.6,24], [4.7,25], [4.8,26], [4.9,27], [5,28], [5.1,29], [5.2,30], [5.3,31], [5.4,32], [5.5,33], [5.6,34], [5.7,35], [5.8,36], [5.9,37]]
MILEAGE_THRESHOLD = 18

CONNECTION_STRING = "HostName=rg-leann-361dhub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=cCNnva4+Glpbx3ViGHRXCbei9wbf524ymUSAm9q1aDE="
DEVICE_ID = "rail"
board = Arduino('/dev/cu.usbmodem301')
pin9 = board.get_pin('d:9:s')

#board.digital[13].write(0)

def far_enough(travel_time):
    if (travel_time >= TIMETABLE[-1][0]):
        return False
    if (travel_time <= TIMETABLE[0][0]):
        return True
    for i in range(len(TIMETABLE)):      
        if (travel_time > TIMETABLE[i][0] and travel_time < TIMETABLE[i+1][0]):
            mileage = TIMETABLE[i][1]
            if (mileage > MILEAGE_THRESHOLD):
                print(mileage)
                return False
            else:
                return True
        else:
            continue

def iothub_devicemethod_sample_run(start_time):
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

        travel_time = time.time() - start_time
        if (not far_enough(travel_time)):
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
    start_time = time.time()
    while True:
        time.sleep(0.5)
        iothub_devicemethod_sample_run(start_time)
