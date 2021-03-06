<img align='right' alt='NeoCord' src='docs/source/images/logo.png'>

# NeoCord
An elegant asynchronous API wrapper around [Discord Bot API](https://discord.dev)

> :warning: **Alpha**: This project is currently alpha!

## :bulb: Features

- Pythonic API interface using asyncio.
- Object Oriented design with no dirty payloads involved.
- Proper handling of HTTPs ratelimits.
- Consistent and actively maintained.
- Performant and highly optimized for all use cases.
- Easy to use and completely beginner friendly.

## :electric_plug: Installation
**NeoCord requires Python 3.8 or higher.**

This library can be installed by the traditional and python's favorite package manager pip.
```sh
pip install -U neocord
```
This would install some extra [dependencies](requirements.txt) that this library depends on.

## :control_knobs: Usage
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

## :thinking: Inspiration from [discord.py](https://github.com/Rapptz/discord.py)
This library started as an inspiration of the amazing Python library, discord.py and that's
why the API might be similar to that of discord.py in many aspects so if you have used
discord.py, you might be familiar with the API design however, there are many notable
differences too.

## :handshake: Contributing
Feel free to suggest features or report bugs using [GitHub Issues](https://github.com/nerdguyahmad/neocord/issues)
or [Create a pull request](https://github.com/nerdguyahmad/neocord/pulls) to directly
contribute to the codebase.

## :link: Links
- [Documentation](https://neocord.readthedocs.io)
- [Discord Developers Portal](https://discord.com/developers/applications)
