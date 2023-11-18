import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')



def notification_send_message(message, channel_id):
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is connected to Discord!')
        await send_message(message)

    async def send_message(message):

        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(message)
            print(f'Message sent successfully: {message}')
        else:
            print('Channel not found.')

        await bot.close()

    bot.run(TOKEN)

def notification_upload_message(file_name, channel_id):
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is connected to Discord!')
        await upload(file_name)

    async def upload(message):
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(message, file=discord.File(file_name))
            print(f'File sent successfully: {message}')
        else:
            print('Channel not found.')

        await bot.close()

    bot.run(TOKEN)
