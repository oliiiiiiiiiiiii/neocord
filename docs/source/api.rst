.. currentmodule:: neocord

API Reference
===============

The section dives into every aspect of the core API of NeoCord.

Core
----

Client
~~~~~~~

.. autoclass:: Client()
    :members:

Events Reference
----------------

This section outlines the gateway events. These events are sent by Discord over websocket
and can be listened to, using the events listener.

Listening to events
~~~~~~~~~~~~~~~~~~~~

A very basic way of listening to an event is simply overriding it::

    class MyClient(neocord.Client):
        async def on_ready():
            print('The bot is ready.')

However, there is another easy way of doing above task::

    @client.event
    async def on_ready():
        print('The bot is ready.')

Both methods are equivalent.

However there are one problem here, that you cannot register multiple events listeners using
above method and that's why library provides a more granular system for listeners handling that
is using :meth:`Client.on` decorator::

    @client.on('ready')
    # or
    # @client.on('on_ready')
    async def ready_listener():
        print('The bot is ready.')

You can easily register any number of listeners you want using this method. See relevant
documentation for more information.

Below section will list all the gateway events that are sent by Discord and can be listened
to.

Library Events
~~~~~~~~~~~~~~~~

.. function:: on_ready

    An event that fires when the client's internal cache is completely filled.

    Important point to note is that this event is not guranteed to call once and similarly,
    This is also not the very first event to call.

    You shouldn't rely on this event to do initial stuff as this event can fire many times.

    Consider using :meth:`Client.connect_hook` if you want a hook that calls initally and
    only once.

.. function:: on_socket_dispatch(event, data)

    .. note::
        This is a debug event and will not be called unless opted-in. To enable debug events,
        Set ``debug_events`` to True in :class:`Client`.

    .. warning::
        You should never enable ``debug_events`` in production enivornment as it
        can cause performance issues.

    Calls when an event dispatch is sent by Discord gateway.

    :param event: The name of event.
    :type event: :class:`str`

    :param data: The raw event data.

User Events
~~~~~~~~~~~~

.. function:: on_user_update(user)

    Calls when properties of a discord user like name, avatar etc. change.

    :param before: The user before update.
    :type before: :class:`User`
    :param after: The user after update.
    :type after: :class:`User`

Guild Events
~~~~~~~~~~~~~~

.. function:: on_guild_join(guild)

    Calls when a guild is joined by the client user.

    Requires :attr:`GatewayIntents.guilds` to be enabled.


    :param guild: The guild that was joined.
    :type guild: :class:`Guild`


.. function:: on_guild_update(before, after)

    Calls when properties of a guild is changed.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param before: The guild before update.
    :type before: :class:`Guild`

    :param after: The guild after update.
    :type after: :class:`Guild`


.. function:: on_guild_delete(guild)

    Calls when a guild is deleted i.e became unavailable due to an outage,
    the client user was removed etc.

    Consider using :func:`on_guild_leave` or :func:`on_guild_unavailable` for only leave or unavailable events
    respectively.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param guild: The guild that was deleted.
    :type guild: :class:`Guild`


.. function:: on_guild_leave(guild)

    Calls when client user leaves a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param guild: The guild that was left.
    :type guild: :class:`Guild`

.. function:: on_guild_unavailable(guild)

    Calls when a guild becomes unavailable due to an outage etc.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param guild: The guild that became unavailable.
    :type guild: :class:`Guild`


Member Events
~~~~~~~~~~~~~~

.. function:: on_member_join(member)

    Calls when a member joins a guild etc.

    Requires :attr:`GatewayIntents.members` to be enabled.

    :param member: The joined member.
    :type member: :class:`GuildMember`



.. function:: on_member_leave(member)

    Calls when a member leaves a guild etc.

    Requires :attr:`GatewayIntents.members` to be enabled.

    :param member: The member who left the guild.
    :type member: :class:`GuildMember`


.. function:: on_member_update(before, after)

    Calls when properties of a guild member updates like nickname change, avatar change etc.

    Requires :attr:`GatewayIntents.members` to be enabled.

    :param before: The member before update.
    :type before: :class:`GuildMember`

    :param after: The member after update.
    :type after: :class:`GuildMember`

Role Events
~~~~~~~~~~~~

.. function:: on_role_create(role)

    Calls when a role is created in a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param role: The created role.
    :type role: :class:`Role`


.. function:: on_role_update(before, after)

    Calls when a role is updated in a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param before: Role before the update.
    :type before: :class:`Role`

    :param after: Role after the update.
    :type after: :class:`Role`

.. function:: on_role_delete(role)

    Calls when a role is deleted in a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param role: The deleted role.
    :type role: :class:`Role`

Channel Events
~~~~~~~~~~~~~~~

.. function:: on_channel_create(channel)

    Calls when a channel is created in a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param channel: The created channel.
    :type channel: :class:`GuildChannel`


.. function:: on_channel_update(before, after)

    Calls when a channel's properties are updated in a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param before: Channel before the update.
    :type before: :class:`GuildChannel`

    :param after: Channel after the update.
    :type after: :class:`GuildChannel`

