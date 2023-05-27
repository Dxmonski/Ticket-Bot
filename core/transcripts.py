import discord
import os
from load_config import load_config
from core.embeds import get_timestamp

data = load_config()

async def get_messages(chnl, user):
    directory = 'assets/ticket-logs'
    os.makedirs(directory, exist_ok=True)

    dr = os.path.join(directory, f'{user}.txt')
    with open(dr, 'w', encoding='utf-8') as file:
        async for message in chnl.history(limit=None):
            file.write(f"{get_timestamp()} -> {user} -> {message.content}\n")
    await user.send(file=discord.File(dr))
