#!/bin/bash
# Copyright (c) 2022 Robert Bosch GmbH
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

SDV_EXAMPLES_PATH="./sdk/examples"

if [[ `git status --porcelain` ]]; then
  echo "####################### WARNING #######################"
  echo "####  Please commit or stash your changes before   ####"
  echo "####  importing the example app.                   ####"
  echo "####  Otherwise all changes will be discarded!     ####
  "
  echo "####################### WARNING #######################"
else
  rm -rf app/ && \
  cp -a $SDV_EXAMPLES_PATH/$@ app && \
  cp -a $SDV_EXAMPLES_PATH/$@/conanfile.txt . && \
  ./install_dependencies.sh
  echo "#######################################################"
  echo "Successfully imported $@"
  echo "#######################################################"
fi
