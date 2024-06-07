# Setup

# Access to BDC artifactory

Please follow the steps below to setup your environment

1. Please Raise a IDM request via the [Bosch IDM Portal](https://rb-im.bosch.com/BOAWeb/pages/selfservice/selfservice-roles.xhtml) to access the repo – for role - `BDC_Artifactory_01_perm400_user`
1. Once the request is done, go to https://artifactory.boschdevcloud.com/ and click the Button "SAML SSO" on the bottom
1. Go to the artifacts (menu on the left side)
1. Filter for `sdv-bgsw-conan-virtual`
1. Click on the Button "Set me up" in the top right corner
1. In the configure-tab click on "Generate Token & Create Instructions"
1. Copy the token
1. In the repository's root folder create a file called `.credentials` with following content:
    ```
    CONAN_REMOTE_USER=<nt-user-id>
    CONAN_REMOTE_TOKEN=<your-token>
    ```
1. In order to use the container images on artifactory you need to login to the registry:
    ```bash
    docker login -u <nt-user-id> -p <your-token> artifactory.boschdevcloud.com
    ```
1. Reopen the folder in a container

After performing the above steps, the basic setup is now done.

# Tailoring the template

If you want to, you can customize your setup to fully fit your needs.

## Configuring mirrors and URLs

### Velocitas toolchain packages

The project configuration file `.velocitas.json` contains soft references to repositories on Github.com via the `packages` object:

```json
{
    "packages": {
        "devenv-runtimes": "v4.0.1",
        "devenv-github-workflows": "v6.0.2",
        "devenv-github-templates": "v1.0.5",
        "devenv-devcontainer-setup": "v2.4.0"
    },
    <...>
}
```

Unless the key of the package contains a fully qualified URL, the key will resolve to `https://github.com/eclipse-velocitas/<key>.git`.

In case you have set-up your own mirrors of the packages, you can reference those mirrors by providing fully qualified URLs:

e.g.
```json
{
    "packages": {
        "https://github.com/SoftwareDefinedVehicle/devenv-runtimes.git": "v4.0.1",
        "https://github.com/SoftwareDefinedVehicle/devenv-github-workflows.git": "v6.0.2",
        "https://github.com/SoftwareDefinedVehicle/devenv-github-templates.git": "v1.0.5",
        "https://github.com/SoftwareDefinedVehicle/devenv-devcontainer-setup.git": "v2.4.0"
    },
    <...>
}
```

### Project variables

There are also several project variables which can be set in the `.velocitas.json`. Here are some examples:

| Variable | Purpose  | Example |
|:---------|:--------|--------|
| `gitLocation` | Base Git location to be used instead of `https://github.com/eclipse-velocitas` for ALL git references which are not configurable elsewhere. | `https://github.com/SoftwareDefinedVehicle`
| `mqttBrokerImage` | URL of a custom MQTT Broker Docker Container | `registry.hub.docker.com/library/eclipse-mosquitto:2.0.14`
| `vehicleDatabrokerImage` | URL of a custom Databroker Docker Container | `ghcr.io/eclipse-kuksa/kuksa-databroker:0.4.4`
| `mockServiceImage` | URL of a custom Mockservice Docker Container | `ghcr.io/eclipse-kuksa/kuksa-mock-provider/mock-provider:0.4.0`,
| `sdkGitRepo` | Git-URL of a custom Vehicle SDK which shall be used instead of `https://github.com/eclipse-velocitas/vehicle-app-cpp-sdk.git` | `https://github.com/SoftwareDefinedVehicle/vehicle-app-cpp-sdk.git`

An exhaustive list of all possible project variables can be obtained by executing `velocitas package` in a terminal or by looking at the manifest files of the used Velocitas packages.

This project contains a convenience script which can be executed to configure needed variables.

* **Reconfigure template URLs**

    1. Open the `reconfigure_template_urls.sh` script.
    1. Adapt all the variables in the marked area (`GIT_FORK_LOCATION`, `PIP_MIRROR`, `BASE_IMAGE_URL`, `VSS_PATH`, `MQTT_IMAGE`, `DATABROKER_IMAGE`, `MOCKSERVICE_IMAGE`).
    1. Execute the script from a Linux host (tested under Ubuntu). This host may be a VM or DevContainer.
        ```shell
        ./reconfigure_template_urls.sh
        ```

## Configuring Vehicle mock behavior

A customized `mock.py` is already part of this repository, feel free to adapt it to the needs of your app.
It uses a Python based DSL to describe the mocking behavior. Refer to the [KUKSA mock provider documentation](https://github.com/eclipse-kuksa/kuksa-mock-provider) for details.
