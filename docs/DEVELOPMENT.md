# Developing a Vehicle App

This repository ships with source code for a sample application in `<repo_root>/app/src` which can be modified freely.

For accessing vehicle data, an auto-generated API based on the [Vehicle Signal Specification 4.0](https://github.com/COVESA/vehicle_signal_specification/tree/v4.0), is used. To access vehicle data, use the `SampleApp::Vehicle` member variable and navigate through the vehicle signal tree using VSCode's intellisense's auto-completion:

![Intellisense](./images/vss_intellisense.png)


### Getting and setting vehicle signals

Once you have navigated to the desired vehicle signal, you can either query its value by invoking its `.get` method or you can actuate it by invoking its `.set` method. Communication with the vehicle will take place asynchronously. To wait for the result, call the `await()` method. Alternatively, you can attach a callback function which will be invoked once the result is available: `onResult(<your callback>)`

```cpp
// Set and query driver seat position
Vehicle.Cabin.Seat.Row1.DriverSide.Position.set(desiredSeatPosition)->await();

auto pos = Vehicle.Cabin.Seat.Row1.DriverSide.Position.get()->await();
```

### Listening for vehicle signal changes

Sometimes you will need to react to changes of a vehicle signal, which can be done by subscribing to the signal using the `VehicleApp::subscribeDataPoints` method:

```cpp
subscribeDataPoints(
    velocitas::QueryBuilder::select(Vehicle.Cabin.Seat.Row1.DriverSide.Position).build())
    ->onItem([this](auto&& item) { onSeatPositionChanged(std::forward<decltype(item)>(item)); });
```

## Configuring Vehicle Signal Interface

The VSS-based input file for auto-generating the API is defined in `<repo_root>/app/AppManifest.json`. Here you will find a section about `vehicle-signal-interface`:

```json
{
    <...>
    "interfaces": [
        {
            "type": "vehicle-signal-interface",
            "config": {
                "src": "https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.0/vss_rel_4.0.json"
            }
        }
    ]
}
```

The `config.src` attribute is a URI to a JSON export of a VSS based vehicle specification, such as the [official release 4.0](https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.0/vss_rel_4.0.json) of VSS. It may point to a local file or on a webserver.

Further reading: [How to reference a model specification](https://eclipse.dev/velocitas/docs/tutorials/vehicle_model_creation/automated_model_lifecycle/#how-to-reference-a-model-specification)

## (Re-)Generating the Vehicle API

Upon initial devContainer startup, Velocitas' lifecycle management reads the `config.src` from the referenced `vehicle-signal-interface` to generate an API to be used within the project.
When the src changes, it is necessary to re-generate the API in one of the following ways:

* **Re-initialize the project**

    Run the following command in a terminal to re-initialize the project:
    ```shell
    velocitas init
    ```
* **Run the re-generate VSCode task**
   1. Press <kbd>F1</kbd>
   1. Select command "Tasks: Run Task"
   1. Select "(Re-)generate vehicle model"

Further reading on [How a vehicle model is generated](https://eclipse.dev/velocitas/docs/tutorials/vehicle_model_creation/automated_model_lifecycle/#model-creation).
