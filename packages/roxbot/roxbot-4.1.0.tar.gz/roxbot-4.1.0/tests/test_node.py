import pytest
import asyncio
import os

from roxbot import Node

if os.environ.get("CI"):
    pytestmark = pytest.mark.skip(reason="Can't run in CI.")


class MyNode(Node):
    """custom node"""

    def __init__(self) -> None:
        super().__init__()
        self._coros.append(self._on_init)

    async def _on_init(self) -> None:
        self._log.info("Running custom init coroutine")


@pytest.mark.asyncio
async def test_node_instance() -> None:
    node = Node()
    task = asyncio.create_task(node.main())

    # Allow some time for the node to start
    await asyncio.sleep(0.1)

    with pytest.raises(RuntimeError):
        await node.main()

    await asyncio.sleep(1)
    await node.stop()
    await task  # Ensure the main task is awaited to finish cleanly


@pytest.mark.asyncio
async def test_custom_node_instance() -> None:
    node = MyNode()
    task = asyncio.create_task(node.main())

    # Allow some time for the node to start
    await asyncio.sleep(0.1)

    await node.stop()
    await task
