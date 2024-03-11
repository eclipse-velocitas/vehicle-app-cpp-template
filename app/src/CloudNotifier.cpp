#include <cloud/CloudNotifier.h>
namespace example {
class CloudNotifier : public virtual ::nevonex::cloud::CloudNotifier {
    void handleMessage(const std::string& message) {
        APP_LOG(SeverityLevel::info) << "Cloud Message Received ... " << message;
    }

    void handleFile(const ::nevonex::resource::FilePath& _file) {
        APP_LOG(SeverityLevel::info)
            << "Cloud File Received ...  file path : " << _file.get().string();
    }
};
} // namespace example