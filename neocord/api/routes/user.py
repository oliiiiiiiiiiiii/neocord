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
from typing import Any, Dict

from .base import BaseRouteMixin, Route
from neocord.typings.snowflake import Snowflake

class Users(BaseRouteMixin):
    def get_client_user(self):
        return self.request(Route('GET', '/users/@me'))

    def edit_client_user(self, payload: Dict[str, Any]):
        return self.request(Route('PATCH', '/users/@me'), json=payload)

    def get_user(self, user_id: Snowflake):
        return self.request(Route('GET', '/users/{user_id}', user_id=user_id))

    def create_dm(self, recipient_id: Snowflake):
        payload = {'recipient_id': recipient_id}
        return self.request(Route('POST', '/users/@me/channels'), json=payload)