import discord
from load_config import load_config
from core.embeds import payments_embed


class PaymentButtons(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(label='Payments', style=discord.ButtonStyle.success, custom_id='payment-button')
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        embed = payments_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)
