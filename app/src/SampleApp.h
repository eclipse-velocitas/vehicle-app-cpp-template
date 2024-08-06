/***************************************************************************************
 * Copyright (c) ETAS GmbH 2024. All rights reserved,
 * also regarding any disposal, exploitation, reproduction, editing,
 * distribution, as well as in the event of applications for industrial property rights.
 ***************************************************************************************/

#ifndef VEHICLE_APP_SDK_SEATADJUSTER_EXAMPLE_H
#define VEHICLE_APP_SDK_SEATADJUSTER_EXAMPLE_H

#include "LatticeApp.h"
#include "cloud/Cloud.h"
#include "nevonex-fcal-platform//log/Logger.hpp"
#include "sdk/Status.h"
#include "vehicle/Vehicle.hpp"
#include <memory>
#include <string>

namespace example {

/**
 * @brief Sample skeleton vehicle app.
 * @details The skeleton subscribes at the VehicleDataBroker for updates for
 * the Vehicle.Speed signal.It also subscribes at a MQTT topic to listen for
 * incoming requests to change the seat position and calls the SeatService to
 * move the seat upon such a request, but only if Vehicle.Speed equals 0.
 */
class SampleApp : public ::lattice::LatticeApp {
public:
    SampleApp();

    /**
     * @brief Run when the vehicle app starts
     *
     */
    void onStart() override;

    /**
     * @brief Handle successful seat movement requests.
     *
     * @param requestId           The ID of the request requested the movement.
     * @param requestedPosition   The seat position of the request.
     */
    void onSeatMovementRequested(const velocitas::VoidResult&, int requestId,
                                 float requestedPosition);

    /**
     * @brief Handle set position request from PubSub topic
     *
     * @param data  The JSON string received from PubSub topic.
     */
    void onSetPositionRequestReceived(const std::string& data);

    /**
     * @brief Handle seat movement events from the VDB.
     *
     * @param dataPoints  The affected data points.
     */
    void onSeatPositionChanged(const velocitas::DataPointReply& dataPoints);

    /**
     * @brief Handle errors which occurred during async invocation.
     *
     * @param status  The status which contains the error.
     */
    void onError(const velocitas::Status& status);
    void onErrorDatapoint(const velocitas::Status& status);
    void onErrorTopic(const velocitas::Status& status);

private:
    vehicle::Vehicle Vehicle;
};

} // namespace example

#endif // VEHICLE_APP_SDK_SEATADJUSTER_EXAMPLE_H
