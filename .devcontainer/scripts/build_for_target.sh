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

rm -rf ./build

APP_NAME=$(cat $(cat .velocitas.json | jq -r .variables.appManifestPath) | jq -r .name)

velocitas exec build-system install -x arm64 -r
velocitas exec build-system build -x arm64 -t app -r

# workaround: rename app binary according to app manifest
mv ./build/bin/app ./build/bin/${APP_NAME}
