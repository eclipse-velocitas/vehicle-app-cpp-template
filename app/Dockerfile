# Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
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

# syntax = docker/dockerfile:1.2

FROM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:v0.2 as builder

COPY . /workspace

ENV CONAN_USER_HOME /home/vscode/

# FIXME: For build tooling we only need "devenv-devcontainer-setup", we should be able to
# filter this without manual jq intervention...
RUN mv /workspace/.velocitas.json /workspace/.velocitas_org.json && \
    cat /workspace/.velocitas_org.json | jq 'del(.packages[] | select(.name != "devenv-devcontainer-setup"))' > /workspace/.velocitas.json

WORKDIR /workspace

RUN velocitas init -f -v && \
    ./install_dependencies.sh -r && \
    ./build.sh -r -t app --static

RUN strip /workspace/build/bin/app

# Runner stage, to copy the executable
FROM scratch

COPY --from=builder /workspace/build/bin/app /dist/app

WORKDIR /tmp
WORKDIR /dist

ENV PATH="/dist:$PATH"

CMD ["/dist/app"]
