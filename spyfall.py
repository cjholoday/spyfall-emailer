import smtplib
import random
import time
import json


import click


@click.command()
@click.option('-c', '--config', type=str,
        help="Specifies the source email's config file. DEFAULT=config")
@click.option('-e', '--emails', type=str,
        help="File that contains players' emails. DEFAULT=players")
def main(emails, config):
    if config is None:
        config = "config"
    if emails is None:
        emails = "players"

    with open(config, 'r') as config_file:
        src_email = config_file.readline().rstrip()
        src_password = config_file.readline().rstrip()

    with open(emails, 'r') as emails_file:
        player_emails = [email.rstrip() for email in emails_file.readlines()]

    # randomize the player order to randomize role assignment
    #
    # Note that shuffling the roles list instead wouldn't
    # fully randomize role assignment: if there are more players than roles,
    # then some players would consistently obtain the same role across
    # games. This is because of the periodic nature of role assignment, which
    # is done with modulo arithmetic
    random.shuffle(player_emails)


    with open('locs.json', 'r') as data_file:
        locs = json.loads(data_file.read())

    loc_cache = []
    try:
        with open('loc_cache.txt', 'r+') as cache_file:
            loc_cache = [loc.rstrip() for loc in cache_file]
    except FileNotFoundError:
        pass # no games have been played recently. Not a problem

    # Blacklist locations that have been recently played with
    for loc in loc_cache:
        del(locs[loc])

    chosen_loc = random.choice(list(locs.keys()))

    # store latest locations so they aren't chosen in the next 5 games
    with open('loc_cache.txt', 'w') as cache_file:
        start = 0
        if len(loc_cache) >= 5:
            start = 1
        for i in range(start, len(loc_cache)):
            cache_file.write(loc_cache[i] + '\n')
        cache_file.write(chosen_loc + '\n')

    
    # Display time in a pretty way. Taken from stackoverflow
    timestamp = time.strftime('%l:%M%p %Z on %b %d, %Y')
    roles = locs[chosen_loc]

    with open('log.txt', 'w') as log:
        log.write('Location: {}\n'.format(chosen_loc))
        log.write('Timestamp: {}\n'.format(timestamp))
        log.write('Roles:\n')

        spy_email = random.choice(player_emails)
        msgs = {}

        role_idx = 0
        for email in player_emails:
            seen_loc = '???'
            role = 'Spy!'
            if email != spy_email:
                role = roles[role_idx % len(roles)]
                role_idx += 1
                seen_loc = chosen_loc
            msgs[email] = construct_msg(seen_loc, role, locs, timestamp)
            log.write(' - {}: {}\n'.format(email, role))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(src_email, src_password)

    for email in player_emails:
        server.sendmail(src_email, email, msgs[email])
    server.quit()

def construct_msg(loc, role, locs, timestamp):
    msg = 'Subject: Spyfall Game Details'
    msg += '\n\n'
    msg += 'Hi! Here are your game details:\n'
    msg += '\n'
    msg += 'Role: {}\n'.format(role)
    msg += 'Location: {}\n'.format(loc)
    msg += 'Timestamp:{}\n'.format(timestamp)
    msg += '\n'
    msg += 'All potential locations:\n'
    msg += '\n'.join([' - ' + l for l in locs]) + '\n'
    return msg

if __name__ == "__main__":
    main()
