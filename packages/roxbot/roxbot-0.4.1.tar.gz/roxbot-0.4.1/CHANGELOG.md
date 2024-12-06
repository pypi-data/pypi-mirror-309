# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Planned




## Unreleased

## v4.1

* add `Node._on_init(self)` coro, override to init nodes


## v4.0

* Refactor `GpsNode` back to a single class. Remove ABC.
* remove heartbeat and error counters from `Node`.


## v3.8

* add `parent` option for creating mqtt adapters to create a descriptive logger name.

## v3.7

* allow only one start of `MqttAdapter`

## v3.6.0

* add `MqttAdapter.publish_nowait` to work with synchronous code.

## v3.5.0

* add `Node.stop()` to cancel all running tasks
* implement lock to avoid multiple starts for `Node.main()`



## v3.4.0

* add `GpsLatlon` and `GpsHeading` classes.
* remove `PositionData.time` it is already in timestamp.


## v3.3.0

* refactor `GpsNode` to use `Node` base class.
* add error and warning counters to `Node` class

## v3.2.0

* add `GpsMockNode` to generate fake gps data.

## v3.0.0

* import point for nodes moved to `roxbot.nodes`
* switch from `ruff` to `pylint` and `black`. Pylint catches more errors.


## v2.8.0

* remove vectors extensions to avoid confusion
* add gps conversion to `Pose`


## v2.7.0

* Deprecate `converter.GpsConverter` in favor of direct functions. This is now more in line with v1.x
* add latlon conversions to `Vector`


## v2.6.0
* refactor gps mock, now more compatible with 1.x


## v2.5.0

* add `Node` base class and `examples/node.py`
* update docs (rename Bridges to Adapters)

## v2.4.0
* gps_mock, posting simulated gps data to mqtt topic
* rename `MqttAdapter.send()` to `.publish()`


## v2.3.0

* add `nodes.gps_node` (receives mqqt gps messages and aggregates them)
* add gps dataclasses in `interfaces`

## v2.2.0

* add `examples/node.py` - classless node implementation
* add `adapters.mqtt_logger.MqttLogger` that forwards python logging to a mqtt topic
* rename `bridges` to `adapters`. Also rename `MqttBridge` to `MqttAdapter`. This is to avoid confusion with
stand-alone [mqtt-bridge](https://gitlab.com/roxautomation/components/mqtt-bridge)

## v2.1.0
    * move vectors to `rox-vectors` package.


## v2.0.0
    * initial release after move to github and refactoring.
