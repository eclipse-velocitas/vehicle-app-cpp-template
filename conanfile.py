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

import os

from conan import ConanFile
from conan.tools.cmake import cmake_layout


class VehicleAppCppSdkConan(ConanFile):
    name = "vehicle-app"
    license = "Apache-2.0"
    url = "https://github.com/eclipse-velocitas/vehicle-app-cpp-template"
    requires = [
        ("fmt/11.1.1"),
        ("nlohmann_json/3.11.3"),
        ("vehicle-model/generated"),
        ("vehicle-app-sdk/bjoern_conan2"),
    ]
    generators = "CMakeDeps", "CMakeToolchain"
    author = "Robert Bosch GmbH"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        os = str(self.settings.os).lower()
        arch = str(self.settings.arch).lower()
        if arch == "armv8":
            arch = "aarch64"
        cmake_layout(
            self,
            src_folder=".",
            build_folder=f"build-{os}-{arch}",
        )
