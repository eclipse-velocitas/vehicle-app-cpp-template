// TODO: Add header file for CloudNotifier
#include "CloudNotifier.cpp"

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
