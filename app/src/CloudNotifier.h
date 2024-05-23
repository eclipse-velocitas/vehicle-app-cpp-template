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

#include "cloud/CloudNotifier.h"
namespace example {
class CloudNotifier : public virtual ::nevonex::cloud::CloudNotifier {
public:
    void handleMessage(const std::string& message) {
        APP_LOG(SeverityLevel::info) << "Cloud Message Received ... " << message;
    }

    void handleFile(const ::nevonex::resource::FilePath& _file) {
        APP_LOG(SeverityLevel::info)
            << "Cloud File Received ...  file path : " << _file.get().string();
    }
};
} // namespace example
