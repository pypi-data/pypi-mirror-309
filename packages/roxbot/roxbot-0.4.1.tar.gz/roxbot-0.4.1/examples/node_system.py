#!/usr/bin/env python3
"""
Nodes example
--------------

This example demonstrates how to use the Node class.

* create two nodes that communicate with each other over mqtt.
* log messages to mqtt with MqttLogger

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import asyncio
import logging

from roxbot import Node
from roxbot.adapters import MqttLogger
from roxbot.utils import run_main_async


class NodeOne(Node):
    def __init__(self) -> None:
        super().__init__()

        # add coroutines to run in main()
        self._coros.append(self.talker_coro)

    async def _on_init(self) -> None:
        """init coroutine to run in main()"""
        self._log.info("Running init coroutine")
        await self.mqtt.register_callback("/test_cmd", self.listener_cbk)

    def listener_cbk(self, args: list | dict) -> None:
        """example callback function"""
        self._log.info(f"Running callback with {args=}")

    async def talker_coro(self) -> None:
        """example coroutine"""

        counter = 0

        while True:
            self._log.debug(f"debug message {counter=}")
            self._log.info(f"info message {counter=}")
            counter += 1
            await asyncio.sleep(1)


class NodeTwo(Node):
    """second node, sends commands to the first"""

    def __init__(self) -> None:
        super().__init__()
        self._coros.append(self.send_command)  # don't forget this one

    async def send_command(self) -> None:
        """send command to the first node"""
        counter = 0
        while True:
            await self.mqtt.publish("/test_cmd", {"counter": counter})
            counter += 1
            await asyncio.sleep(2)


# --- main ---


async def main() -> None:
    mqtt_logger = MqttLogger(logging.getLogger())  # forward logs to mqtt
    _ = asyncio.create_task(mqtt_logger.main())  # start logging task

    nodes = [NodeOne(), NodeTwo()]

    await asyncio.gather(*[node.main() for node in nodes])


if __name__ == "__main__":
    run_main_async(main())
