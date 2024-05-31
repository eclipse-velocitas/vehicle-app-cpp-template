# Local version of Velocitas Vehicle App C++ template

A locally usable snapshot of the vehicle app template.

## Prerequisites

Prerequisites are the same to the regular version but without the requirement to have an internet connection.

1. VSCode installed
2. Container engine/runtime (e.g. Docker desktop, Podman, ...)
3. Unarchiver for ZIP files (e.g. unzip for Linux)

## Setup

Follow these steps to set up your local development environment:

1. Download the `devenv-local-<desired developer PC architecture>` artifact from a release.
1. Unpack the archive contents using your preferred unzip tool (e.g. `unzip` on linux) into the directory `vehicle-app-cpp-template-lattice`
    ```shell
    unzip devenv-local-linux_<arch>.zip -d vehicle-app-cpp-template-lattice
    ```
1. Import the local container image to your container runtime's images:
    ```shell
    docker load -i vehicle-app-cpp-template-lattice/localimage.tar
    ```
1. Open VSCode
1. Open the directory `vehicle-app-cpp-template-lattice` in VSCode
1. When prompted to start the directory in a dev container, click yes.
1. Once the devContainer has started up successfully, it is recommended to initialize a new git repository to track your changes:
   ```shell
   git init
   git add .
   git commit -m "Initial version"
   ```
2. Happy developing!

## Using the devcontainer

If you want to build a local version of the app container you need to load the localimage again into the docker cache.
Execute the following command inside the devcontainer:
```bash
docker load -i localimage.tar
```
