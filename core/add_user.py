import discord
from discord.ui import InputText, Modal
from load_config import load_config
from core.embeds import user_added
from core.utils import Utilies

class AskModal(Modal):
    def __init__(self, bot):
        super().__init__(title="User Input", timeout=None)
        self.add_item(InputText(label="User-id", placeholder="Put the user's ID here.."))
        self.bot = bot
        self.utils = Utilies(bot)
        
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = load_config()
        if not await self.utils.id_check(interaction):
            await interaction.followup.send('You are not allowed to add someone.')
            return
        chnl = interaction.channel
        user_id = int(self.children[0].value)
        user = interaction.guild.get_member(user_id)
        
        if user is None:
            print(f"User with ID {user_id} not found.")
            return
        
        overwrites = chnl.overwrites
        guild = interaction.guild 
        blocked_roles = guild.get_role(int(data.bl_roles))

        overwrites[user] = discord.PermissionOverwrite(read_messages=True, send_messages=True, mention_everyone=False)
        overwrites[blocked_roles] = discord.PermissionOverwrite(read_messages=False)
        overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
        
        await chnl.edit(overwrites=overwrites)
        await interaction.followup.send(f"Successfully added user: {user.mention}")
        chnl = self.bot.get_channel(int(data.logs_channel))
        embed = user_added(user_id, interaction.user.id, chnl.id)
        await chnl.send(embed=embed)
                
class AddUser(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label='Add User', style=discord.ButtonStyle.success, custom_id='add-button')
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        bot = self.bot
        await interaction.response.send_modal(AskModal(bot))
