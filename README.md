<div align="center">
  <h1>NeoCord</h1>
  <sup><strong>This project is work in progress not for production use.</strong></sup>
  <hr>
  <p>An asynchronous API wrapper around Discord API written in Python.</p>
</div>

## Inspiration
This library is a side project of [mine](https://github.com/nerdguyahmad) which I started as an inspiration of [discord.py by Rapptz](https://github.com/Rapptz/discord.py), The aim of this library is to provide a simple interface to interact with Discord API by abstracting away most of the complications. 

## Features
- Modern API interface using async/await syntax.
- Consistent, Object Oriented Design — No dirty payloads.
- Fully optimized and performant.

## Usage
**This is currently a concept.**
```py
import neocord

client = neocord.Client(token='bot-token')

@client.on('ready')
async def on_ready():
  print(f'{client.user} is ready.')

@client.on('message')
async def on_message(message):
  if message.author.bot:
    return
  
  if message.content == '!ping':
    await message.channel.send('PONG!')

client.run()
```
