#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show streaming sending events with different options to an Event Hub.
"""

# pylint: disable=C0111

import time
import os
from numpy import genfromtxt
import json

from azure.eventhub import EventHubProducerClient, EventData

CONNECTION_STR = "Your EventHubs connection string"
EVENTHUB_NAME = "Your EventHub name"

#Read the accelerator X, Y, Z data from a file as a simluation.
#In actual case, we get the data from a sensor.
array3d_acc = genfromtxt('acc.csv', delimiter=',')

start_time = time.time()

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

with producer:
    for i in range(array3d_acc.shape[0]):
        event_data_batch = producer.create_batch()
        tempstring = {"x": array3d_acc[i][0], "y": array3d_acc[i][1], "z": array3d_acc[i][2]}
        json_data = json.dumps(tempstring)
        event_data = EventData(json_data)
        try:
            event_data_batch.add(event_data)
        except ValueError:
            producer.send_batch(event_data_batch)
            event_data_batch = producer.create_batch()
            event_data_batch.add(event_data)
        
        if len(event_data_batch) > 0:
            producer.send_batch(event_data_batch)

        time.sleep(0.5)
    

print("Send messages in {} seconds.".format(time.time() - start_time))