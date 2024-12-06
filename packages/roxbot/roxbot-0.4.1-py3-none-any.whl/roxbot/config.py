#!/usr/bin/env python3
"""
common configuration

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class MqttConfig(BaseSettings):
    """MQTT related settings"""

    model_config = SettingsConfigDict(env_prefix="mqtt_")

    host: str = "localhost"
    port: int = 1883
    # topics
    heartbeat_topic: str = "/heartbeat"
    log_topic: str = "/log"
    gps_position_topic: str = "/gps/position"
    gps_direction_topic: str = "/gps/direction"


class PrecisionConfig(BaseSettings):
    """precision settings"""

    model_config = SettingsConfigDict(env_prefix="digits_")

    position: int = 3
    latlon: int = 8
    angle: int = 4
