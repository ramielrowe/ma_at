import asyncio
import os

from ma_at import data
from ma_at import steam


ARK_ALERTS_CHAN_ID = os.getenv('ARK_ALERTS_CHAN_ID')


async def monitor_arc_users(client):
    await client.wait_until_ready()
    while not client.is_closed:
        ark_alerts = client.get_channel(ARK_ALERTS_CHAN_ID)
        ark_tracked_users = [steam.user_on_ark(user_id)
                             for user_id in data.get('ark.tracked_users', [])]
        new_online_usernames = []
        for online, user_id, name in ark_tracked_users:
            if not online and user_id in data.get('ark.online_users', []):
                data.get('ark.online_users', []).remove(user_id)
            elif online and user_id not in data.get('ark.online_users', []):
                data.get('ark.online_users', []).append(user_id)
                new_online_usernames.append(name)
        data.save()

        if new_online_usernames:
            callouts = data.get('ark.user_alert_callouts', [])
            msg = ('{callout} Ark online user alert for: {users}'
                   .format(callout=' '.join(callouts),
                           users=', '.join(new_online_usernames)))
            await client.send_message(ark_alerts, msg)

        await asyncio.sleep(60)
