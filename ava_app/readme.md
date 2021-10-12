# AVA cloud to device sample console app

To manually call AVA direct methods for debugging.

This directory contains a Python sample app that would enable you to invoke AVA on IoT Edge Direct Methods in a sequence and with parameters, defined by you in a JSON file (operations.json).  This app must be run on the same local network as the Percept DK (run on dev/local machine, not the Percept DK).

## Contents

| File             | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| `readme.md`             | This readme file                                              |
| `operations_start_cvr.json`   | JSON file defining the sequence of operations to execute upon for starting CVR |
| `operations_delete_cvr.json`   | JSON file defining the sequence of operations to execute upon for stopping CVR |
| `operations_start_http.json`   | JSON file defining the sequence of operations to execute upon for starting http (`simpleserver` module must be running) |
| `operations_delete_http.json`   | JSON file defining the sequence of operations to execute upon for stopping http (`simpleserver` module must be running) |
| `main.py`               | The main program file                                         |
| `requirements.txt`      | List of all dependent Python libraries                        |


## Setup

Create a file named `appsettings.json` in this folder. Add the following text and provide values for all parameters.

```JSON
{
    "IoThubConnectionString" : "<your iothub connection string>",
    "deviceId" : "<device ID>",
    "moduleId" : "avaedge"
}
```

* **IoThubConnectionString** - Refers to the connection string of your IoT hub. This should have registry write and service connect access.
* **deviceId** - Refers to your IoT Edge device ID (registered with your IoT hub)
* **moduleId** - Refers to the module id of Azure Video Analyzer edge module (when deployed to the IoT Edge device)

## Running the sample from Visual Studio Code

Detailed instructions for running the sample can be found in the tutorials for AVA on IoT Edge. Below is a summary of key steps. Make sure you have installed the required prerequisites.

* Open your local clone of this git repository in Visual Studio Code, have the [Azure Iot Tools](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools) extension installed. 
* Right click on src/edge/deployment.template.json and select **“Generate Iot Edge deployment manifest”**. This will create an IoT Edge deployment manifest file in src/edge/config folder named deployment.amd64.json.
* Right click on src/edge/config /deployment.amd64.json and select **"Create Deployment for single device"** and select the name of your edge device. This will trigger the deployment of the IoT Edge modules to your Edge device. You can view the status of the deployment in the Azure IoT Hub extension (expand 'Devices' and then 'Modules' under your IoT Edge device).
* Right click on your edge device in Azure IoT Hub extension and select **"Start Monitoring Built-in Event Endpoint"**.
* Ensure you have installed python dependencies from `requirements.txt` at the base of this repo. This can be done by running `pip install -r requirements.txt` at the base of the repo.
* Check your `topology.json` file used in this app to ensure it has correct values.  If you already have a video in the Azure Portal, you may wish to increment the name in the `topology.json` in the sinks section (under `videoName`).

```json
{
 "@type": "#Microsoft.VideoAnalyzer.VideoSink",
        "name": "videoSink",
        "videoName": "sample-http-extension-<increment here or change name>",
        ...
}
```

* To run CVR only, activate your conda environment if you haven't done so already, go to the `ava_app` folder on the command line and run the `main.py` as follows.

From the base of the repo:
```
cd ava_deploy
conda activate <name of your conda environment>
```

To activate the live AVA pipeline for the CVR only setup, perform the following.

```
python main.py --action start --type cvr
```

To activate the live AVA pipeline for the http `simpleserver` setup, perform the following.

```
python main.py --action start --type http
```

## Deactivate and Delete

To deactivate a live AVA pipeline for CVR only run the following command.  This is nice for debugging purposes and you may always reactivate as shown above.

```
python main.py --action stop --type cvr
```

To deactivate the live AVA pipeline for the http `simpleserver` setup, perform the following.

```
python main.py --action stop --type http
```

## Troubleshooting

- See the [Azure Video Analyzer Troubleshooting page](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/troubleshoot).

- When you see either of the following messages, this generally means the RTSP stream has stop coming in to `avaedge` module (this could be due to `azureeyemodule` crashing for instance).

```json
[IoTHubMonitor] [7:53:20 AM] Message received from [percept-ava/avaedge]:
{
  "code": "connectionRefused",
  "target": "rtsp"
}
[IoTHubMonitor] [7:53:22 AM] Message received from [percept-ava/avaedge]:
{
  "code": "nameResolutionError",
  "target": "rtsp"
}
```

 - When a module crashes, the Video in the Azure Portal will stop Recording, even though it may indicate it is still Recording.  Please give the device a few minutes, and try running the Python script above with the action of `stop` again.  If this does not work after a few minutes, a hard reboot of the device can fix this temporarily so you may `stop` AVA with the Python script above after the device is up and running again.

## Credits and References

- The contents of this folder are based upon the [AVA Python sample app](https://github.com/Azure-Samples/video-analyzer-iot-edge-python).