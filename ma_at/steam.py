import os

import requests

STEAM_TOKEN = os.getenv('STEAM_TOKEN')
STEAM_USER_URL = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={{user_id}}'.format(STEAM_TOKEN)
ARK_GAME_ID = '346110'
ARK_SERVER_ID = os.getenv('ARK_SERVER_ID')


def user_on_ark(steam_user_id):
    url = STEAM_USER_URL.format(user_id=steam_user_id)
    resp = requests.get(url)
    if resp.status_code == 200:
        body = resp.json()
        if body['response']['players']:
            player = body['response']['players'][0]
            game_id = player.get('gameid')
            server_id = player.get('gameserversteamid')
            return ((game_id == ARK_GAME_ID and server_id == ARK_SERVER_ID),
                    steam_user_id,
                    player.get('personaname'))
    return False, steam_user_id, None
