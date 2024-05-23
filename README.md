# Vehicle App C++ Template

![Template CI Workflow](https://github.com/SoftwareDefinedVehicle/vehicle-app-cpp-template-lattice/actions/workflows/ci.yml/badge.svg)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)


## Original project / OSS stream

The Vehicle App Template for C++ allows to create `Vehicle Apps` from the [Velocitas](https://github.com/eclipse-velocitas/velocitas-docs) development model in the C++ programming language.

## EDGE / enterprise variant

In addition to the original Velocitas Vehicle App template, this EDGE / enterprise variant allows creation of `Vehicle Apps` for our Lattice based enterprise EDGE distribution, allowing access to platform services such as:

* State Management
* Persistence Store
* Cloud Connector Service
* Logger

These APIs are made available through extensions to the Velocitas SDK.

## Prerequisites to use the Vehicle App template

* Visual Studio Code is installed on your developer PC
* A supported container runtime is available on your developer PC (Docker, Podman)
* An account on [Bosch Development Cloud Artifactory](https://artifactory.boschdevcloud.com/) with appropriate permissions. See [SETUP](./SETUP.md) on how to request the access.

## Folder structure

* 📁 `.devcontainer`- Setup and configuration for the Visual Studio Code IDE's development container feature
* 📁 `.github` - Workflows, actions and templates for usage of the repository on the Github (Enterprise) platform
* 📁 `.vscode` - Setup and configuration for the Visual Studio Code IDE
* 📁 `app` - base directory for a vehicle app
    * 📁 `src` - source code of the vehicle app
    * 📁 `tests` - tests for the vehicle app

## Building

### Building the App
To build the App, run the build entry point from within the development container, **after a successful run of** `velocitas init`

1. Initialize the development environment
    ```bash
    velocitas init
    ```
2. Install dependencies and build, using one of these command combinations:
    * Velocitas toolchain abstraction (recommended)
        ```bash
        velocitas exec build-system install
        velocitas exec build-system build
        ```
    * Python scripts
        ```bash
        python3 ./install_deps.py
        python3 ./build.py
        ```

## Starting the runtime

Open the `Run Task` view in VSCode and select `Local Runtime - Up`.

## Launching the example
With the runtime running in the background, you can run the app.
The app must have been build before (see above).

### Without debugging

Open the `Run Task` view in VSCode and select `Local Runtime - Run VehicleApp`.

### With debugging
You can simply launch the example in the Debugging Tab. Make sure the `VehicleApp - Debug (Native)` is selected at the top. After the selection is done, you can also simply hit `F5`, to start the debugging session.

*Note: This launch task will also make sure to re-build the app if it has been modified!*

### Run App as Docker container

1. Build the app
    ```bash
    docker build -f app/Dockerfile -t vehicleapp:local 
    ```
2. Run it
    ```bash
    docker run --rm -it --net="host" \
        -e SDV_MIDDLEWARE_TYPE="native" \
        -e SDV_MQTT_ADDRESS="localhost:1883" \
        -e SDV_VEHICLEDATABROKER_ADDRESS="localhost:55555" \
        -e FEATURE_CONFIG="/feature.config" \
        -v $(pwd)/app/feature.config.py:/feature.config \
        vehicleapp:local
    ```

## Running in GitHub Codespaces
GitHub Codespaces currently restrict the token that is used within the Codespace to just the current repository. Working on cloned repositories or
submodules will not be possible without further setup. To work on other repos, you need to create a personal access token (PAT) [here](https://github.com/settings/tokens/new) which has full "repo" access. Copy the contents of the PAT and create a Codespace secret called `MY_GH_TOKEN` and paste the content of your PAT. Finally you need to give the Codespace secret access to the repository of the Codespace, in this case `vehicle-app-cpp-template`.

## Documentation
* [Velocitas Development Model](https://eclipse.dev/velocitas/docs/concepts/development_model/)
* [Vehicle App SDK Overview](https://eclipse.dev/velocitas/docs/concepts/development_model/vehicle_app_sdk/)

## Quickstart Tutorials
1. [Setup and Explore Development Environment](https://eclipse.dev/velocitas/docs/tutorials/quickstart/)
1. [Develop your own Vehicle Model](https://eclipse.dev/velocitas/docs/tutorials/vehicle_model_creation/)
1. [Develop your own Vehicle App](https://eclipse.dev/velocitas/docs/tutorials/vehicle_app_development/)

## Contribution
- [GitHub Issues](https://github.com/eclipse-velocitas/vehicle-app-cpp-template/issues)
- [Mailing List](https://accounts.eclipse.org/mailing-list/velocitas-dev)
- [Contribution](CONTRIBUTING.md)

## Troubleshooting

### Manually installing dependencies
All dependencies of the application should be downloaded and installed automatically once the VSCode DevContainer is created. Should this process fail for whatever reason, you can trigger the manual installation this command:
```bash
velocitas exec build-system install
```
