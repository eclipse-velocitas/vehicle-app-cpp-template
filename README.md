# Vehicle App C++ Template

![Template CI Workflow](https://github.com/SoftwareDefinedVehicle/vehicle-app-cpp-template-lattice/actions/workflows/ci.yml/badge.svg)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)


## Original project / OSS stream

This project is based on the open source repository [Vehicle App C++ Template](https://github.com/eclipse-velocitas/vehicle-app-cpp-template). Generally, it follows the same approach and principles, hence please refer to the [OSS documentation repository](https://github.com/eclipse-velocitas/velocitas-docs) / [official docs](https://eclipse.dev/velocitas/) until noted otherwise.

## EDGE / enterprise variant

In addition to what is provided in the original Velocitas Vehicle App template, this EDGE / enterprise variant allows creation of `Vehicle Apps` for the ETAS enterprise EDGE distribution, allowing access to platform services such as:

* State Management - *not yet available*
* Persistence Store - *not yet available*
* Cloud Connector Service - *see `nevonex::cloud::Cloud::uploadData`*
* Logger - *see usage of `APP_LOG` macro in SampleApp*

These APIs are made available through extensions to the Velocitas C++ SDK (see entry `lattice-extensions` in `conanfile.txt`).

:warning: APIs for EDGE services are not yet finalized and may change!

## Prerequisites to use the Vehicle App template (Recommended/ONLINE VERSION)

:warning: The following items are <span style="color:red">**mandatory**</span>. Without the following prerequisites, no support can be given when using the template.

* General internet access
* Access to https://github.com, https://pypi.org, https://conan.io/center
    * These can be configured to use mirrors instead, see [SETUP](./docs/SETUP.md).
* Visual Studio Code is installed on your developer PC with the `Dev Containers` extension installed.
* A supported container runtime is available on your developer PC. Recommended is Docker Desktop. For installation and usage of alternative runtimes, refer to the [documentation](https://eclipse.dev/velocitas/docs/tutorials/quickstart/container_runtime/).
* **ONLINE VERSION ONLY:** An account on [Bosch Development Cloud Artifactory](https://artifactory.boschdevcloud.com/) with appropriate permissions. See [SETUP](./docs/SETUP.md) on how to request the access.
* **ONLINE VERSION ONLY:** A *manually created* `.crendentials` file located next to this README (root of the project) - this is going to contain user-specific credentials and hence is exluded from versioning. Refer to [SETUP](./docs/SETUP.md) to learn how to create the file.  

### Fallback: OFFLINE version

In special cases, no online connection might be available or connection to Bosch Development Cloud might not be possible. Therefore, the project also builds a pure offline version which comes pre-equipped with all dependencies to start developing your app on your local PC. To obtain such a build have a look at the provided artifacts or, if possible, access build artifacts of the [localversion workflow](https://github.com/SoftwareDefinedVehicle/vehicle-app-cpp-template-lattice/actions/workflows/localversion.yml).

Once the artifact has been obtained, please have a look at the [LOCAL SETUP](./.devcontainer/localversion/LOCAL_SETUP.md) to get started.

## Folder structure

* 📁 `.devcontainer`- Setup and configuration for the Visual Studio Code IDE's development container feature
* 📁 `.github` - Workflows, actions and templates for usage of the repository on the Github (Enterprise) platform
* 📁 `.vscode` - Setup and configuration for the Visual Studio Code IDE
* 📁 `app` - base directory for a vehicle app
    * 📁 `src` - source code of the vehicle app
    * 📁 `tests` - tests for the vehicle app

## Development

This repository contains a [quickstart guide](./docs/DEVELOPMENT.md) to enable you to start writing an app immediately. For a more in-depth guide, refer to the [official documentation](https://eclipse.dev/velocitas/docs/tutorials/vehicle_app_development/cpp_development/).

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
        velocitas exec build-system install -r
        velocitas exec build-system build
        ```
    * Python scripts
        ```bash
        python3 ./install_deps.py -r
        python3 ./build.py
        ```
    * Bash scripts
        ```bash
        ./install_dependencies.sh -r
        ./build.sh
        ```

## Starting the runtime

Open the `Run Task` view in VSCode and select `Local Runtime - Up`.

## Launching the example

With the runtime running in the background, you can run the app.
The app must have been build before (see above).

### With debugging

You can simply launch the example in the Debugging Tab. Make sure the `VehicleApp - Debug (Native)` is selected at the top. After the selection is done, you can also simply hit `F5`, to start the debugging session.

:warning: *Note: This launch task will also make sure to re-build the app if it has been modified!*

### Run App as Docker container

1. Build the app
    ```bash
    docker build -f app/Dockerfile -t vehicleapp:local .
    ```
2. Run it
    ```bash
    docker run --rm -it --net="host" \
        -e SDV_MIDDLEWARE_TYPE="native" \
        -e SDV_MQTT_ADDRESS="localhost:1883" \
        -e SDV_VEHICLEDATABROKER_ADDRESS="localhost:55555" \
        -e FEATURE_CONFIG="/feature.config" \
        -v $(pwd)/app/feature.config:/feature.config \
        vehicleapp:local
    ```

### Build for linux arm64 target device

To build a native app for an linux arm64 device you have 2 options:

* In VSCode do `View` → `Command Palette...` → `Tasks: Run Task` → `Build app for target`

**or**

* In terminal run `./.devcontainer/scripts/build_for_target.sh`

The resulting native binary will be output to `build/bin` and will be named after the `name` specified in your `app/AppManifest.json`

## Running in GitHub Codespaces

GitHub Codespaces currently restrict the token that is used within the Codespace to just the current repository. Working on cloned repositories or
submodules will not be possible without further setup. To work on other repos, you need to create a personal access token (PAT) [here](https://github.com/settings/tokens/new) which has full "repo" access. Copy the contents of the PAT and create a Codespace secret called `MY_GH_TOKEN` and paste the content of your PAT. Finally you need to give the Codespace secret access to the repository of the Codespace, in this case `vehicle-app-cpp-template-lattice`.

## Documentation

* [Developing a Vehicle App](./docs/DEVELOPMENT.md)
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

### Delete all Velocitas packages and settings to have a clean start
```bash
rm -rf ~/.velocitas
```

### Manually initialize Velocitas components

All specified components should be initialized automatically when the devcontainer starts. However you can also trigger this manually again in case of any error:
```bash
velocitas init -v
```
`-v` is added to get more logs in case you have to debug an error.

### Manually installing dependencies

All dependencies of the application should be downloaded and installed automatically once the VSCode DevContainer is created. Should this process fail for whatever reason, you can trigger the manual installation this command:
```bash
velocitas exec build-system install -r
```

## FAQ

**Q:** Why am I getting an InvalidValueException when I try to get the value of a signal/data point by calling the `.value()` function?<br>
**A:** The current state of a signal/data point might not always represent a valid value, but could be in some failure state. You'll find possible [failure reasons](https://eclipse.dev/velocitas/docs/tutorials/vehicle_app_development/cpp_development/#failure-reasons) and suggestions for a [failure handling](https://eclipse.dev/velocitas/docs/tutorials/vehicle_app_development/cpp_development/#failure-handling) in the 
[Velocitas tutorial for C++ Vehicle App Development](https://eclipse.dev/velocitas/docs/tutorials/vehicle_app_development/cpp_development/).

**Q:** Why am I getting an AsyncException while I'm waiting for the outcome of getting or setting signal values using the `.await()` fucntion?<br>
**Q:** Why am I getting an AsyncException while I'm waiting for the next update of a subscription using the `.next()` fucntion?<br>
**A:** This will happen if there is an communication issue between your app and the data broker, e.g. because the broker is not yet started or some networking issue did occur. See section [Failure Handling](https://eclipse.dev/velocitas/docs/tutorials/vehicle_app_development/cpp_development/#failure-handling) of the Velocitas Documentation.

**Q:** I've subscribed multiple signals/data points and now I'm getting always the state of all signals/data points in an update notification, instead of just those one where the state did change. Why?<br>
**A:** This data broker will always bundle the states of all signals/data points selected in the single subscription. If you don’t want this behaviour, you must subscribe to change notifications for each signal/data point separately.
