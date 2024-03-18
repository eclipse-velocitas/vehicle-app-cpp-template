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

FROM --platform=$BUILDPLATFORM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:v0.2 as builder
ARG TARGETARCH

ENV CONAN_USER_HOME /home/vscode/

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y jq sudo curl wget git cmake build-essential \
    gcc-aarch64-linux-gnu g++-aarch64-linux-gnu binutils-aarch64-linux-gnu \
    gcc-x86-64-linux-gnu g++-x86-64-linux-gnu binutils-x86-64-linux-gnu && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY . /workspace

# FIXME: For build tooling we only need "devenv-devcontainer-setup", we should be able to
# filter this without manual jq intervention...
RUN mv /workspace/.velocitas.json /workspace/.velocitas_org.json && \
    cat /workspace/.velocitas_org.json | jq 'del(.packages[] | select(.name != "devenv-devcontainer-setup"))' > /workspace/.velocitas.json

WORKDIR /workspace

RUN velocitas init -f -v && \
    ./install_dependencies.sh -r -x $TARGETARCH && \
    ./build.sh -r -t app --static -x $TARGETARCH


# Intermediate stage to delete unused executable
FROM --platform=$TARGETPLATFORM bash:latest as mover
COPY --from=builder /workspace/build/bin/app_* /
COPY ./utils/delete.sh /delete.sh
CMD ["bash", "/delete.sh $TARGETPLATFROM"]

# Runner stage, to copy the executable
FROM scratch
COPY --from=mover /app_* /dist/app

WORKDIR /tmp
WORKDIR /dist

ENV PATH="/dist:$PATH"

CMD ["/dist/app"]
