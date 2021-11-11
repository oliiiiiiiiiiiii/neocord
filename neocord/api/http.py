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
from typing import Any, ClassVar, Optional, Union, Dict, TYPE_CHECKING

from neocord.errors.http import HTTPError, NotFound, Forbidden
from neocord.api.routes import Routes, Route
from neocord.internal.logger import logger

import neocord
import aiohttp
import asyncio

class HTTPClient(Routes):
    """
    Represents a HTTP client that interacts with Discord's REST API.
    """
    def __init__(self, *, session: Optional[aiohttp.ClientResponse] = None) -> None:
        self.token: Optional[str] = None
        self.session = None

    async def request(self, route: Route, **kwargs: Any) -> Any:
        self.reset()
        url = route.url

        headers = kwargs.pop('headers', {})
        headers.update(self._get_basic_headers())

        reason = kwargs.pop('reason', None)

        if reason is not None:
            headers.update({'X-Audit-Log-Reason': reason})

        response = await self.session.request(route.request, url, headers=headers, **kwargs) # type: ignore
        data: Union[str, Dict[str, Any]] = await self._get_data(response) # type: ignore

        if response.status < 300:
            # successful request
            return data
        if response.status == 429:
            retry_after: float = data["retry_after"] # type: ignore
            is_global = data.get('global', False) # type: ignore
            fmt = '{message}, Retrying after %ss' % str(retry_after)

            if is_global:
                msg = fmt.format(message='A global ratelimit has occured')
            else:
                msg = fmt.format(message='A ratelimit has occured')

            logger.warn(msg)
            await asyncio.sleep(retry_after)
            return await self.request(route, **kwargs)


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
