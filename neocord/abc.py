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
from typing import Optional, List, TYPE_CHECKING

from neocord.internal.missing import MISSING
from neocord.internal import helpers
from neocord.models.message import Message, _MessageReferenceMixin

import asyncio

if TYPE_CHECKING:
    from neocord.models.base import DiscordModel
    from neocord.dataclasses.embeds import Embed
    from neocord.dataclasses.mentions import AllowedMentions
    from neocord.dataclasses.file import File
    from neocord.api.state import State

class Messageable:
    if TYPE_CHECKING:
        _state: State

    async def _get_messageable_channel(self) -> DiscordModel:
        raise NotImplementedError

    async def send(self,
        content: Optional[str] = None,
        *,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        delete_after: Optional[float] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        file: Optional[File] = None,
        files: Optional[List[File]] = None,
        reference: Optional[_MessageReferenceMixin] = None,
        mention_replied_user: Optional[bool] = None,
    ) -> Message:
        """
        Sends a message to the destination.

        Parameters
        ----------
        content: :class:`str`
            The content of message.
        embed: :class:`Embed`
            The embed shown in message. This parameter cannot be mixed with ``embeds``
        embeds: List[:class:`Embed`]
            The list of embeds shown in message. This parameter cannot be mixed with ``embed``
        file: :class:`File`
            The file sent in message. This parameter cannot be mixed with ``files``
        files: List[:class:`File`]
            The list of files sent in message. This parameter cannot be mixed with ``file``
        reference: Union[:class:`MessageReference`, :class:`Message`]
            The message reference to reply this message for.
        mention_replied_user: :class:`bool`
            Whether to mention the author when replying. When set, Overrides the
            :attr:`AllowedMentions.mention_replied_user`
        delete_after: :class:`float`
            The interval after which this message would be deleted automatically.

        Returns
        -------
        :class:`Message`
            The message that was sent.

        Raises
        ------
        Forbidden:
            You are not allowed to send message at this destination.
        HTTPError:
            The message sending failed somehow.
        """
        if file is not None and files is not None:
            raise TypeError('file and files parameter cannot be mixed.')

        channel = await self._get_messageable_channel()
        payload = helpers.parse_message_create_payload(
            self._state.client,
            content=content,
            embed=embed,
            embeds=embeds,
            allowed_mentions=allowed_mentions,
            reference=reference,
            mention_replied_user=mention_replied_user,
        )

        if file is not None:
            files = [file]

        if files:
            data = await self._state.http.create_message_with_files(
                channel_id=channel.id,
                payload=payload,
                files=files,
            )
        else:
            data = await self._state.http.create_message(
                channel_id=channel.id,
                payload=payload,
                )

        message = Message(data, state=self._state)

        if delete_after is not None:
            asyncio.create_task(self._delay_message_delete(delay=delete_after, message=message))

        return message

    async def _delay_message_delete(self, delay: float, message: Message):
        await asyncio.sleep(delay)
        await self.delete_message(message)

    async def edit_message(self, message: DiscordModel,
        content: Optional[str] = MISSING,
        *,
        embed: Optional[Embed] = MISSING,
        embeds: List[Embed] = MISSING,
        allowed_mentions: Optional[AllowedMentions] = MISSING,
        attachments: List[Attachment] = MISSING,
        suppress: Optional[bool] = MISSING,
        ):
        if embed is not MISSING and embeds is not MISSING:
            raise TypeError('embed and embeds parameters cannot be mixed.')

        payload = {}

        if content is not MISSING:
            payload['content'] = content
        if embed is not MISSING:
            embeds = [embed]
        if embeds:
            payload['embeds'] = [embed.to_dict()]

        if allowed_mentions is not MISSING:
            payload['allowed_mentions'] = allowed_mentions.to_dict()

        if attachments is not MISSING:
            if attachments is None:
                attachments = []

            payload['attachments'] = [a.to_dict() for a in attachments]

        if suppress:
            payload['flags'] = 1 << 2

        channel = await self._get_messageable_channel()
        await self._state.http.edit_message(channel_id=channel.id, message_id=message.id, payload=payload)

    async def delete_message(self, message: DiscordModel):
        """
        Deletes a message from the destination. A shorthand and a lower level of
        :meth:`Message.delete`.


        Parameters
        ----------
        message: :class:`Message`
            The message to delete.

        Raises
        ------
        Forbidden:
            You are not allowed to delete this message.
        HTTPError:
            The message deleting failed somehow.
        """
        channel = await self._get_messageable_channel()
        await self._state.http.delete_message(channel_id=channel.id, message_id=message.id)