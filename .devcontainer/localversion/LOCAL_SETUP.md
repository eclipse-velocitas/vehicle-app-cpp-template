# Local version of Velocitas Vehicle App C++ template

A locally usable snapshot of the vehicle app template.

## Prerequisites

Prerequisites are the same to the regular version but without the requirement to have an internet connection.

1. VSCode installed
2. Container engine/runtime (e.g. Docker desktop, Podman, ...)
3. Unarchiver for TAR files (e.g. tar for Linux)

## Setup

Follow these steps to set up your local development environment:

1. Download the `devenv-local-linux_<desired developer PC architecture>.tar` artifact from a release.
1. Create an empty directory: `vehicle-app-cpp-template-lattice`
   ```shell
   mkdir vehicle-app-cpp-template-lattice
   ```
1. Unpack the archive contents using your preferred unpackaging tool (e.g. `tar` on linux) into the directory `vehicle-app-cpp-template-lattice`
   ```shell
   cd vehicle-app-cpp-template-lattice
   tar -xvf /path/to/devenv-local-linux_<arch>.tar
   ```
1. Now you should have the following folder structure

   ```shell
   vehicle-app-cpp-template-lattice
    ├── CMakeLists.txt
    ├── CODE_OF_CONDUCT.md
    ├── CONTRIBUTING.md
    ├── CPPLINT.cfg
    ├── LICENSE
    ├── NOTICE-3RD-PARTY-CONTENT.md
    ├── NOTICE.md
    ├── README.md
    ├── SECURITY.md
    ├── app
    ├── build.py
    ├── build.sh
    ├── conanfile.txt
    ├── docs
    ├── gcovr.cfg
    ├── install_dependencies.sh
    ├── install_deps.py
    ├── license_header.txt
    ├── localimage.tar
    ├── mock.py
    ├── reconfigure_template_urls.sh
    ├── requirements.txt
    └── whitelisted-licenses.txt
   ```

1. Import the local container image to your container runtime's images:
   ```shell
   docker load -i localimage.tar
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
1. Happy developing!

## Using the devcontainer

If you want to build a local version of the app container you need to load the localimage again into the docker cache.
Execute the following command inside the devcontainer:

```bash
docker load -i localimage.tar
```
