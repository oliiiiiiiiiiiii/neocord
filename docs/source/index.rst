.. NeoCord documentation master file, created by
   sphinx-quickstart on Sun Nov 21 19:46:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NeoCord's documentation!
===================================

NeoCord is a performant, asynchronous and easy to use API wrapper around Discord Bot API.

Features
~~~~~~~~

- Pythonic API interface using asyncio.
- Object Oriented design with no dirty payloads involved.
- Consistent & Actively maintained.
- Performant and highly optimized.

Basic Usage
~~~~~~~~~~~

Example::

   import neocord

   client = neocord.Client()

   # Register a READY event listener that fires whenever
   # the bot gets ready initally. "once" sets the event to call only once.
   @client.on('ready', once=True)
   async def on_ready():
   print(f'{client.user} is ready.')

   # Listen to messages...
   @client.on('message')
   async def on_message(message):
   if message.author.bot:
      # Don't respond to bots (or ourselves).
      return

   if message.content.lower() == '!ping':
      # command used, let's send a response!
      await message.channel.send('Pong from NeoCord!')

   # run the bot.
   client.run('bot-token')

Explore
~~~~~~~

You can explore the possibilites of this library in this documentation and following
pages dive into each and every aspect of what this library is capable of.

.. toctree::
   :maxdepth: 1

   api
