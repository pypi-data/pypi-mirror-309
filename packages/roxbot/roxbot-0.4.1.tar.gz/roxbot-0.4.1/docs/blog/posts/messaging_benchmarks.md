---
draft: false
date: 2023-12-13
categories:
  - ROS2
  - asyncio
authors:
  - jev
---

# Why asyncio is Ideal for Robotics Development

As a professional in robotics software development, I've extensively used ROS. In fact, ROS2 is the current standard in this field. However, I've recently transitioned to using asyncio, a leaner solution that allows for the creation of more efficient and manageable codebases in a shorter time. In this post, I'll share my experiences with ROS and explain why I believe asyncio is a superior choice.


![](img/benchmark_emoticons.png)

<!-- more -->

## ROS In A Nutshell

Let's start with a brief introduction to ROS for those unfamiliar with it. Essentially, ROS (Robot Operating System) is a framework designed to help in creating and managing asynchronous processes, known as "nodes". These nodes are individual processes tasked with specific functions, like reading a sensor or controlling an actuator. They communicate through "topics" using a publish/subscribe pattern, and request/reply interactions are facilitated through services. In this article, when I refer to "ROS", I'm specifically talking about ROS2, as ROS1 is now outdated and not recommended for industrial use.

## Why ROS Might Not Be the Ideal Choice

While ROS is quite helpful in managing complex, asynchronous systems, I often found it to be somewhat cumbersome, adding unnecessary complexity and slowing down development, especially when compared to more streamlined frameworks available in the Python ecosystem.

Here are some key limitations I encountered with ROS, particularly from a Python developer's perspective:

1. **Primary Language**: ROS primarily uses C++, making Python integration feel like an afterthought. The Python library `rclpy` often lacks the full functionality of its C++ counterpart.
2. **Packaging and Execution Process**: The way ROS packages and executes code is quite different from standard Python practices. For example, why do we need to source a setup file (`source /setup.bash`) and then use a ROS-specific command (`ros2 run ...`) when we could just run an executable directly?
3. **Launch System**: ROS employs its own unique and complex and inefficient launch system (each `launch.py` file consuming around 20MB of memory). In contrast, tools like `systemd` and Docker provide more mature and well-designed launching solutions for modern applications.
4. **Interface Definitions**: The process of defining and compiling interfaces in ROS can add unnecessary overhead to development.
5. **Cross-Domain Communication**: Transferring data across different subdomains in ROS can be challenging. An alternative like MQTT, with its centralized protocol, simplifies this process by specifying clear host and port connections, making troubleshooting more straightforward.
6. **Performance Issues**: Inter-node communication, especially between nodes written in Python, can be inefficient, leading to sluggish performance. I'll delve more into this in the "Benchmarks" section.
7. **Native graphics requirement**: ROS relies on tools like RQT, which depend on native graphics. This setup becomes problematic when working remotely, as these tools are not easily accessible or functional across network domains. A more practical alternative would be web-based tools, which can be operated from any browser, offering greater flexibility and ease of use in remote working scenarios.



## Introducing Roxbot: A Pythonic ROS Alternative

