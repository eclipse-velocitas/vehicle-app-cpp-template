#include "listener/FeatureManager.h"
#include "nevonex-fcal-platform/log/Logger.hpp"
using namespace ::nevonex::log;

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