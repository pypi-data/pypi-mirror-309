#!/usr/bin/env python3
"""
Demonstration of forwarding log messages to an MQTT topic

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import logging
import asyncio

from roxbot.adapters.mqtt_logger import MqttLogger
from roxbot.utils import run_main_async


async def main() -> None:
    log = logging.getLogger("main")
    log.setLevel(logging.DEBUG)

    log_forwarder = MqttLogger(logger=log)

    # add the mqtt log handler
    # log.addHandler(log_forwarder.get_log_handler())

    # log some messages
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")

    asyncio.create_task(log_forwarder.main())
    await asyncio.sleep(1)


if __name__ == "__main__":
    run_main_async(main())
