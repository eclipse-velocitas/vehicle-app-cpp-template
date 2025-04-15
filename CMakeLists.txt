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

cmake_minimum_required(VERSION 3.16)

# set the project name
project(VehicleApp CXX)

# APP settings
set(APP_BUILD_TESTS     ON CACHE BOOL "Build the App's tests.")

# Overall settings
set(CMAKE_CXX_STANDARD 17)
set(STATIC_BUILD        OFF CACHE BOOL "Build all targets with external dependencies linked in statically.")

find_package(vehicle-app-sdk REQUIRED)
find_package(vehicle-model REQUIRED)
find_package(fmt REQUIRED)
find_package(nlohmann_json REQUIRED)

# Induce to put executables into the bin folder of the current build folder
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin)

if(STATIC_BUILD)
    set(BUILD_SHARED_LIBS OFF)
    set(CMAKE_EXE_LINKER_FLAGS "-static")
endif()

find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    message("Found ccache installation")
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
endif()

add_subdirectory(app)

if(APP_BUILD_TESTS)
    enable_testing()
endif()
