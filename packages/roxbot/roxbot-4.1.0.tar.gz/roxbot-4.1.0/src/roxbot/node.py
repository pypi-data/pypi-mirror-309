#!/usr/bin/env python3
"""
Base Node class

Contains boilerplate for all nodes to ensure consistency.



Copyright (c) 2024 ROX Automation - Jev Kuznetsov

"""

import asyncio
import logging
import time
from typing import List, Callable

from .adapters.mqtt_adapter import MqttAdapter
from .config import MqttConfig


class Node:
    """base Node class

    Functionality:
        * logging `self._log`
        * mqtt interface `self.mqtt`
        * cancellation of all tasks on .stop()
        * lock to avoid starting a node multple times

    How to use:
        * create a Node child class, optionally provide a name
        * add coroutines to `self._coros` list in __init__

    """

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.__class__.__name__
        self._log = logging.getLogger(self.name)
        self.mqtt = MqttAdapter(parent=self)

        # list of coroutines to run in main(). Append to this list in __init__ of derived class. Provide as a reference to the coro, not a call.
        self._coros: List[Callable] = []

        self._main_started = False
        self._tasks: List[asyncio.Task] = []

    async def _on_init(self) -> None:
        """init coroutine to run in main(), override in derived class"""

    async def main(self) -> None:
        """main coroutine"""
        self._log.debug("starting main")

        if self._main_started:
            raise RuntimeError("Node is already running")

        self._main_started = True

        # start mqtt
        self._tasks.append(asyncio.create_task(self.mqtt.main()))

        await self._on_init()

        async with asyncio.TaskGroup() as tg:
            for coro in self._coros:
                self._log.info(f"starting {coro}")
                task = tg.create_task(coro())
                self._tasks.append(task)

        self._log.info("Main coroutine finished")

    async def stop(self) -> None:
        """cancel all running tasks"""
        self._log.info("Stopping Node...")
        for task in self._tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                self._log.info(f"Task {task} cancelled")
        self._log.info("Node stopped")
        self._main_started = False