.. function:: on_channel_delete(channel)

    Calls when a channel is deleted in a guild.

    Requires :attr:`GatewayIntents.guilds` to be enabled.

    :param channel: The deleted channel.
    :type channel: :class:`GuildChannel`

Message Events
~~~~~~~~~~~~~~

.. function:: on_message(message)

    Calls when a message is sent in either a guild channel or a DM channel.

    Requires :attr:`GatewayIntents.messages` to be enabled.

    :param message: The sent message.
    :type message: :class:`Message`

Scheduled Events
~~~~~~~~~~~~~~~~~

.. function:: on_scheduled_event_create(event)

    Calls when a scheduled event is created in a guild.

    Requires :attr:`GatewayIntents.scheduled_events` to be enabled.

    :param event: The created scheduled event.
    :type event: :class:`ScheduledEvent`


.. function:: on_scheduled_event_update(before, after)

    Calls when a scheduled event's properties are updated.

    Requires :attr:`GatewayIntents.scheduled_events` to be enabled.

    :param before: Scheduled event before the update.
    :type before: :class:`ScheduledEvent`

    :param after: Scheduled event after the update.
    :type after: :class:`ScheduledEvent`


.. function:: on_scheduled_event_delete(event)

    Calls when a scheduled event is deleted, ended or cancelled.

    Requires :attr:`GatewayIntents.scheduled_events` to be enabled.

    :param event: The deleted scheduled event.
    :type event: :class:`ScheduledEvent`

Emojis Events
~~~~~~~~~~~~~~

.. function:: on_emojis_update(before, after)

    Calls when emojis of a guild update i.e either some emojis were added or removed.

    Requires :attr:`GatewayIntents.emojis_and_stickers` to be enabled.

    :param before: The list of emojis before update was applied.
    :type before: List[:class:`Emoji`]

    :param after: The list of emojis after update was applied.
    :type after: List[:class:`Emoji`]

Discord Data Models
-------------------

These classes wrap the Discord complex data models into easy to use object oriented
interface.

These classes are not meant to be initalized by users. You should also never modify the
instance of these classes provided by library as it may cause many issues like cache issues
etc.

Due to the nature of these objects that they are often cached, All objects have defined
``__slots__`` to avoid memory issues so it is impossible to have dynamic attributes on these
classes.

Attachment
~~~~~~~~~~

.. autoclass:: Attachment()
    :members:

CDNAsset
~~~~~~~~

.. autoclass:: CDNAsset()
    :members:

Emoji
~~~~~

.. autoclass:: Emoji()
    :members:

Guild
~~~~~

.. autoclass:: Guild()
    :members:


GuildMember
~~~~~~~~~~~~

.. autoclass:: GuildMember()
    :members:
    :inherited-members:

Message
~~~~~~~

.. autoclass:: Message()
    :members:
    :inherited-members:

Role
~~~~

.. autoclass:: Role()
    :members:

ClientUser
~~~~~~~~~~

.. autoclass:: ClientUser()
    :members:
    :inherited-members:

User
~~~~

.. autoclass:: User()
    :members:
    :inherited-members:

GuildChannel
~~~~~~~~~~~~

.. autoclass:: GuildChannel()
    :members:
    :inherited-members:

TextChannel
~~~~~~~~~~~~

.. autoclass:: TextChannel()
    :members:
    :inherited-members:

VoiceChannel
~~~~~~~~~~~~

.. autoclass:: VoiceChannel()
    :members:
    :inherited-members:

CategoryChannel
~~~~~~~~~~~~~~~~

.. autoclass:: CategoryChannel()
    :members:
    :inherited-members:

DMChannel
~~~~~~~~~

.. autoclass:: DMChannel()
    :members:
    :inherited-members:

StageInstance
~~~~~~~~~~~~~

.. autoclass:: StageInstance()
    :members:

ScheduledEvent
~~~~~~~~~~~~~~~~

.. autoclass:: ScheduledEvent()
    :members:



Dataclasses
-------------

These data classes can be created by users and provide a rich interface for certain tasks
like embeds creation etc.

Color
~~~~~

.. autoclass:: Color()
    :members:

Embed
~~~~~

.. autoclass:: Embed()
    :members:

AllowedMentions
~~~~~~~~~~~~~~~

.. autoclass:: AllowedMentions()
    :members:

File
~~~~

.. autoclass:: File()
    :members:

PermissionOverwrite
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PermissionOverwrite()
    :members:

Flags
-----

These classes wrap the flags management in an easy to use interface.

GatewayIntents
~~~~~~~~~~~~~~~

.. autoclass:: GatewayIntents()
    :members:

SystemChannelFlags
~~~~~~~~~~~~~~~~~~~

.. autoclass:: SystemChannelFlags()
    :members:

UserFlags
~~~~~~~~~

.. autoclass:: UserFlags()
    :members:


MessageFlags
~~~~~~~~~~~~

.. autoclass:: MessageFlags()
    :members:

Permissions
~~~~~~~~~~~

.. autoclass:: Permissions()
    :members: