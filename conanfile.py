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
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout


class VehicleAppCppSdkConan(ConanFile):
    name = "vehicle-app"
    license = "Apache-2.0"
    url = "https://github.com/eclipse-velocitas/vehicle-app-cpp-template"
    requires = [
        ("fmt/11.1.1"),
        ("nlohmann_json/3.11.3"),
        ("vehicle-model/generated"),
        ("vehicle-app-sdk/rebased_conan2"),
    ]
    generators = "CMakeDeps"
    author = "Robert Bosch GmbH"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "STATIC_BUILD": ["ON", "OFF"],
        "COVERAGE": ["ON", "OFF"],
        "BUILD_TARGET": ["ANY"],
        "BUILD_ARCH": ["ANY"],
        "HOST_ARCH": ["ANY"],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "STATIC_BUILD": "OFF",
        "COVERAGE": "OFF",
        "BUILD_TARGET": "all",
        "BUILD_ARCH": os.uname().machine,
        "HOST_ARCH": os.uname().machine,
    }

    def config_options(self):
        # self.options.shared = self.options.STATIC_BUILD == "OFF"
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self, src_folder=".")

    def generate(self):
        # This generates "conan_toolchain.cmake" in self.generators_folder
        cxx_flags = []
        # cxx_flags.append("-g")
        if self.settings.build_type == "Debug":
            cxx_flags.append("-O0")
        else:
            cxx_flags.append("-O3")
            cxx_flags.append("-s")

        if self.options.COVERAGE:
            cxx_flags.append("--coverage")

        tc = CMakeToolchain(self, generator="Ninja")
        tc.absolute_paths = True
        tc.variables["CMAKE_EXPORT_COMPILE_COMMANDS"] = "ON"
        tc.cache_variables["STATIC_BUILD"] = self.options.STATIC_BUILD
        tc.extra_cxxflags = cxx_flags
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(target=f"{self.options.BUILD_TARGET}")

    def imports(self):
        self.copy("license*", src=".", dst="./licenses", folder=True, ignore_case=True)

    # def build_requirements(self):
    #     # 'build' context (protoc.exe will be available)
    #     self.tool_requires("grpc/1.67.1")
