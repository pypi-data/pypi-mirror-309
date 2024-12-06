#!/usr/bin/env python3
"""
  plot data with plotjuggler
"""
import time
import socket
import orjson
import logging


class UDP_Client:
    """send data to UDP server, used for plotting with plotjuggler"""

    def __init__(self, host: str = "127.0.0.1", port: int = 5005):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._log = logging.getLogger(self.__class__.__name__)

    def send(self, data: dict) -> None:
        """send data to UDP server"""
        try:
            data["ts"] = round(time.time(), 3)
            self._sock.sendto(orjson.dumps(data), (self._host, self._port))
        except Exception as e:  # pylint: disable=broad-except
            self._log.error(f"Failed to send data: {e}")

    def close(self) -> None:
        """close socket"""
        self._sock.close()

    def __del__(self) -> None:
        self.close()
