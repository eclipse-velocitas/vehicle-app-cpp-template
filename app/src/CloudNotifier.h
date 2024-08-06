/***************************************************************************************
 * Copyright (c) ETAS GmbH 2024. All rights reserved,
 * also regarding any disposal, exploitation, reproduction, editing,
 * distribution, as well as in the event of applications for industrial property rights.
 ***************************************************************************************/

#include "cloud/CloudNotifier.h"
#include "nevonex-fcal-platform/log/Logger.hpp"

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
