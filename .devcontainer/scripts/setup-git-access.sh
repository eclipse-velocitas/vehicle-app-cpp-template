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

if [[ "${GITHUB_TOKEN}" != "" || -e ".github_token" ]]; then
    if [ -z "${GITHUB_TOKEN}" ]; then
        GITHUB_TOKEN=$(cat .github_token)
    fi

    echo "Using Github access token"

    git config --global credential.helper store
    echo "https://user:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
fi
