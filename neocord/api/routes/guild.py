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

if TYPE_CHECKING:
    from neocord.typings.snowflake import Snowflake

class Guilds(BaseRouteMixin):

    def get_guild(self, guild_id: Snowflake):
        return self.request(Route('GET', '/guilds/{guild_id}', guild_id=guild_id))

    # roles management

    def edit_role(self, guild_id: Snowflake, role_id: Snowflake, payload: Dict[str, Any], reason: Optional[str]):
        return self.request(
            Route('PATCH', '/guilds/{guild_id}/roles/{role_id}', role_id=role_id, guild_id=guild_id),
            json=payload,
            reason=reason
            )

    def edit_role_position(self, guild_id: Snowflake, payload: Dict[str, Any], reason: Optional[str]):
        return self.request(Route('PATCH', '/guilds/{guild_id}/roles', guild_id=guild_id), json=payload, reason=reason)

    def delete_role(self, guild_id: Snowflake, role_id: Snowflake, reason: Optional[str]):
        return self.request(Route('DELETE', '/guilds/{guild_id}/roles/{role_id}', guild_id=guild_id, role_id=role_id), reason=reason)

    # members management

    def get_guild_member(self, guild_id: Snowflake, member_id: Snowflake):
        route = Route('GET', '/guilds/{guild_id}/members/{member_id}', guild_id=guild_id, member_id=member_id)
        return self.request(route)

    def edit_guild_member(self, guild_id: Snowflake, member_id: Snowflake, payload: Any, reason: str = None):
        route = Route('PATCH', '/guilds/{guild_id}/members/{member_id}', guild_id=guild_id, member_id=member_id)
        return self.request(route, json=payload, reason=reason)

    def kick_guild_member(self, guild_id: Snowflake, member_id: Snowflake, reason: str = None):
        route = Route('DELETE', '/guilds/{guild_id}/members/{member_id}', guild_id=guild_id, member_id=member_id)
        return self.request(route, reason=reason)

    # emojis management

    def get_guild_emojis(self, guild_id: Snowflake):
        return self.request(Route('GET', '/guilds/{guild_id}/emojis', guild_id=guild_id))

    def get_guild_emoji(self, guild_id: Snowflake, emoji_id: Snowflake):
        return self.request(Route('GET', '/guilds/{guild_id}/emojis/{emoji_id}', guild_id=guild_id, emoji_id=emoji_id))

    def create_guild_emoji(self, guild_id: Snowflake, payload, reason: str = None):
        return self.request(Route('POST', '/guilds/{guild_id}/emojis', guild_id=guild_id), reason=reason, json=payload)

    def delete_guild_emoji(self, guild_id: Snowflake, emoji_id: Snowflake, reason: str = None):
        return self.request(Route('DELETE', '/guilds/{guild_id}/emojis/{emoji_id}', guild_id=guild_id, emoji_id=emoji_id), reason=reason)

    def edit_guild_emoji(self, guild_id: Snowflake, emoji_id: Snowflake, payload, reason: str = None):
        return self.request(Route('PATCH', '/guilds/{guild_id}/emojis/{emoji_id}', guild_id=guild_id, emoji_id=emoji_id), reason=reason, json=payload)

    # scheduled events management

    def get_guild_events(self, guild_id: Snowflake):
        return self.request(Route('GET', '/guilds/{guild_id}/scheduled-events', guild_id=guild_id))

    def get_guild_event(self, guild_id: Snowflake, event_id: Snowflake):
        return self.request(Route('GET', '/guilds/{guild_id}/scheduled-events/{event_id}', guild_id=guild_id, event_id=event_id))

    def create_guild_event(self, guild_id: Snowflake, payload):
        return self.request(Route('POST', '/guilds/{guild_id}/scheduled-events', guild_id=guild_id), json=payload)

    def edit_guild_event(self, guild_id: Snowflake, event_id: Snowflake, payload):
        return self.request(Route('PATCH', '/guilds/{guild_id}/scheduled-events/{event_id}', guild_id=guild_id, event_id=event_id), json=payload)

    def delete_guild_event(self, guild_id: Snowflake, event_id: Snowflake):
        return self.request(Route('DELETE', '/guilds/{guild_id}/scheduled-events/{event_id}', guild_id=guild_id, event_id=event_id))

    def get_guild_event_subscribers(self, guild_id: Snowflake, event_id: Snowflake):
        return self.request(Route('GET', '/guilds/{guild_id}/scheduled-events/{event_id}/users', guild_id=guild_id, event_id=event_id))

