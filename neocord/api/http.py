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
from typing import Any, ClassVar, Optional, Union, Dict

from neocord.errors.http import HTTPError, NotFound, Forbidden

import neocord
import aiohttp

class Route:
    """
    Represents an endpoint from Discord API.
    """
    BASE: ClassVar[str] = 'https://discord.com/api/v9'

    def __init__(self, request: str, route: str, **params: Any) -> None:
        self.request = request
        self.route  = route
        self.params = params

    @property
    def url(self) -> str:
        return f'{self.BASE}{self.route.format(**self.params)}'

class HTTPClient:
    """
    Represents a HTTP client that interacts with Discord's REST API.
    """
    def __init__(self) -> None:
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None

    async def request(self, route: Route, **kwargs: Any) -> Any:
        self.reset()
        url = route.url

        headers = kwargs.pop('headers')
        headers.update(self._get_basic_headers())

        reason = kwargs.pop('reason')

        if reason is not None:
            headers.update({'X-Audit-Log-Reason': reason})

        response = await self.session.request(route.request, url, headers=headers, **kwargs) # type: ignore
        data: Union[str, Dict[str, Any]] = await self._get_data(response) # type: ignore

        if response.status < 300:
            # successful request
            return data
        if response.status == 404:
            raise NotFound(data) # type: ignore
        if response.status in [403, 401]:
            raise Forbidden(data) # type: ignore
        if response.status >= 500:
            raise HTTPError(data) # type: ignore


    async def _get_data(self, response: aiohttp.ClientResponse) -> Any:
        if response.headers['Content-Type'] == 'application/json':
            return (await response.json())

        return (await response.text())


    def _get_basic_headers(self):
        return {
            "User-Agent": f"DiscordBot (https://github.com/nerdguyahmad/neocord, {neocord.__version__})",
            "Authorization": f"Bot {self.token}"
        }

    def reset(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()