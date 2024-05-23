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

// TODO: Add header file for CloudNotifier
#include "CloudNotifier.h"

#include <gtest/gtest.h>

using namespace example;

TEST(CloudNotifierTest, test_handleMessage_arbitraryMessage_unableToFindFeatureConfig) {
    CloudNotifier notifier;
    EXPECT_THROW(notifier.handleMessage(std::string{"my message"}), std::runtime_error);
}

TEST(CloudNotifierTest, handleFile_invalidFilePath_unableToFindFeatureConfig) {
    CloudNotifier notifier;
    EXPECT_THROW(notifier.handleFile(std::string{"/file/path"}), std::runtime_error);
}
