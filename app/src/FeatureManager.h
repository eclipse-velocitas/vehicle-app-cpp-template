/**
 * Copyright (c) 2024 Contributors to the Eclipse Foundation
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

#include "listener/FeatureManager.h"
#include "nevonex-fcal-platform/log/Logger.hpp"

namespace example {
class FeatureManager : public virtual ::lattice::listener::FeatureManager {
public:
    void handleFeatureStart(const std::string& message) override {
        APP_LOG(SeverityLevel::info) << "handleFeatureStart .." << message;
    }
    void handleFeatureStop(const std::string& message) override {
        APP_LOG(SeverityLevel::info) << "handleFeatureStop .." << message;
    }
};
} // namespace example
