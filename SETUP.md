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
