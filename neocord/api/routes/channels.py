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
from typing import Any, Dict, Optional, TYPE_CHECKING

from .base import BaseRouteMixin, Route

import json
import aiohttp

if TYPE_CHECKING:
    from neocord.typings.snowflake import Snowflake

class Channels(BaseRouteMixin):

    def edit_channel(self, channel_id: Snowflake, payload, reason: Optional[str]):
        return self.request(Route('PATCH', '/channels/{channel_id}', channel_id=channel_id), json=payload, reason=reason)

    def delete_channel(self, channel_id: Snowflake, reason: Optional[str]):
        return self.request(Route('DELETE', '/channels/{channel_id}', channel_id=channel_id), reason=reason)

    def get_message(self, channel_id: Snowflake, message_id: Snowflake):
        route = Route('GET', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(route)

    def create_message(self, channel_id: Snowflake, payload: Any):
        route = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)
        return self.request(route, json=payload)

    def create_message_with_files(self, channel_id: Snowflake, files: List[File], payload: Any = None):
        route = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)

        form_data = aiohttp.FormData()
        if payload:
            form_data.add_field(name='payload_json', value=json.dumps(payload))

        for n, file in enumerate(files):
            form_data.add_field(
                name=f'file{n}',
                value=file.fp,
                filename=file.proper_name,
                content_type='application/octet-stream'
                )

        return self.request(route, data=form_data)

    def delete_message(self, channel_id: Snowflake, message_id: Snowflake):
        route = Route('DELETE', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(route)