# Copyright (c) 2022-2025 Contributors to the Eclipse Foundation
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

FROM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:v0.4 AS builder

COPY . /workspace

WORKDIR /workspace

RUN pip install -r requirements.txt && \
    velocitas init -f -v && \
    ./install_dependencies.sh -r && \
    ./build.sh -r -t app --static

# Runner stage, to copy the executable
FROM scratch AS runner

COPY --from=builder /workspace/build/bin/app /app

WORKDIR /tmp

ENV PATH="/:$PATH"

CMD ["/app"]
