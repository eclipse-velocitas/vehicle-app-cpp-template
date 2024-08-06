/***************************************************************************************
 * Copyright (c) ETAS GmbH 2024. All rights reserved,
 * also regarding any disposal, exploitation, reproduction, editing,
 * distribution, as well as in the event of applications for industrial property rights.
 ***************************************************************************************/

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
