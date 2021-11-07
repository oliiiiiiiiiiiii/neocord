<div align="center">
  <h1>NeoCord</h1>
  <sup><strong>This project is work in progress not for production use.</strong></sup>
  <hr>
  <p>An asynchronous API wrapper around Discord API written in Python.</p>
</div>

## Features
- Modern API interface using async/await syntax.
- Consistent, Object Oriented Design — No dirty payloads.
- Fully optimized and performant.
- Properly typehinted interface

## Usage
**This is currently a concept.**
```py
import neocord

client = neocord.Client()

@client.on('ready')
async def on_ready():
  print(f'{client.user} is ready.')

@client.on('message')
async def on_message(message):
  if message.author.bot:
    return

  if message.content == '!ping':
    await message.channel.send('PONG!')

client.run('bot-token')
```
