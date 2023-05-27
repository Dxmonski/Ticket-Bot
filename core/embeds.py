import discord
import datetime
from load_config import load_config

data = load_config()

def get_timestamp():
    timestamp = f"{datetime.datetime.now().strftime('%H:%M:%S')}"
    return timestamp

def embed_closed(user, chnl, interaction_id):
    embed = discord.Embed(
        title='Ticket Closed',
        description=f'Ticket was closed at: `{get_timestamp()}`',
        color=discord.Colour.red()
    )
    embed.add_field(name='Author', value=f'<@{user}>', inline=False)
    embed.add_field(name='Channel', value=f'`{chnl}`', inline=False)
    embed.add_field(name='Closed By', value=f"<@{interaction_id}>", inline=False)
    embed.set_footer(text=data.footer)
    return embed

def user_added(user, interactor, chnl):
    embed = discord.Embed(
        title='User Added',
        description=f'New user was added to an ticket at `{get_timestamp()}`',
        color=discord.Colour.green()
    )
    embed.add_field(name='Added By', value=f'<@{interactor}>', inline=False)
    embed.add_field(name='Channel', value=f'<#{chnl}> `({chnl})`', inline=False)
    embed.add_field(name='Added User', value=f'<@{user}>')
    embed.set_footer(text=data.footer)
    return embed

def payments_embed():
    embed = discord.Embed(
        title='Payment methods',
        description='Down below is a list of our payment addresses.',
        color=15000295
    )
    embed.add_field(name='LTC', value=data.ltc, inline=False)
    embed.add_field(name='BTC', value=data.btc, inline=False)
    embed.add_field(name='ETH', value=data.eth, inline=False)
    embed.add_field(name='SOL', value=data.sol, inline=False)
    embed.set_footer(text=data.footer)
    return embed
