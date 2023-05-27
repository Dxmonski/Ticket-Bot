import discord
import json
from discord.ext import commands, tasks
from datetime import datetime
from load_config import load_config
from core.close import CloseButton
from core.add_user import AddUser
from core.payments import PaymentButtons
from core.utils import Utilies

bot = commands.Bot(command_prefix="/", case_insensitive=True,intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    bot.add_view(OpenButton())
    bot.add_view(CustomView())
    uhidk.start()
    print(f"{bot.user} OK.")
    
data = load_config()

@tasks.loop(minutes=2)
async def uhidk():
    guild = bot.get_guild(int(data.guild))
    z = discord.utils.get(guild.categories, id=int(data.category_1))
    r = discord.utils.get(guild.categories, id=int(data.category_2))
    x = discord.utils.get(guild.categories, id=int(data.category_3))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Watching {len(z.channels) + len(r.channels) + len(x.channels)} tickets!'))

def load_tickets():
    try:
        with open("assets/tickets.json", "r") as f:
            tickets = json.load(f)
    except FileNotFoundError:
        tickets = []
    return tickets

async def save_tickets(ticket_ids):
    with open("assets/tickets.json", "w") as file:
        json.dump(ticket_ids, file, indent=4)

@bot.slash_command()
async def panel(ctx):
    embed = discord.Embed(
        title='',
        description=f"{data.ticket_em} |  **__ZRX Tickets__**\n\n__**How to open a ticket**__\n\n> There's a button assigned to this embed, once you press on it you will be forwarded a selectoption, where you can choose what you are opening a ticket for. Once you choose your option, it will make a new ticket for you, there you can chat and place your order.\n\n__**Format**__\n\n> When you open a ticket please give us detailed information about what you want to order. For example: `1x Sniper Key - payment: LTC`",
        color=15134443,
        timestamp=datetime.now()
    )
    utils = Utilies(bot)
    view = OpenButton()
    msg = await ctx.send(embed=embed, view=view)
    await ctx.respond('Successfully sent panel!', ephemeral=True)
    await utils.save_ids(msg.id, ctx.channel.id)

class OpenButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Open Ticket', style=discord.ButtonStyle.success, custom_id='open-button')
    async def button_callback(self, button, interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(title='', description='Please Pick your option down below in the select menu.')
        embed.set_image(url=data.thumb)
        embed.set_footer(text=data.footer)
        await interaction.followup.send(embed=embed,view=SendQuestion(), ephemeral=True)
    
class CustomView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AddUser(bot))
        self.add_item(PaymentButtons(bot))
        self.add_item(CloseButton(bot))
        
class SendQuestion(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, interaction, value, category_id):
        await interaction.response.defer(ephemeral=True)
        db = load_tickets()
        response = discord.Embed(title='', description=f'{data.load_em} | Please wait while we process your ticket.')
        msg = await interaction.followup.send(embed=response, ephemeral=True)
        if any(ticket.get('author') == interaction.user.id for ticket in db.values()):
            response.description = f'{data.failed_em} | You already have an open ticket.'
            await msg.edit(embed=response)
            return

        guild = interaction.guild
        category = guild.get_channel(int(category_id))
        owner = guild.get_role(int(data.owner))
        blocked_role = guild.get_role(int(data.bl_roles))
        index = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            owner: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            blocked_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, mention_everyone=False)
        }

        chnl = await guild.create_text_channel(f'{value.lower()}-{interaction.user.name}', category=category, overwrites=index)
        await chnl.send(f'{owner.mention}')
        embed = discord.Embed(
            title='ZRX Services',
            description=f'{data.ticket_em} | You have opened a ticket to buy or ask a question. Please feel free to leave your message here staff will be here shortly.',
            color=172214,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=data.thumb)
        view = CustomView()
        await chnl.send(embed=embed, view=view)

        response.description = f'{data.suc_em} | Successfully made your ticket.\n\n> {chnl.mention}'
        await msg.edit(embed=response)

        ticket = {
            'channel_id': chnl.id,
            'author': interaction.user.id
        }
        tickets = load_tickets()
        tickets[str(chnl.id)] = ticket
        await save_tickets(tickets)

    @discord.ui.select(
        placeholder='Choose your ticket option.',
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=f'{data.opt1_name}',
                description=f'{data.opt1_desc}',
                emoji=f'{data.opt1_emj}'
            ),
            discord.SelectOption(
                label=f'{data.opt2_name}',
                description=f'{data.opt2_desc}',
                emoji=f'{data.opt2_emj}'
            ),
            discord.SelectOption(
                label=f'{data.opt3_name}',
                description=f'{data.opt3_desc}',
                emoji=f'{data.opt3_emj}'
            )
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == f"{data.opt1_name}":
            await self.create_ticket(interaction, select.values[0], data.category_1)
        elif select.values[0] == f"{data.opt2_name}":
            await self.create_ticket(interaction, select.values[0], data.category_2)
        elif select.values[0] == f"{data.opt3_name}":
            await self.create_ticket(interaction, select.values[0], data.category_3)
        
            
bot.run(data.bot_token)
