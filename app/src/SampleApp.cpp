/***************************************************************************************
 * Copyright (c) ETAS GmbH 2024. All rights reserved,
 * also regarding any disposal, exploitation, reproduction, editing,
 * distribution, as well as in the event of applications for industrial property rights.
 ***************************************************************************************/

#include "SampleApp.h"
#include "sdk/IPubSubClient.h"
#include "sdk/Logger.h"
#include "sdk/QueryBuilder.h"
#include "sdk/vdb/IVehicleDataBrokerClient.h"

#include "CloudNotifier.h"
#include "FeatureManager.h"
#include <fmt/core.h>
#include <nlohmann/json.hpp>
#include <utility>

using namespace nevonex::log;

namespace example {

const auto TOPIC_REQUEST          = "seatadjuster/setPosition/request";
const auto TOPIC_RESPONSE         = "seatadjuster/setPosition/response";
const auto TOPIC_CURRENT_POSITION = "seatadjuster/currentPosition";

const auto JSON_FIELD_REQUEST_ID = "requestId";
const auto JSON_FIELD_POSITION   = "position";
const auto JSON_FIELD_STATUS     = "status";
const auto JSON_FIELD_MESSAGE    = "message";
const auto JSON_FIELD_RESULT     = "result";

const auto STATUS_OK   = 0;
const auto STATUS_FAIL = 1;

SampleApp::SampleApp()
    : LatticeApp(std::shared_ptr<CloudNotifier>(new CloudNotifier()),
                 std::shared_ptr<lattice::listener::FeatureManager>(new FeatureManager())) {}

void SampleApp::onStart() {
    // This method will be called by the SDK when the connection to the
    // Vehicle DataBroker is ready.
    // Here you can subscribe for the Vehicle Signals update (e.g. Vehicle Speed).
    const auto* const logMessage = "Subscribe for data points!";
    velocitas::logger().info(logMessage);
    APP_LOG(SeverityLevel::info) << logMessage;

    subscribeDataPoints(
        velocitas::QueryBuilder::select(Vehicle.Cabin.Seat.Row1.DriverSide.Position).build())
        ->onItem([this](auto&& item) { onSeatPositionChanged(std::forward<decltype(item)>(item)); })
        ->onError(
            [this](auto&& status) { onErrorDatapoint(std::forward<decltype(status)>(status)); });

    subscribeToTopic(TOPIC_REQUEST)
        ->onItem([this](auto&& item) {
            onSetPositionRequestReceived(std::forward<decltype(item)>(item));
        })
        ->onError([this](auto&& status) { onErrorTopic(std::forward<decltype(status)>(status)); });
}

void SampleApp::onSetPositionRequestReceived(const std::string& data) {
    const auto logMessage = "position request: " + data;
    velocitas::logger().debug("position request: {}", data);
    APP_LOG(SeverityLevel::debug) << logMessage;

    const auto jsonData = nlohmann::json::parse(data);
    if (!jsonData.contains(JSON_FIELD_POSITION)) {
        const auto errorMsg = fmt::format("No position specified");
        velocitas::logger().error(errorMsg);
        APP_LOG(SeverityLevel::error) << errorMsg;

        nlohmann::json respData({{JSON_FIELD_REQUEST_ID, jsonData[JSON_FIELD_REQUEST_ID]},
                                 {JSON_FIELD_STATUS, STATUS_FAIL},
                                 {JSON_FIELD_MESSAGE, errorMsg}});
        publishToTopic(TOPIC_RESPONSE, respData.dump());
        return;
    }

    const auto desiredSeatPosition = jsonData[JSON_FIELD_POSITION].get<int>();
    const auto requestId           = jsonData[JSON_FIELD_REQUEST_ID].get<int>();

    nlohmann::json respData({{JSON_FIELD_REQUEST_ID, requestId}, {JSON_FIELD_RESULT, {}}});
    const auto     vehicleSpeed = Vehicle.Speed.get()->await().value();
    if (vehicleSpeed == 0) {
        Vehicle.Cabin.Seat.Row1.DriverSide.Position.set(desiredSeatPosition)->await();
        const auto message = fmt::format("Set Seat position to: {}", desiredSeatPosition);
        respData[JSON_FIELD_RESULT][JSON_FIELD_STATUS]  = STATUS_OK;
        respData[JSON_FIELD_RESULT][JSON_FIELD_MESSAGE] = message;
        APP_LOG(SeverityLevel::info) << message;
        try {
            ::nevonex::cloud::Cloud::getInstance()->uploadData(message, 1);
        } catch (std::exception& exception) {
            APP_LOG(SeverityLevel::info)
                << "Error while uploading message to the cloud " << exception.what();
        }
    } else {
        const auto errorMsg = fmt::format(
            "Not allowed to move seat because vehicle speed is {} and not 0", vehicleSpeed);
        velocitas::logger().info(errorMsg);
        APP_LOG(SeverityLevel::error) << errorMsg;

        respData[JSON_FIELD_RESULT][JSON_FIELD_STATUS]  = STATUS_FAIL;
        respData[JSON_FIELD_RESULT][JSON_FIELD_MESSAGE] = errorMsg;
    }

    publishToTopic(TOPIC_RESPONSE, respData.dump());
}

void SampleApp::onSeatPositionChanged(const velocitas::DataPointReply& dataPoints) {
    nlohmann::json jsonResponse;
    try {
        const auto seatPositionValue =
            dataPoints.get(Vehicle.Cabin.Seat.Row1.DriverSide.Position)->value();
        jsonResponse[JSON_FIELD_POSITION] = seatPositionValue;
    } catch (std::exception& exception) {
        const auto errorMsg =
            fmt::format("Unable to get Current Seat Position, Exception: {}", exception.what());
        velocitas::logger().warn(errorMsg);
        APP_LOG(SeverityLevel::warning) << errorMsg;

        jsonResponse[JSON_FIELD_STATUS]  = STATUS_FAIL;
        jsonResponse[JSON_FIELD_MESSAGE] = exception.what();
    }

    publishToTopic(TOPIC_CURRENT_POSITION, jsonResponse.dump());
}

void SampleApp::onError(const velocitas::Status& status) {
    const auto errorMsg =
        fmt::format("Error occurred during async invocation: {}", status.errorMessage());
    velocitas::logger().error(errorMsg);
    APP_LOG(SeverityLevel::error) << errorMsg;
}

void SampleApp::onErrorDatapoint(const velocitas::Status& status) {
    const auto errorMsg =
        fmt::format("Datapoint: Error occurred during async invocation: {}", status.errorMessage());
    velocitas::logger().error(errorMsg);
    APP_LOG(SeverityLevel::error) << errorMsg;
}
void SampleApp::onErrorTopic(const velocitas::Status& status) {
    const auto errorMsg =
        fmt::format("Topic: Error occurred during async invocation: {}", status.errorMessage());
    velocitas::logger().error(errorMsg);
    APP_LOG(SeverityLevel::error) << errorMsg;
}

} // namespace example
