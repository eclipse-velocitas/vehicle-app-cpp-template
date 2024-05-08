#include <gtest/gtest.h>

// this is required to override the test_main entry point from boost...
int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
