# MIT License

# Copyright (c) 2021 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations
from typing import Any, Optional, Dict, TYPE_CHECKING

from neocord.internal.mixins import ClientPropertyMixin
from neocord.internal.logger import logger

import sys
import asyncio
import aiohttp
import zlib
import json
import threading
import time

if TYPE_CHECKING:
    from neocord.core import Client

class OP:
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

class Heartbeater(threading.Thread):
    """
    A thread that handles sending of heartbeats after the provided interval.
    """
    def __init__(self, ws: DiscordWebsocket) -> None:
        self.interval: Optional[int] = None
        self.ws = ws
        self.last_beat: Optional[float] = None
        super().__init__(
            target=self._handler,
            daemon=True,
            name='neocord-heartbeat-handler'
            )

    def ack(self):
        self.last_beat = time.time()

    def _handler(self):
        while not self.ws.is_closed():
            asyncio.run(self.ws.heartbeat())
            # interval should not be None here as this
            # thread is only started after interval is set i.e after HELLO
            # op code.
            # also, time.sleep shouldn't block our main loop because this
            # is a separate thread.
            time.sleep(self.interval) # type: ignore


class DiscordWebsocket(ClientPropertyMixin):
    """
    A private class that implements the internal working for management of websocket
    connection from Discord gateway.
    """
    if TYPE_CHECKING:
        socket: Optional[aiohttp.ClientWebSocketResponse]

    def __init__(self, client: Client) -> None:
        self.client = client
        self.socket = None


        # websocket related data

        # fmt: off
        self.session_id = None
        self.sequence   = None
        self.hb         = Heartbeater(ws=self)
        self.inflator   = zlib.decompressobj()
        self.buffer     = bytearray()
        # fmt: on

    # helpers

    async def receive(self) -> Optional[Dict[str, Any]]:
        data = await self.socket.receive()
        data = data.data

        if not data:
            return

        if isinstance(data, bytes):
            self.buffer.extend(data)

            if len(data) < 4 or data[-4:] != b'\x00\x00\xff\xff':
                return

            data = self.inflator.decompress(self.buffer)
            data = data.decode('utf-8')
            self.buffer = bytearray()

        data = json.loads(data)
        return data

    async def send_json(self, data):
        await self.socket.send_str(json.dumps(data))

    def is_closed(self) -> bool:
        if self.socket is None:
            # socket is not set yet, so it's closed.
            return True

        return self.socket.closed

    # packets stuff

    async def heartbeat(self):
        logger.debug('Sending HEARTBEAT packet')
        await self.send_json({
            "op": OP.HEARTBEAT,
            "d": self.sequence
        })
        if self.hb.last_beat is not None:
            print(self.hb.last_beat, time.time())
            previous = self.hb.last_beat
            self.hb.last_beat = time.time()
            diff = self.hb.interval - (self.hb.last_beat - previous)

            if diff > 5:
                logger.warn('Heartbeat was blocked for more then {}s'.format(diff))
        else:
            self.hb.last_beat = time.time()

    async def identify(self):
        logger.debug('Sending IDENTIFY packet.')
        await self.send_json({
            "op": OP.IDENTIFY,
            "d": {
                "token": self.http.token,
                "intents": self.client.intents.value,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "NeoCord",
                    "$device": "NeoCord"
                },
                "compress": True,
            }
        })

    async def handle_events(self):
        while not self.is_closed():
            msg = await self.receive()
            if not msg:
                continue

            op = msg['op']
            data = msg['d']
            sequence = msg.get('s')

            if sequence is not None:
                # update our sequence with the one that we just got.
                self.sequence = sequence

            # main logging in (connection to gateway) logic here:
            if op == OP.HELLO:
                # we have got HELLO (10) OP code which is sent initally and
                # now we have to start heartbeating and identify the session.
                self.hb.interval = data['heartbeat_interval'] / 1000.0
                self.hb.start()

                await self.identify()

            elif op == OP.HEARTBEAT:
                # Recieved request to heartbeat, sending an immediate heartbeat
                await self.heartbeat()
            elif op == OP.DISPATCH:
                if msg['t'] == 'READY':
                    logger.info('Successfully connected to Gateway.')
                    self.session_id = data['session_id']

                self.state.parse_event(event=msg['t'], data=msg['d'])

    async def connect(self, url: str):
        url = url + '?v=9&encoding=json&compress=zlib-stream'
        self.socket = await self.http.ws_connect(url)
        await self.handle_events()