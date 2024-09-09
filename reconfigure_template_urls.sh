#!/bin/bash

# Copyright (c) 2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

############################################################################################################
## Replace the following values
# The repositories have to exist already at the desired git location
GIT_FORK_LOCATION="https://github.com/USER"
GIT_REPO_NAME_PREFIX="" # optional repository name prefix to differentiate between OSS repo and fork repo
PIP_MIRROR="https://pypi.org/simple"
BASE_IMAGE_URL="ghcr.io/eclipse-velocitas/devcontainer-base-images"
VSS_PATH="https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.0/vss_rel_4.0.json"
MQTT_IMAGE="registry.hub.docker.com/library/eclipse-mosquitto:2.0.14"
DATABROKER_IMAGE="ghcr.io/eclipse-kuksa/kuksa-databroker:0.4.4"
MOCKSERVICE_IMAGE="ghcr.io/eclipse-kuksa/kuksa-mock-provider/mock-provider:0.4.0"
############################################################################################################

################################## ! No need to touch ! ####################################################
export DEVCONTAINER_SETUP_FORK_URL=$GIT_FORK_LOCATION/${GIT_REPO_NAME_PREFIX}devenv-devcontainer-setup.git
export RUNTIMES_FORK_URL=$GIT_FORK_LOCATION/${GIT_REPO_NAME_PREFIX}devenv-runtimes.git
############################################################################################################

# update pip mirror before velocitas init
pip_host=$(echo "$PIP_MIRROR" | awk -F/ '{print $3}')
pip_config="pip config set global.index-url $PIP_MIRROR\\
pip config set install.trusted-host $pip_host\\
pip install --upgrade pip --no-cache-dir\\n"

custom_vars="        \"gitLocation\": \"$GIT_FORK_LOCATION\", \\
    \"mqttBrokerImage\": \"$MQTT_IMAGE\", \\
    \"vehicleDatabrokerImage\": \"$DATABROKER_IMAGE\", \\
    \"mockServiceImage\": \"$MOCKSERVICE_IMAGE\","

echo "Updating onCreateCommand.sh"
# Use alternative pip server, only for online mode
on_create_path=$(find . -name "onCreateCommand.sh")
pip_update_marker="# PIP_EXTRA_CONFIG"
sed -i "s+$pip_update_marker+$pip_config\\n+g" "$on_create_path"

# update base image URL
echo "Updating Dockerfiles"
dockerfiles=$(find . -name "Dockerfile")
for file in $dockerfiles; do
    sed -i "s+ghcr.io/eclipse-velocitas/devcontainer-base-images+$BASE_IMAGE_URL+g" "$file"
done

echo "Updating devcontainer.json"
devcontainer_path=$(find . -name "devcontainer.json")
sed -i '/"postStartCommand": "bash \.devcontainer\/scripts\/upgrade-cli\.sh"/d' "$devcontainer_path"

echo "Updating .velocitas.json"
velocitas_path=$(find . -name ".velocitas.json")
sed -i "s+\"devenv-runtimes\"+\"$RUNTIMES_FORK_URL\"+g" "$velocitas_path"
sed -i "s+\"devenv-devcontainer-setup\"+\"$DEVCONTAINER_SETUP_FORK_URL\"+g" "$velocitas_path"
sed -i "/devenv-github-workflows/d" "$velocitas_path"
sed -i "/devenv-github-templates/d" "$velocitas_path"
sed -i "s+\"repoType\": \"app\",+\"repoType\": \"app\",\\n$custom_vars+g" "$velocitas_path"
jq 'del(.components)' "$velocitas_path" > "$velocitas_path".tmp && mv "$velocitas_path".tmp "$velocitas_path"

echo "Removing .velocitas-lock.json"
velocitas_lock_path=$(find . -name ".velocitas-lock.json")
rm "$velocitas_lock_path"

echo "Updating AppManifest.json"
appmanifest_path=$(find . -name "AppManifest.json")
sed -i "s+https://github.com/COVESA/vehicle_signal_specification/releases/download.*.json+$VSS_PATH+g" "$appmanifest_path"
