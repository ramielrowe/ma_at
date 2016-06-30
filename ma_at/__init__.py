import os

import discord

from ma_at import commands
from ma_at import data
from ma_at import tasks

DATA_FILE = os.getenv('DATA_FILE', 'ma_at.json')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

CLIENT = discord.Client()


@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('------')


@CLIENT.event
async def on_message(message):
    if message.content.startswith('!'):
        args = message.content.split(' ')
        cmd_func = commands.get_function(args[0])
        if cmd_func:
            await cmd_func(CLIENT, message)


def main():
    CLIENT.loop.create_task(tasks.monitor_arc_users(CLIENT))
    CLIENT.run(DISCORD_TOKEN)
