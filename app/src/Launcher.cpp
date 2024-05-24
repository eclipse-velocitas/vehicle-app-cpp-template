/**
 * Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include "SampleApp.h"
#include "sdk/Logger.h"

#include <csignal>
#include <memory>

std::unique_ptr<example::SampleApp> myApp;

void signal_handler(int sig) {
    velocitas::logger().info("App terminated due to: Signal {}", sig);
    myApp->stop();
}

int main(int argc, char** argv) {
    signal(SIGINT, signal_handler);

    myApp = std::make_unique<example::SampleApp>();
    try {
        myApp->run();
    } catch (const std::exception& e) {
        velocitas::logger().error("App terminated due to: {}", e.what());
    } catch (...) {
        velocitas::logger().error("App terminated due to an unknown exeption.");
    }
    return 0;
}
