import discord
import time
import json
from core.embeds import embed_closed
from load_config import load_config
from core.utils import Utilies
from core.transcripts import get_messages

class CloseButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label='Close', style=discord.ButtonStyle.red, custom_id='close-button')
        self.bot = bot
        self.utils = Utilies(bot)
    
    async def callback(self, interaction: discord.Interaction):
        data = load_config()
        await interaction.response.send_message('Deleting ticket in 3 secs..')
        time.sleep(3)
        chnl = interaction.channel
        
        user_id = await self.utils.user_to_id(chnl.id)
        user = interaction.guild.get_member(user_id)
        await get_messages(chnl, user)
        await chnl.delete()
        
        with open("assets/tickets.json", "r") as file:
            data = json.load(file)
        
        channel_id = str(chnl.id)
        if channel_id in data:
            del data[channel_id]
            with open("assets/tickets.json", "w") as file:
                json.dump(data, file, indent=4)
        
        embed = discord.Embed(title='', description=f'Your ticket has been closed. If you need our services in the future, feel free to open a new ticket.\n\n> **Closed by:** {interaction.user.mention}', color=discord.Colour.og_blurple())
        await user.send(embed=embed)
        logs_channel = self.bot.get_channel(int(1106691208899731476))
        closed = embed_closed(user_id, chnl.id, interaction.user.id)
        await logs_channel.send(embed=closed)
