# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

from lib.animator import RepeatMode
from lib.dsl import (
    create_animation_action,
    create_behavior,
    create_event_trigger,
    create_set_action,
    get_datapoint_value,
    mock_datapoint,
)
from lib.trigger import ClockTrigger, EventType

mock_datapoint(
    path="Vehicle.Speed",
    initial_value=0.0,
    behaviors=[
        create_behavior(
            trigger=ClockTrigger(0),
            action=create_animation_action(
                duration=10.0,
                repeat_mode=RepeatMode.REPEAT,
                values=[0, 100.0, 0.0],
            ),
        )
    ],
)

mock_datapoint(
    path="Vehicle.Cabin.Seat.Row1.Pos1.Position",
    initial_value=0,
    behaviors=[
        create_behavior(
            trigger=create_event_trigger(EventType.ACTUATOR_TARGET),
            action=create_animation_action(
                duration=10.0,
                values=["$self", "$event.value"],
            ),
        )
    ],
)

mock_datapoint(
    path="Vehicle.Body.Windshield.Front.Wiping.System.Mode",
    initial_value="STOP_HOLD",
    behaviors=[
        create_behavior(
            trigger=create_event_trigger(EventType.ACTUATOR_TARGET),
            action=create_set_action("$event.value"),
        )
    ],
)

mock_datapoint(
    path="Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition",
    initial_value=0,
    behaviors=[
        create_behavior(
            trigger=create_event_trigger(EventType.ACTUATOR_TARGET),
            action=create_set_action("$event.value"),
        )
    ],
)

mock_datapoint(
    path="Vehicle.Body.Windshield.Front.Wiping.System.ActualPosition",
    initial_value=0,
    behaviors=[
        create_behavior(
            trigger=create_event_trigger(EventType.ACTUATOR_TARGET),
            condition=lambda ctx: get_datapoint_value(
                ctx, "Vehicle.Body.Windshield.Front.Wiping.System.Mode"
            )
            == "EMERGENCY_STOP",
            action=create_set_action(0),
        ),
        create_behavior(
            trigger=create_event_trigger(EventType.ACTUATOR_TARGET),
            condition=lambda ctx: get_datapoint_value(
                ctx, "Vehicle.Body.Windshield.Front.Wiping.System.Mode"
            )
            == "STOP_HOLD",
            action=create_animation_action(
                duration=10.0,
                values=[
                    "$self",
                    "$Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition",
                ],
            ),
        ),
        create_behavior(
            trigger=create_event_trigger(EventType.ACTUATOR_TARGET),
            condition=lambda ctx: get_datapoint_value(
                ctx, "Vehicle.Body.Windshield.Front.Wiping.System.Mode"
            )
            == "WIPE",
            action=create_animation_action(
                duration=10.0,
                values=[
                    "$self",
                    "$Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition",
                ],
            ),
        ),
    ],
)

mock_datapoint(
    path="Vehicle.Cabin.HVAC.IsFrontDefrosterActive",
    initial_value=False,
    behaviors=[
        create_behavior(
            create_event_trigger(EventType.ACTUATOR_TARGET),
            create_set_action("$event.value"),
        )
    ],
)
