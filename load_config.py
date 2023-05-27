import json

def load_config():
    with open("assets/config.json") as f:
        data = json.load(f)
        
    class load_config():
        bot_token = data['bot']['token']
        owner = data['bot']['owner_role_id']
        guild = data['bot']['guild_id']
        category_1 = data['categories']['category_id-1']
        category_2 = data['categories']['category_id-2']
        category_3 = data['categories']['category_id-3']
        thumb = data['embed']['embed_thumnail_url']
        footer = data['embed']['embed_footer']
        logs_channel = data['categories']['logs_channel']
        owner_ids = data['owners']['owner_ids']
        bl_roles = data['categories']['blocked_role']
        ltc = data['payments']['ltc']
        btc = data['payments']['btc']
        eth = data['payments']['eth']
        sol = data['payments']['sol']
        message_id = data['categories']['message_id']
        channel_id = data['categories']['channel_id']
        load_em = data['embed']['loading_response_emoji']
        suc_em = data['embed']['success_response_emoji']
        ticket_em = data['embed']['ticket-embed_emoji']
        failed_em = data['embed']['failed_response_emoji']
        opt1_name = data['select_menu']['option-1_name']
        opt2_name = data['select_menu']['option-2_name']
        opt3_name = data['select_menu']['option-3_name']
        opt1_desc = data['select_menu']['option-1_description']
        opt2_desc = data['select_menu']['option-2_description']
        opt3_desc = data['select_menu']['option-3_description']
        opt1_emj = data['select_menu']['option-1_emoji']
        opt2_emj = data['select_menu']['option-2_emoji']
        opt3_emj = data['select_menu']['option-3_emoji']
        
    return load_config()

data = load_config()
