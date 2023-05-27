import discord
import json
from load_config import load_config

class Utilies():
    def __init__(self, bot):
        self.bot = bot
    
    async def id_check(self, interaction:discord.Interaction):
        data = load_config()
        if str(interaction.user.id) not in data.owner_ids:
            return False
        else:
            return True
        
    async def save_ids(self, msg_id, chnl_id):
        with open("assets/config.json", "r") as f:
            data = json.load(f)

        data["categories"]["channel_id"] = str(chnl_id)
        data["categories"]["message_id"] = str(msg_id)

        with open("assets/config.json", "w") as f:
            json.dump(data, f, indent=4)
            
    async def user_to_id(self, chnl):
        with open('assets/tickets.json', 'r') as f:
            data = json.load(f)
    
        for value in data.values():
            if value.get('channel_id') == chnl:
                user = value.get('author')
                return user

        return None
