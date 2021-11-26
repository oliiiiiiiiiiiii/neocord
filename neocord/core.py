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
from asyncio.coroutines import iscoroutinefunction
from neocord.api.gateway import DiscordWebsocket
from typing import Any, Union, Literal, Callable, Dict, List, Optional, TYPE_CHECKING

from neocord.api.http import HTTPClient
from neocord.api.state import State
from neocord.models.user import ClientUser
from neocord.dataclasses.flags.intents import GatewayIntents

import asyncio

if TYPE_CHECKING:
    from neocord.models.user import User
    from neocord.models.message import Message
    from neocord.models.guild import Guild

class Client:
    """
    Represents a client that interacts with the Discord API. This is the starter
    point of any bot and core class for creating discord bots.

    This class takes no required parameters in initalization however a number
    of parameters can be passed in the initalization to modify the behaviour of
    class as needed. All parameters are optional and keyword-only.

    Parameters
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The asyncio event loop to use. if not provided, it will be obtained by calling
        :func:`asyncio.get_event_loop` function.
    session: :class:`aiohttp.ClientSession`
        The aiohttp session to use in HTTP or websocket operations. if not provided, Library
        creates it's own session.
    intents: :class:`GatewayIntents`
        The gateway intents to use while connecting to gateway. If not provided, all the
        unprivelged intents are enabled by default.
    message_cache_limit: :class:`int`
        The amount of messages that would be cached by the client at a time. This can be no larger
        then 1000. 0 can be passed to disable the message cache. On reaching this amount,
        The client would discard all the previous messages and would start re-filling
        the cache. Defaults to ``500``
    allowed_mentions: :class:`AllowedMentions`
        The global mentions configuration that applies to every bot's message. This can
        be overridden per message.
    """
    if TYPE_CHECKING:
        loop: asyncio.AbstractEventLoop
        _listeners: Dict[str, List[Callable[..., Any]]]
        intents: GatewayIntents

    def __init__(self, **params: Any) -> None:
        self.loop  = params.get('loop') or asyncio.get_event_loop()
        self.intents = params.get('intents') or GatewayIntents.unprivileged()
        self.message_cache_limit = params.get('message_cache_limit', 500)

        if self.message_cache_limit is None:
            self.message_cache_limit = 0
        elif self.message_cache_limit > 1000:
            raise ValueError('message cache limit cannot be larger then 1000.')

        self.allowed_mentions = params.get('allowed_mentions')

        # internal stuff:
        self.http  = HTTPClient(session=params.get('session'))
        self.ws = DiscordWebsocket(client=self)
        self.state = State(client=self)
        self._ready = asyncio.Event(loop=self.loop)
        self._listeners = {}
        self._connect_hook_called = False

    def dispatch(self, event: str, *args: Any):
        if not self._ready.is_set():
            return

        # call the event first
        coro = getattr(self, f'on_{event}', None)
        if coro:
            asyncio.create_task(coro(), name=f'neocord-event-dispatch: {event}')

        try:
            listeners = self._listeners[event]
        except KeyError:
            return

        to_remove: List[Callable[..., Any]] = []


        for listener in listeners:
            coro = listener(*args)
            asyncio.create_task(coro, name='neocord-event-dispatch: {}'.format(event))
            try:
                options = listener.__neocord_event_listener_options__
            except AttributeError:
                options = {}

            if options.get('once', False):
                to_remove.append(listener)

        for listener in to_remove:
            try:
                self._listeners[event].remove(listener)
            except:
                continue

    async def connect_hook(self):
        """
        A hook that is called whenever the client connects initially to
        the Discord gateway.

        By default, This method does nothing however, it can be overridden to add
        functionality like creating a database connection etc.

        Note that this hook is called *BEFORE* ready event is fired which means
        that you shouldn't rely on client's cache in this hook as it is more then likely
        that it is not filled at all or is in process of filling.
        """
        pass

    def is_ready(self) -> bool:
        """
        Returns a boolean representation of whether the client is in ready state,
        as such client has connected to Discord and has successfully filled
        the internal cache.

        Returns
        -------
        :class:`bool`
            Whether the client is ready or not.
        """
        return self._ready.is_set()

    async def wait_until_ready(self) -> None:
        """
        A coroutine that waits until the client is in ready state. The client is
        considered in ready state when it has connected to Discord websocket and has
        successfully filled the internal cache.
        """
        await self._ready.wait()

    async def login(self, token: str) -> None:
        """
        Logins to Discord using an authorization bot token.

        This method does not establishes a websocket connection but simply
        logins by fetching the information of the client user associated with the
        token.

        Parameters
        ----------
        token: :class:`str`
            The token that should be used for login.
        """
        self.http.token = token.strip()
        data = await self.http.get_client_user()

        self.state.user = ClientUser(data, self.state)

    async def connect(self):
        """
        Connects to the Discord websocket. This method must be called after logging
        in, i.e after calling :meth:`.login`

        A shorthand :meth:`.start` can also be used that calls :meth:`.login` and
        :meth:`.connect`.
        """
        url = (await self.http.get_gateway())['url']
        await self.ws.connect(url)

    async def start(self, token: str):
        """
        A short-hand coroutine that logins and connects to Discord websocket.

        This one coroutine is roughly equivalent to
        :meth:`.login` + :meth:`.connect`

        Parameters
        ----------
        token: :class:`str`
            The token that should be used for login.
        """
        await self.login(token)
        await self.connect()

    def run(self, token: str):
        """
        A blocking method that runs the client. This abstracts away the asyncio event
        loop handling.

        Parameters
        ----------
        token: :class:`str`
            The token that should be used for login.
        """
        async def runner():
            await self.login(token)
            await self.connect()

        if self.loop.is_running():
            asyncio.ensure_future(runner())
        else:
            self.loop.run_until_complete(runner())

    # listeners

    def event(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        A decorator that registers a callback for an event.

        Example::

            @client.event
            async def on_ready():
                print('Ready called')

        This is equivalent to:

        Example::

            class Client(neocord.Client):
                def __init__(self):
                    ...

                async def on_ready():
                    print('Ready called.')

        .. warning::
            You cannot register multiple callbacks using this decorator, Consider
            using listeners API for that. See documentation for :meth:`.on` decorator.

        .. note::
            The callback's name MUST be prefixed with ``on_``.
        """
        if not iscoroutinefunction(func):
            raise TypeError('callback function must be a coroutine.')

        setattr(self, func.__name__, func)
        return func

    def clear_listeners(self, event: str) -> None:
        """
        Removes all the listeners for the provided event.

        Parameters
        ----------
        event: :class:`str`
            The event name to clear listeners for.
        """
        try:
            del self._listeners[event]
        except KeyError:
            return

    def get_listeners(self, event: str, *, include_temporary: bool = False) -> List[Callable[..., Any]]:
        """
        Returns the registered event listeners for the provided event.

        Parameters
        ----------
        event: :class:`str`
            The event name to get listeners for.
        include_temporary: :class:`bool`
            Whether to include temporary listeners, i.e those that are marked
            to call only once. Defaults to False. Setting this to True would also
            return the internal listeners i.e the one's that were added by :meth:`.wait_for`

        Returns
        -------
        The list of event listeners callbacks.
        """
        try:
            listeners = self._listeners[event]
        except KeyError:
            return []

        if not include_temporary:
            listeners = [l for l in listeners if not l.__neocord_event_listener_options__.get('once', False)]

        return listeners

    def add_listener(self,
        listener: Callable[..., Any],
        name: str,
        *,
        once: bool = False
        ) -> Callable[..., Any]:
        """
        Adds an event listener to the bot.

        This is a non-decorator and lower level interface to :meth:`.on` decorator. Consider
        using it instead as it is more easy to use.

        Example::
            async def on_message(message):
                ...

            bot.add_listener(on_message, 'message')

        Parameters
        ----------
        listener:
            The async function that represents the event's callback.
        name: :class:`str`
            The name of event to listen to.
        once: :class:`bool`
            Whether this listener should be called only once.
        """
        if not iscoroutinefunction(listener):
            raise TypeError('listener callback must be a coroutine.')

        if name.startswith('on_'):
            name = name[3:]

        listener.__neocord_event_listener_options__ = {}
        listener.__neocord_event_listener_options__['once'] = once

        try:
            self._listeners[name].append(listener)
        except KeyError:
            self._listeners[name] = [listener]

        return listener

    def on(self, *args, **kwargs):
        """
        A decorator that registers a listener to listen to gateway events.

        Example::

            @client.on('ready')
            # or
            # @client.on('on_ready')

            async def ready_event():
                print('Ready.')

        Unlike :meth:`.event`, You can register as many events you want.

        Example::

            @client.on('ready')
            async def ready1():
                print('Ready called.')

            @client.on('ready')
            async def ready2():
                print('Ready 2 called.')

        Parameters
        ----------
        name: :class:`str`
            The name of event to listen to.
        once: :class:`bool`
            Whether this listener should be called only once.
        """
        def deco(func: Callable[..., Any]):
            return self.add_listener(func, *args, **kwargs)

        return deco

    async def wait_for(self, event: str, *, check: Optional[Callable[..., bool]] = None, timeout: Union[int, float] = None):
        """
        Waits for an event to dispatch.

        This method returns the tuple of arguments that belong to the event.

        Example::

            message = await bot.wait_for('message', check=lambda m: m.author.id == 1234, timeout=60.0)
            if message.content == 'yes':
                await message.channel.send('Affirmative.')
            else:
                await message.channel.send('Negative.')

        Parameters
        -----------
        event: :class:`str`
            The event to wait for.
        check:
            The check that will be checked for when returning result. This CANNOT be a
            coroutine.
        timeout: :class:`float`
            The timeout after which this method would stop.

        Raises
        ------
        asyncio.TimeoutError
            The timeout period expired and event was not dispatched.
        """
        if not check:
            def _check(*args: Any) -> Literal[True]:
                return True

            check = _check

        future = asyncio.Future()

        async def listener(*args: Any):
            # this is basically our internal listener that checks
            # whether provided check function satisfies True with the
            # args.
            # if it does, we simply set the result.
            # if it does not, we would keep on re-adding the listener with once set
            # to True until the check satisfies.
            if check(*args):
                future.set_result(args)
            else:
                # the check failed so re-add this listener.
                self.add_listener(listener, event, once=True)

        self.add_listener(listener, event, once=True)
        result = await asyncio.wait_for(future, timeout=timeout)

        if len(result) == 1:
            result = result[0]

        return result

    @property
    def user(self) -> Optional[ClientUser]:
        """
        :class:`ClientUser`: Returns the user associated to this client. This is only available
        after the client has logged in.
        """
        return self.state.user

    def get_user(self, id: int, /) -> Optional[User]:
        """
        Gets a user from the client's internal cache. This method
        returns None is the user is not found in internal cache.

        Parameters
        ----------
        id: :class:`int`
            The ID of the user.

        Returns
        -------
        :class:`User`
            The requested user.
        """
        return self.state.get_user(id)

    async def fetch_user(self, id: int) -> User:
        """
        Fetches a user from the API.

        This is an API call. For general usage and if you have member
        intents enabled, you can use :meth:`.get_user`

        Parameters
        ----------
        id: :class:`int`
            The ID of the user.

        Raises
        ------
        NotFound
            Provided user ID is invalid.
        HTTPError
            The user fetch failed somehow.

        Returns
        -------
        :class:`User`
            The requested user.
        """
        data = await self.http.get_user(id)
        user = self.state.add_user(data)
        return user

    def get_guild(self, id: int, /) -> Optional[Guild]:
        """
        Gets a guild from the client's internal cache. This method
        returns None is the guild is not found in internal cache.

        Parameters
        ----------
        id: :class:`int`
            The ID of the guild.

        Returns
        -------
        :class:`Guild`
            The requested guild.
        """
        return self.state.get_guild(id)

    async def fetch_guild(self, id: int) -> Optional[Guild]:
        """
        Fetches a guild from the API.

        This is an API call. you can use :meth:`.get_guild`

        Parameters
        ----------
        id: :class:`int`
            The ID of the guild.

        Raises
        ------
        NotFound
            Provided guild ID is invalid.
        HTTPError
            The guild fetch failed somehow.

        Returns
        -------
        :class:`Guild`
            The requested guild.
        """
        data = await self.http.get_guild(id)
        guild = self.state.create_guild(data)
        return guild


    def get_message(self, id: int, /) -> Optional[Message]:
        """
        Gets a message from the client's internal cache. This method
        returns None is the message is not found in internal cache.

        Parameters
        ----------
        id: :class:`int`
            The ID of the message.

        Returns
        -------
        :class:`Message`
            The requested message, if found.
        """
        return self.state.get_message(id)

    async def fetch_stage_instance(self, channel_id: int, /):
        """Fetches a stage instance by the stage channel ID.

        This is an API call. Consider using :meth:`Guild.get_stage_instance` or
        :attr:`StageChannel.instance` instead.

        Parameters
        ----------
        id: :class:`int`
            The ID of stage channel.

        Returns
        -------
        :class:`StageInstance`
            The fetched stage instance.

        Raises
        ------
        NotFound
            The stage instance was not found.
        HTTPError
            An error occured while fetching.
        """
        data = await self.http.get_stage_instance(channel_id=channel_id)
        return StageInstance(data, state=self.state)