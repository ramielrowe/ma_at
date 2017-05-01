from ma_at import data
from ma_at import pokemon
from ma_at import steam

POLL = None


def get_function(command):
    return globals().get('cmd_{}'.format(command[1:]))


def list_commands():
    return ['!{}'.format(func_name[4:]) for func_name in globals()
            if func_name.startswith('cmd_')]


async def cmd_help(client, message):
    msg = ('Available commands are: {commands}.'
           .format(commands=', '.join(list_commands())))
    await client.send_message(message.channel, msg)


async def cmd_on_ark(client, message):
    args = message.content.split(' ')[1:]
    if len(args) != 1:
        msg = 'Invalid usage! Command is "!on_ark [steam_user_id]"'
        await client.send_message(message.channel, msg)
    else:
        on_ark, user_id, name = steam.user_on_ark(args[0])
        if on_ark:
            msg = 'Yes, {name} is on our Ark Server.'.format(name=name)
            await client.send_message(message.channel, msg)
        else:
            msg = 'No, {name} is not on our Ark Server.'.format(name=name)
            await client.send_message(message.channel, msg)


async def cmd_track_ark_user(client, message):
    args = message.content.split(' ')[1:]
    if len(args) != 1:
        msg = 'Invalid usage! Command is "!track_arg_user [steam_user_id]"'
        await client.send_message(message.channel, msg)
    else:
        tracked_users = data.get('ark.tracked_users', [])
        if args[0] not in tracked_users:
            tracked_users.append(args[0])
        data.save()
        msg = 'Started tracking user {user}'.format(user=args[0])
        await client.send_message(message.channel, msg)


async def cmd_untrack_ark_user(client, message):
    args = message.content.split(' ')[1:]
    if len(args) != 1:
        msg = 'Invalid usage! Command is "!untrack_arg_user [steam_user_id]"'
        await client.send_message(message.channel, msg)
    else:
        tracked_users = data.get('ark.tracked_users', [])
        if args[0] in tracked_users:
            tracked_users.remove(args[0])
        data.save()
        msg = 'Stopped tracking user {user}'.format(user=args[0])
        await client.send_message(message.channel, msg)


async def cmd_ark_user_alert_on(client, message):
    callout = message.author.mention
    callouts = data.get('ark.user_alert_callouts', [])
    if callout not in callouts:
        callouts.append(callout)
        data.save()
    msg = "Ok, I'll send you Ark user alerts"
    await client.send_message(message.channel, msg)


async def cmd_ark_user_alert_off(client, message):
    callout = message.author.mention
    callouts = data.get('ark.user_alert_callouts', [])
    if callout in callouts:
        callouts.remove(callout)
        data.save()
    msg = "Ok, I won't send you Ark user alerts"
    await client.send_message(message.channel, msg)


async def cmd_ark_user_survey(client, message):
    tracked_users = [steam.user_on_ark(user_id) for user_id in
                     data.get('ark.tracked_users', [])]
    lines = ['{} ({}): {}'.format(name, user_id,
                                  'online' if online else 'offline')
             for (online, user_id, name) in tracked_users]
    msg = '\n'.join(lines)
    await client.send_message(message.channel, msg)


async def cmd_ark_users_online(client, message):
    users = ', '.join(steam.ark_users_online())
    await client.send_message(message.channel, 'Online Users: {}'.format(users))


async def cmd_pokemap(client, message):
    username = message.author.name
    args = message.content.split(' ', 1)
    location = args[1] if len(args) > 1 else None
    await client.send_message(message.channel,
                              pokemon.pokemap(username, location))

async def cmd_pokemap_small(client, message):
    username = message.author.name
    args = message.content.split(' ', 1)
    location = args[1] if len(args) > 1 else None
    await client.send_message(message.channel,
                              pokemon.pokemap(username, location,
                                              steps='4'))


async def cmd_pokemap_beta(client, message):
    username = message.author.name
    args = message.content.split(' ', 1)
    location = args[1] if len(args) > 1 else None
    await client.send_message(message.channel,
                              pokemon.pokemap(username, location,
                                              image='pokemap_beta'))


async def cmd_poll(client, message):
    args = message.content.split(' ', 1)[1].split('|')
    poll = args[0].strip()
    options = [o.strip() for o in args[1:]]

    global POLL
    POLL = {
        'poll': poll,
        'options': {option.lower(): [] for option in options}
    }
    await client.send_message(message.channel,
                              'Created new poll, use !vote to cast your vote.')

async def cmd_vote(client, message):
    username = message.author.name
    args = message.content.split(' ', 1)
    option = args[1].lower().strip()

    if POLL and option in POLL['options']:
        POLL['options'][option].append(username)
        await client.send_message(message.channel, 'Ballot cast.')
    else:
        await client.send_message(message.channel, 'Invalid vote.')


async def cmd_tally(client, message):
    if POLL:
        lines = [POLL['poll']]
        for option, votes in POLL['options'].items():
            lines.append('{}: {} ({})'.format(option,
                                              len(votes), ', '.join(votes)))
        await client.send_message(message.channel, '\n'.join(lines))
    else:
        await client.send_message(message.channel, 'No running poll.')


async def cmd_page(client, message):
    group = message.content.split(' ', 1)[1].lower()
    users = ', '.join(data.get('page_groups.{}'.format(group), []))
    if users:
        await client.send_message(message.channel, 'Paging: {}'.format(users))


async def cmd_pageme(client, message):
    group = message.content.split(' ', 1)[1].lower()
    users = data.get('page_groups.{}'.format(group), [])
    if message.author.name not in users:
        users.append(message.author.mention)
        data.save()


async def cmd_nopage(client, message):
    group = message.content.split(' ', 1)[1].lower()
    users = data.get('page_groups.{}'.format(group), [])
    if message.author.name in users:
        users.remove(message.author.mention)
        data.save()
