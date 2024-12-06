"""WebsocketServer class module."""

import asyncio
import json
import logging
import websockets

from zmc.components.core import BaseComponent
from zmc.components.core import ValueReceiverBaseComponent
from zmc.version import __version__

from .async_utils import cancellable, async_repeat
from .connector import Connector


__all__ = ["WebSocketClient"]


# User friendly error message regarding the fact that a component that does not
# allow for setting a value was sent a value from the Mission Control app.
SETTING_VALUE_ON_NON_SETTER_ERROR_TEMPLATE = (
    "Component id, '{}', was attached to a component that does not expect to "
    "receive any values. However, the Mission Control app is sending values to "
    "the component with this id.\nPlease verify that you are using the right "
    "id when initializing this component."
)

# Rate (in Hz) at which messages will be sent over websockets.
_THROTTLE_RATE = 61


class WebSocketClient(Connector):
    """Server that allows caller to open up a websocket on a separate thread.

    Args:
        - host: host as per similarly named asyncio.serve() function parameter
        - port: port as per similarly named asyncio.serve() function parameter
        - gui_id: id of the gui this server is going to connect to.
    """

    def __init__(self, host, port, gui_id):
        super().__init__()
        self.uri = f"ws://{host}:{port}"
        self.gui_id = gui_id

        # Client/websocket related attributes
        self.__websocket = None
        self.__data_component_queue = asyncio.Queue()

    def _reset(self):
        self.__websocket = None
        self.__data_component_queue = asyncio.Queue()

    @cancellable
    async def _send_all_component_data(self, components):
        if self.__websocket is None or not self.__websocket.open:
            return

        data_event = {
            "type": "send-all-data",
            "guiId": self.gui_id,
            "components": [
                {
                    "componentId": component.id,
                    "data": component.data,
                }
                for component in components.values()
            ],
            "pyVersion": __version__,
        }
        json_data_event = json.dumps(data_event)
        try:
            await self.__websocket.send(json_data_event)
        except websockets.ConnectionClosed:
            self.__websocket = None

    @cancellable
    @async_repeat(1 / _THROTTLE_RATE)
    async def _send_queued_component_data_loop(self):
        await self._send_queued_component_data()

    @cancellable
    async def _send_queued_component_data(self):
        items = {}
        while not self.__data_component_queue.empty():
            component = await self.__data_component_queue.get()
            items[component.id] = component
        if items:
            await self._send_all_component_data(items)

    async def _send_component_data(self, component):
        """Queues up component data to be sent at regular intervals."""
        await self.__data_component_queue.put(component)

    # TODO: should refactor this to be a little more palettable
    async def _websocket_receiver(self):
        if self.__websocket is None:
            return

        async for message in self.__websocket:
            event = json.loads(message)
            # TODO: handle app versions (for future proofing as things change)
            _app_version = event["app_version"]
            if event["type"] == "set-value":
                component_id = event["component_id"]
                component = BaseComponent.registry.get(component_id, None)
                if component is None:
                    continue  # Didn't find component. Do nothing and skip.
                if not isinstance(component, ValueReceiverBaseComponent):
                    raise ValueError(
                        SETTING_VALUE_ON_NON_SETTER_ERROR_TEMPLATE.format(
                            component.id
                        )
                    )
                value = event.get("value", None)
                self._execute_in_new_thread(component.receive_value, value)

            if event["type"] == "initialize":
                logging.debug("Initializing script")
                components = event["components"]
                for component_json in components:
                    component_id = component_json["component_id"]
                    component = BaseComponent.registry.get(component_id, None)
                    if component is None:
                        continue  # Didn't find component. Do nothing and skip.
                    value = component_json.get("value", None)
                    if not value:
                        continue  # No value to update.
                    if not isinstance(component, ValueReceiverBaseComponent):
                        raise ValueError(
                            SETTING_VALUE_ON_NON_SETTER_ERROR_TEMPLATE.format(
                                component.id
                            )
                        )
                    self._execute_in_new_thread(component.receive_value, value)
                self.is_connected = True  # Signal that a connection is ready
            if event["type"] == "kill-func":
                self._exit_original_thread()

    async def _start_websocket_handlers(self):
        receiver_task = asyncio.create_task(self._websocket_receiver())
        send_queued_data_task = asyncio.create_task(
            self._send_queued_component_data_loop()
        )

        done, pending = await asyncio.wait(
            [receiver_task, send_queued_data_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()
        self.__websocket = None

        for task in done:
            try:
                error = task.exception()
                if error is not None:
                    self._handle_thread_exception(error)
            except asyncio.CancelledError:
                pass

    async def _start_connector(self):
        is_connected = False
        while not is_connected:
            try:
                self.__websocket = await websockets.connect(
                    self.uri,
                    # gui_id key must not contain any capital letters.
                    extra_headers={"gui_id": self.gui_id},
                )
                is_connected = True
            except OSError:
                logging.warning(
                    "Failed to connect websocket. Retrying in 1 second..."
                )
                await asyncio.sleep(1)
        # Start the websocket handlers asynchronously
        asyncio.create_task(self._start_websocket_handlers())

    async def _stop_connector(self):
        if self.__websocket is not None and self.__websocket.open:
            # Send whatever data is still queued before closing connection.
            await self._send_queued_component_data()
            await self.__websocket.close()

        self._reset()
