<div align="center">
  <h1>NeoCord</h1>
  <sup><strong>This project is in alpha stage!</strong></sup>
  <hr>
  <p>An asynchronous API wrapper around Discord API written in Python.</p>
</div>

## Features

- Pythonic API interface using asyncio.
- Object Oriented design with no dirty payloads involved.
- Consistent & Actively maintained.

## Usage
```py
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
```
There are a lot more features that are up to you to discover. Feel
free to explore the library's [documentation](https://neocord.rtfd.io) and
discover the possibilites.


## Inspiration from discord.py
This library started as an inspiration of the amazing Python library, discord.py and that's
why the API might be similar to that of discord.py in many ways to discord.py.

## Acknowledgments
This library is still in alpha stage and is currently actively developed. While we try
our best to avoid making breaking changes, some versions might bring some breaking changes for compatibility or consistencies purposes.

## Contributing
Feel free to suggest features or report bugs using [GitHub Issues](https://github.com/nerdguyahmad/neocord/issues)
or [Create a pull request](https://github.com/nerdguyahmad/neocord/pulls) to directly
contribute to the codebase.