Please follow the steps below to setup your environment

1. Please Raise a IDM request to access the repo – for Role - BDC_Artifactory_01_perm400_user
1. Once the request is done, go to https://artifactory.boschdevcloud.com/ and click the Button "SAML SSO" on the bottom
1. Go to the artifacts and search for "sdv-bgsw-conan-virtual"
1. click on the Button "Set me up" in the top right corner
1. in the configure-tab click on "Generate Token $ Create Instructions"
1. copy the token, your user-id is your NT-User
1. in the repository create file called .credentials with following content:
    CONAN_REMOTE_USER=<nt-user>
    CONAN_REMOTE_TOKEN=<your-token>
1. Reopen the folder in a container

The basic setup is done after these steps.

If you want to, you can even customize your setup to fully fit your needs.
A customized mock.py is already part of this repository, feel free to adapt it to your app.
There are also several variables which can be set in the velocitas.json, e.g.
 - mqttBrokerImage (Url of a custom MQTT Broker Docker Container)
 - vehicleDatabrokerImage (Url of a custom Databroker Docker Container)
 - mockServiceImage (Url of a custom Mockservice Docker Container)
 - sdkGitRepo (Git-Url of a custom Vehicle SDK, needs to be referenced in the requirements-file)

You can find all possible variables in the manifests of the Velocitas packages.
