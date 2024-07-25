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

FROM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:v0.3

# The name of the repo, usually the project name, that is used by the devContainer
# to create a directory under /workspace/<REPO_NAME>
ARG REPO_NAME=vehicle-app-cpp-template-lattice

USER vscode:vscode
COPY --chown=vscode:vscode . /workspaces/${REPO_NAME}

WORKDIR /workspaces/${REPO_NAME}
# Download all components and pre-heat Velocitas caches
RUN bash ./.devcontainer/scripts/onCreateCommand.sh && conan remove "*/*" -fs && conan user --clean \
    && conan remote remove sdv-bgsw-conan-virtual && conan remote disable conancenter
WORKDIR /

# clear project files
RUN rm -rf /workspaces/${REPO_NAME}

ENV VELOCITAS_OFFLINE=true

# switch back to root user to make devContainers happy
USER root
