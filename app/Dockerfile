# Copyright (c) 2022-2023 Robert Bosch GmbH
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

FROM ghcr.io/eclipse-velocitas/vehicle-app-cpp-sdk:v0.3.1 as builder

RUN apk update && \
    apk add ninja && \
    apk add cmake && \
    apk add clang-extra-tools && \
    apk add python3 && \
    apk add py3-pip && \
    apk add build-base && \
    apk add linux-headers && \
    apk add perl && \
    apk add bash && \
    apk add git && \
    pip3 install "conan==1.58"

COPY . /app

RUN --mount=type=cache,target=/root/.conan

RUN cd /app && \
    ./install_dependencies.sh -r && \
    ./build.sh -r -t app --static

RUN strip /app/build/bin/app

# Runner stage, to copy the executable
FROM scratch

COPY --from=builder /app/build/bin/app /dist/app

WORKDIR /tmp
WORKDIR /dist

ENV PATH="/dist:$PATH"

CMD ["/dist/app"]