Confronted daily with these challenges in ROS, I was motivated to find solutions to streamline my work. Over the past year, I've been developing a Python-centric robotics framework named "Roxbot". This framework is akin to ROS but is designed to overcome the limitations I've encountered. Currently, Roxbot is in its pre-release phase and can be explored on [Github](https://github.com/rox-automation/roxbot) Note that while Roxbot is not ready for release as a full-fledged ROS replacement, it contains many bits and pieces that
I've been using in various customer projects over the course of last year.


While I plan to delve deeper into Roxbot in a future post, this article will focus on its most critical component – the communication layer. Selecting the right communication protocol is perhaps the most significant and challenging architectural decision in the framework's development. To ensure I made an informed choice, I created an extensive benchmark suite. This suite evaluates various communication protocols, examining their performance both within and across Docker containers. I will share the comprehensive findings and insights from this benchmarking in the next section of the blog.


## Benchmarks: The Results Are In!

The complete benchmark suite is accessible on [GitLab](https://gitlab.com/roxautomation/playground/benchmarks) in the `messaging` folder.

The benchmark involves various scenarios with nodes named `Alice` and `Bob` communicating within the same Docker container or across two different ones. Here's a brief overview:

- **ROS Benchmark Python**: Two `rclpy` nodes in the same container.
- **C++ in Single Container**: Two C++ nodes in the same container.
- **C++ in Two Containers**: Separate containers, communicating over the host network.
- **C++ in Two Isolated Containers**: Separate containers, communicating over an isolated Docker network.
- **MQTT Benchmark**: Separate containers using `paho.mqtt` with a Mosquitto broker, over an isolated Docker network.
- **Async Benchmark**: Same container, nodes communicate via `asyncio.Queue`.
- **Websocket Benchmark**: Separate containers, nodes communicate using `websockets`.
- **RPC Benchmark**:  `grpc` remote call. Note that this is different from other methods as it uses request/reply instead of pub/sub

### Benchmark Methodology:

1. Alice sends the number 0 to Bob.
2. Bob increments the number to 1 and sends it back to Alice.
3. Alice increments it to 2 and sends it back to Bob.
4. This ping-pong continues until a specific count is reached (typically 10,000).
5. The "message rate" is calculated based on the number of messages exchanged per second.

These benchmarks are designed to run in Docker containers, allowing for easy replication on your system. For detailed instructions, refer to the `README.md` file.

## And The Winner Is...

After running the benchmark suite on various systems, the insights gained were quite eye-opening. Here's what emerged:

1. Python nodes in ROS exhibit significantly slow communication speeds.
2. C++ nodes offer decent performance, but C++ may not be the preferred language for ease of coding.
3. Python `async` stands out remarkably, surpassing even C++ systems in single-container setups by a substantial margin.

An interesting observation was the performance drop in ROS C++ nodes when communicating across containers in an isolated Docker network. Therefore, if you're considering segmenting your system into separate Docker containers, using `net=host` might be a more efficient approach.


Top of this post contains results from a fairly modern laptop with an i5 processor.
Tests on a RaspberryPi 4 with 2GB of memory produce these results:

![](img/benchmark_rpi4.png)

While the difference in perofmance between C++ and asyncio on `aarch64` is less dramatic than on a `x86_64`system, asyncio is an undisputed winner here.

## Show Me The Code!

!!! info
    The complete benchmark suite is accessible on [GitLab](https://gitlab.com/roxautomation/playground/benchmarks) in the [`messaging`](https://gitlab.com/roxautomation/playground/benchmarks/-/tree/main/messaging?ref_type=heads) folder.

Another great advantage of `asyncio` is code simplicity. An implementation of `EchoNode` looks like this:

```python

STOP_AFTER = 100_000

class EchoNode:
    def __init__(self, name: str, sub_q: asyncio.Queue, pub_q: asyncio.Queue):
        self.name = name
        self.sub_q = sub_q
        self.pub_q = pub_q

        # Alice starts the ping-pong
        if name.lower() == "alice":
            self.pub(0)

    def pub(self, nr):
        self.pub_q.put_nowait(nr)

    async def sub(self):
        """handle incoming messages"""

        while True:
            nr = await self.sub_q.get()

            if nr > STOP_AFTER:
                print(f"{self.name} had enough. Stopping.")
                raise TestComplete

            self.sub_q.task_done()
            self.pub(nr + 1)

```

Let's compare it with a C++ snippets (split over `.hpp` and `.cpp` files) to achieve the same functionality...


!!! note
    I haven't used C++ much since my masters thesis in 2004. So "Pardon my C++" ;-).
    This is what I managed to build with help of ChatGPT.

```C++

// ----------------- .hpp -----------------------
#ifndef ROS_BENCHMARK_CPP__ECHO_NODE_HPP_
#define ROS_BENCHMARK_CPP__ECHO_NODE_HPP_

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int64.hpp"
#include <chrono>

class EchoNode : public rclcpp::Node {
public:
    static constexpr int STOP_AFTER = 10'000;
    EchoNode(const std::string & name, const std::string & sub_topic, const std::string & pub_topic);
    void pub(int nr);

    // Method to get the start time of the node
    const std::chrono::steady_clock::time_point& get_start_time() const;

private:
    void sub_callback(const std_msgs::msg::Int64::SharedPtr msg);

    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::Int64>::SharedPtr subscriber_;

    // Start time for the benchmark
    std::chrono::steady_clock::time_point start_time_;


};

#endif  // ROS_BENCHMARK_CPP__ECHO_NODE_HPP_

// ------------------ .cpp -----------------------------


#include "ros_benchmark_cpp/echo_node.hpp"
#include <iostream>

EchoNode::EchoNode(const std::string & name, const std::string & sub_topic, const std::string & pub_topic)
: Node(name),
  publisher_(this->create_publisher<std_msgs::msg::Int64>(pub_topic, 10)),
  subscriber_(this->create_subscription<std_msgs::msg::Int64>(
      sub_topic, 10, [this](const std_msgs::msg::Int64::SharedPtr msg) { this->sub_callback(msg); })),
  start_time_(std::chrono::steady_clock::now())
{
}

void EchoNode::sub_callback(const std_msgs::msg::Int64::SharedPtr msg) {
    int nr = msg->data;

    if (nr > STOP_AFTER) {
        std::cout << this->get_name() << " had enough. Stopping." << std::endl;
        rclcpp::shutdown();
    } else {
        this->pub(nr + 1);
    }
}

void EchoNode::pub(int nr) {
    auto message = std_msgs::msg::Int64();
    message.data = nr;
    publisher_->publish(message);
}

const std::chrono::steady_clock::time_point& EchoNode::get_start_time() const {
    return start_time_;
}

```

Regarding maintainability and readability, I don't have to explain much here - the code
speaks for itself.


## Looking Forward


!!! question "Interested?"
    Are you passionate about robotics and Python, dreaming of a "Pythonic ROS"? You're not alone! I'm on a quest to develop Roxbot, and I'd love to collaborate with like-minded developers.
