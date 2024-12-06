# Adapters


"Adapters" are used for connecting subsystems and as an interface to user interfaces.

A `Adapter` is an abstraction that implements `pub/sub` paradigm. An `Adapter` interface is defined by [AdapterProtocol](../reference/interfaces.md#roxbot.interfaces.AdapterProtocol)


For example, we can split a system in two parts - *motion* and *safety*. Each subsystem can
run stand-alone in its own docker container. `pub/sub` topics can be used to communicate between the
containers over network.

Specific backend of a `Adapter` can vary. Many "middlewares" are available, like `mqtt`, `zeromq` and others.

``` mermaid
graph TD

    subgraph motion_subsystem
        diffdrive_node
        line_follower_node
    end

    subgraph safety_subsystem
        estop_node
        lidar_node
    end

    safety_subsystem ---|Adapter|motion_subsystem



```



## MQTT Adapter

*see also:*  [code reference](../reference/adapters.md)

Example usage (see `examples/Adapters` folder)

```python
--8<-- "examples/Adapters/mqtt_Adapter_example.py"

```



## Background - Middleware alternatives



ROS2 currently uses DDS, which is  a source of frustration for many ROS users. Common criticisms include complexity in setup and configuration, especially in networking and node management. The use of DDS (Data Distribution Service) as the default communication middleware has been highlighted as a pain point, with users reporting difficulties in configuring and optimizing network communications
[ROS Discourse](https://discourse.ros.org/t/why-ros-is-still-choosen-against-ros-2/34723)

A list of alternatives for DDD has been considered and well-documented.

see [RMW alternate.pdf](https://discourse.ros.org/uploads/short-url/o9ihvSjCwB8LkzRklpKdeesRTDi.pdf)

!!! note
    ROS2 seems to choose Zenoh. It does however not play nice with `asyncio`. MQTT seems simpler and more stable.
