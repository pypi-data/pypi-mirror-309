---
draft: false
date: 2023-06-11
categories:
  - ROS2
  - cicd
authors:
  - jev
---


# Speed up your ROS2 development with a Docker stack

In this post, I'm going to share with you my solution for quickly setting up development and runtime environments around ROS2. If you've ever struggled with incompatible package versions, conflicting OS requirements, or reproducing the exact same setup across multiple machines, then this post is for you. By utilizing a Docker stack, you can bring up a clean development environment in mere minutes, allowing you to focus on developing your robotics applications instead of system management.

<!-- more -->

## Why Docker?

Docker solves many of the challenges that developers face:

1. **Automated and reproducible system installation**: With Docker, you can start with a clean Ubuntu or pre-installed ROS image and build further on that. A Dockerfile serves as a self-documenting recipe for setting up your system step-by-step, eliminating the need for copying and pasting shell commands.

2. **Keeping your system clean**: Have you ever messed up your system while experimenting? With Docker, you can simply rebuild the container, and you'll have a clean slate again. This ability to isolate your development environment from your host system is incredibly valuable.

3. **Isolated development environment**: Similar to virtual environments or virtual machines, a Docker container contains only the necessary components, ensuring that your host system remains untouched. This isolation eliminates conflicts and allows for seamless development across different machines.

4. **Deployment**: With Docker, you can build an image of your ROS2 application and run it on any machine that supports Docker. This portability simplifies the deployment process, as you don't have to worry about differences in system configurations.

5. **CI/CD**: By utilizing container images, you can leverage the automation tools provided by platforms like GitHub or GitLab for continuous integration and continuous deployment. This allows for streamlined testing and deployment of your robotics applications.

## What you need

To get started, you'll need the following:

1. A Linux host system (Ubuntu 20+ is recommended).
2. `git` for cloning repositories.
3. Docker for running containers (install easily from [get.docker.com](https://get.docker.com/)).
4. Docker-compose for managing multi-container applications (`pip install docker-compose`).
5. [Visual Studio Code](https://code.visualstudio.com/) and the [devcontainers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
6. Basic understanding of development inside a container. If you're new to this concept, you can find an excellent explanation [here](https://code.visualstudio.com/docs/devcontainers/containers).

## Let's get started

I've created an example repository on [GitLab](https://gitlab.com/roxautomation/playground/ros-stack). Let's begin by getting the code:

```shell
git clone https://gitlab.com/roxautomation/playground/ros-stack.git
cd ros-stack
```

Now, we can start the Docker stack by running `docker-compose up`. This command launches the containers defined in the `docker-compose.yml` file, providing a complete ROS2 environment for development and testing.

The stack includes the following services:

- `talker`: Runs the `talker_node.py` script, which posts a message on `/chatter` every 5 seconds.
- `rosboard`: Runs the [rosboard](https://github.com/dheera/rosboard) web UI accessible at [localhost:8888](http://localhost:8888).
- `rosbridge`: Provides a way for non-ROS code to interact with the stack through a WebSocket, using the [rosbridge protocol](https://github.com/biobotus/rosbridge_suite/blob/master/ROSBRIDGE_PROTOCOL.md).
- `devcontainer`: A ROS2 container specifically designed for

 development.

This setup closely resembles what you would run on a production system.

## Working with the stack

Once the stack is running, you have a couple of options for interacting with the `devcontainer`:

1. From the shell: Use the command `docker exec -it devcontainer bash` to enter a prompt inside the container.
2. From Visual Studio Code: Use the command `Devcontainers: Attach to running container` to connect to the `devcontainer`.

Once inside the `devcontainer`, you can use familiar ROS2 commands like `ros2 node list`, `ros2 topic list`, and `ros2 topic echo /chatter` to interact with the ROS2 stack.

Additionally, if the stack is not running, you can easily launch it from within Visual Studio Code:

1. Open the repository folder in Visual Studio Code.
2. Run the command `Devcontainers: Rebuild and reopen in container`. This will rebuild the stack and connect to the `devcontainer`.

This is actually my preferred way of firing up my dev environment.

## Connecting from non-ROS systems

Sometimes, you may need to interact with the ROS system from non-ROS subsystems, such as a web interface or a pure Python script. In such cases, the `rosbridge` component comes to the rescue. It enables access to the ROS stack through a WebSocket using well-defined JSON messages. You can utilize the `roslibpy` Python package to communicate with the `rosbridge` protocol.

An example listener utilizing `rosbridge` is provided in the `/workspace/examples/listen.py` file.

## Limitations

While running ROS in Docker greatly simplifies system management, it's important to be aware of its limitations. One notable limitation is the difficulty of running native GUI applications inside Docker. Although attempts have been made to make graphical tools work from within a container, the results have been limited and hard to reproduce across different host systems. As a workaround, it's recommended to utilize web-based tools like `rosboard`. This approach not only overcomes the GUI limitation but also enables the execution of graphical interfaces on remote systems.

## Conclusion

Using Docker for your ROS2 development can significantly speed up your workflow by providing an automated, reproducible, and isolated environment. By utilizing Docker's containerization technology, you can minimize the time spent on environment setup, package management, and launch system configuration. The ability to deploy your ROS2 applications seamlessly and leverage CI/CD pipelines further enhances your development process. While there are limitations, such as running native GUI applications, Docker remains an invaluable tool for streamlining ROS2 development and ensuring consistency across multiple machines.

I would like to extend my gratitude to the Hadabot blog and their code repository at [https://github.com/hadabot/hadabot_main/tree/master/docker](https://github.com/hadabot/hadabot_main/tree/master/docker) for providing valuable insights and inspiration. Their resources greatly helped me get started with using Docker for ROS2 development. I encourage you to explore their content for further knowledge in this area.

Give the ROS2 Docker stack a try, and experience the benefits firsthand in your robotics projects. Accelerate your development and focus on building amazing robotic applications without the hassle of system management.
