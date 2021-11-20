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
from typing import Any, Optional, Union, Dict

from neocord.errors.http import *
from neocord.api.routes import Routes, Route
from neocord.internal.logger import logger

import neocord
import aiohttp
import asyncio

class RatelimitHandler:
    def __init__(self):
        self._ratelimit_over = asyncio.Event()
        self._ratelimit_over.set()

    def is_ratelimited(self):
        return (not self._ratelimit_over.is_set())

    def wait_until_over(self):
        return self._ratelimit_over.wait()

    def set_ratelimit(self):
        return self._ratelimit_over.clear()

    def clear_ratelimit(self):
        return self._ratelimit_over.set()


class HTTPClient(Routes):
    """
    Represents a HTTP client that interacts with Discord's REST API.
    """
    def __init__(self, *, session: Optional[aiohttp.ClientResponse] = None) -> None:
        self.token: Optional[str] = None
        self.session = None
        self.ratelimit_handler = RatelimitHandler()

    async def request(self, route: Route, **kwargs: Any) -> Any:
        self.reset()
        url = route.url

        headers = kwargs.pop('headers', {})
        headers.update(self._get_basic_headers())

        reason = kwargs.pop('reason', None)

        if reason is not None:
            headers.update({'X-Audit-Log-Reason': reason})

        if self.ratelimit_handler.is_ratelimited():
            await self.ratelimit_handler.wait_until_over()

        # this loop is primarily for ratelimit handling
        response = None
        for tries in range(5):
            try:
                async with self.session.request(route.request, url, headers=headers, **kwargs) as response: # type: ignore
                    if not response.status >= 500:
                        data: Union[str, Dict[str, Any]] = await self._get_data(response) # type: ignore

                    if response.status < 300:
                        # successful request
                        logger.debug('HTTP request was successfully done. Returned with status {}'.format(response.status))
                        return data # type: ignore
                    if response.status == 429:
                        retry_after: float = data["retry_after"] # type: ignore
                        is_global = data.get('global', False) # type: ignore

                        fmt = '{message}, Retrying after %ss (%s %s)' % (str(retry_after), route.request, route.route)

                        if is_global:
                            msg = fmt.format(message='A global ratelimit has occured')
                            self.ratelimit_handler.set_ratelimit()
                        else:
                            msg = fmt.format(message='A ratelimit has occured')

                        logger.warn(msg)
                        await asyncio.sleep(retry_after)

                        if is_global:
                            logger.info('Global ratelimit is over.')
                            self.ratelimit_handler.clear_ratelimit()

                        continue

                    # TODO: Add more handlers here.

                    if response.status == 404:
                        raise NotFound(response, data) # type: ignore
                    if response.status in [403, 401]:
                        raise Forbidden(response, data) # type: ignore
                    if response.status in (500, 502, 504):
                        await asyncio.sleep(1 + tries * 2)
                        continue

            except OSError as err:
                if tries < 4 and err.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise err

        if response is not None:
            raise HTTPRequestFailed(response)



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
