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
