# Edge Deployment
Use this information to deploy smart plug modules on your edge device

## Contents 

| File             | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| `readme.md`             | This readme file                                              |
| `Dockerfile.arm64v8`    | The Dockerfile of the smart plug module                       |
| `main.py`               | The main program file                                         |
| `module.json`           | The config of the smart plug module                           |
| `requirement.txt`       | List of all dependent Python libraries                        |

## Setup for edge

1. Fill your ACR address in module.json file
```
   "repository": "<Your container registry address>"
```
2. Build and push your IoT Edge solutions to your private ACR 
Use VSCode as in [here](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-develop-for-linux?view=iotedge-2020-11#build-and-push-your-solution) to build and push your solutions

3. Deploy edge modules to device
Use VSCode as in [here](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-develop-for-linux?view=iotedge-2020-11#deploy-modules-to-device) to deploy the modules to the Percept DK with the above files.


### Credits and references
- [Tutorial: Develop IoT Edge modules with Linux containers](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-develop-for-linux?view=iotedge-2020-11)
