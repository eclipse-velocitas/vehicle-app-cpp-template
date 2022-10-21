# Vehicle App C++ Template

![Template CI Workflow](https://github.com/eclipse-velocitas/vehicle-app-cpp-template/actions/workflows/ci.yml/badge.svg)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)

The Vehicle App Template for C++ allows to create `Vehicle Apps` from the [Velocitas](https://github.com/eclipse-velocitas/velocitas-docs) development model in the C++ programming language.

## Folder structure

* 📁 `app` - base directory for a vehicle app
    * 📁 `src` - source code of the vehicle app
    * 📁 `tests` - tests for the vehicle app
    * 📁 `vehicle_model` - vehicle model to be used by the vehicle app

## Building

### Building the App
To build the App, run the build script:
```bash
./build.sh
```

## Starting the runtime

Open the `Run Task` view in VSCode and select `Local - Start VehicleApp runtime`.

## Launching the example
With the runtime running in the background, you can run the app.

### Without debugging

Open the `Run Task` view in VSCode and select `Local - VehicleApp (Dapr run)`.

### With debugging
You can simply launch the example in the Debugging Tab. Make sure the `VehicleApp - Debug (dapr run)` is selected at the top. After the selection is done, you can also simply hit `F5`, to start the debugging session. 

*Note: This launch task will also make sure to re-build the app if it has been modified!*

### Run App and Dapr-Sidecar as individual Docker containers
#### Sidecar
```bash
docker run --net="host" --mount type=bind,source="$(pwd)"/.dapr,target=/.dapr daprio/daprd:edge ./daprd -app-id vehicleapp -dapr-grpc-port 50001 -dapr-http-port 3500 -components-path /.dapr/components -config /.dapr/config.yaml -app-protocol grpc
```
#### App
```bash
docker run --rm -it --net="host" -e DAPR_GRPC_PORT=50001 -e DAPR_HTTP_PORT=3500 localhost:12345/vehicleapp:local
```

## Running in GH Codespaces
GH Codespaces currently restricts the token that is used within the Codespace to just the current repository, working on cloned repositories or
submodules will not be possible without further setup. To work on other repos, you need to create a personal access token [here](https://github.com/settings/tokens/new) which has full "repo" access. Copy the contents of the PAT and create a Codespace secret called `MY_GH_TOKEN` and paste the content of your PAT. Finally you need to give the Codespace secret access to the repository of the Codespace, in this case `vehicle-app-cpp-template`.

## Documentation
* [Velocitas Development Model](https://websites.eclipseprojects.io/velocitas/docs/about/development_model/)
* [Vehicle App SDK Overview](https://websites.eclipseprojects.io/velocitas/docs/about/development_model/vehicle_app_sdk/)

## Quickstart Tutorials
1. [Setup and Explore Development Enviroment](https://websites.eclipseprojects.io/velocitas-docs/docs/tutorials/quickstart/)
1. [Develop your own Vehicle Model](https://websites.eclipseprojects.io/velocitas/docs/tutorials/tutorial_how_to_create_a_vehicle_model/)
1. [Develop your own Vehicle App](https://websites.eclipseprojects.io/velocitas/docs/tutorials/vehicle-app-development/)

## Contribution
- [GitHub Issues](https://github.com/eclipse-velocitas/vehicle-app-cpp-template/issues)
- [Mailing List](https://accounts.eclipse.org/mailing-list/velocitas-dev)
- [Contribution](CONTRIBUTING.md)

## Troubleshooting

### Manually installing dependencies
All dependencies of the application should be downloaded and installed automatically once the VSCode DevContainer is created. Should this process fail for whatever reason, you can trigger the manual installation this command:
```bash
./install_dependencies.sh
```