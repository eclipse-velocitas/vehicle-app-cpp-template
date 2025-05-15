# Vehicle App C++ Template

![Template CI Workflow](https://github.com/eclipse-velocitas/vehicle-app-cpp-template/actions/workflows/ci.yml/badge.svg)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)

The Vehicle App Template for C++ allows to create `Vehicle Apps` from the [Velocitas](https://github.com/eclipse-velocitas/velocitas-docs) development model in the C++ programming language.

> [!IMPORTANT]
> We successfully migrated our C++ repositories to use version 2 of the [Conan package manager](https://conan.io/).
> Unfortunately, those changes are not backwards compatible. So, please be aware that recent versions of this C++ app template repository
> (everything since the `conan2` tag) require usage of the [Velocitas C++ SDK](https://github.com/eclipse-velocitas/vehicle-app-cpp-sdk) >= 0.7.0,
> packages [devcontainer-setup](https://github.com/eclipse-velocitas/devenv-devcontainer-setup) >= v3 and
> [github-workflows](https://github.com/eclipse-velocitas/devenv-github-workflows) >= v7, and
> [base images](https://github.com/eclipse-velocitas/devcontainer-base-images) >= v0.4.
>
> If you like to migrate older app repositories created from this template before Conan 2,
> please have a look at the [Conan 2 migration guide](#migrate-older-app-repositories-to-conan-2) below.

## Folder structure

* 📁 `app` - base directory for a vehicle app
    * 📁 `src` - source code of the vehicle app
    * 📁 `tests` - tests for the vehicle app

## Building

### Building the App
To build the App, run the build script:
```bash
./build.sh
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
```bash
docker run --rm -it --net="host" -e SDV_MIDDLEWARE_TYPE="native" -e SDV_MQTT_ADDRESS="localhost:1883" -e SDV_VEHICLEDATABROKER_ADDRESS="localhost:55555" localhost:12345/vehicleapp:local
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
./install_dependencies.sh
```

### Migrate older app repositories to Conan 2
If you have app repositories created from this template basing on Conan 1 and you like to migrate them to the
latest state/Conan 2, here are some hints how to achieve that:

1. You should run `velocitas upgrade --ignore-bounds` and upgrade packages
   * `devenv-github-workflows` to a version >= v7.0.0 and
   * `devenv-devcontainer-setup` to a version >= v3.0.0.

   This will migrate the base image and required Velocitas components to Conan 2.
2. Run `velocitas sync` to automatically update some local files.
3. You should make sure to update the cli-version to something recent (>= 13.2).
   Set the version in `.velocitas.json`.

Now some local files need to be updated manually:
1. `conanfile.txt`:

   In the `[requires]` section:
   * Make sure you are referencing all packages used by the app directly.
     Don't rely on indirect requirements provide by e.g. the C++ SDK:
     ```diff
     [requires]
     +fmt/11.1.1
     +nlohmann_json/3.11.3
     ```
     Update the SDK to a version >= 0.7.0:
     ```diff
     vehicle-app-sdk/0.7.0
     ```
     In the `[generators]` section replace `cmake` as follows:
     ```diff
     [generators]
     -cmake
     +CMakeDeps
     +CMakeToolchain
     ```
2. Python `requirements.in`: Upgrade Conan to version 2
   ```diff
   -conan==1.x.y
   +conan>=2,<3
   ```
   Update `requirements.txt` using `pip-compile requirements.in`
3. `.pre-commit-config.yaml`: You should modify the suppression for the build folder:
   ```diff
   -"--suppress=*:build/*",
   +"--suppress=*:build*/*",
   ```
4. `.gitignore`: Add an entry to ignore `CMakeUserPresets.json` files
   ```diff
   +CMakeUserPresets.json
   ```
5. `app/Dockerfile` - if you are using containerized apps:
   * Update the base-image:
     ```diff
     -FROM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:v0.3 as builder
     +FROM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:v0.4 AS builder
     ```
     You can remove the Conan 1 environment variable (no replacement needed):
     ```diff
     -ENV CONAN_USER_HOME /home/vscode/
     -
     ```
6. Now comes the - potentially - tricky part: Update the `CMakelist.txt` files.
   Instead of referencing all packages pulled in via Conan using the cmake variable
   `CONAN_LIBS` the dependent package now need to be found one by one via `find_package`.
   For migration it's best if you compare the changes in the `CMakeLists.txt` files of
   this repository between the commit tagged with `conan2` and the commit before that
   and take over the required changes.

> [!NOTE]
>
> If you are using a `conanfile.py` instead of the `conanfile.txt` variant, here are some hints:
> * The Python file variant is not supported by the Velcitas tooling (especially the gPRC interface tools)!
> * Make sure you don't configure `cmake_layout` in the layout section:
>   This will conflict with the build script provieded by component `build-system`.
