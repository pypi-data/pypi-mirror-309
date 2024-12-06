#!/bin/bash

# send some test commands

mosquitto_pub -h localhost -t /test_cmd -m '["cmd", {"foo":1, "bar":2}]'
mosquitto_pub -h localhost -t /unrelated -m 'whatever'
