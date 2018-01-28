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

    
    timestamp = time.strftime('%l:%M%p %Z on %b %d, %Y')
    roles = locs[chosen_loc]
    if len(player_emails) - 1 > len(roles):
        print("Error: Not enough roles for all players", file=sys.stderr)
        sys.exit(1)

    msgs = {}
    for email in player_emails:
        chosen_idx = random.randrange(len(roles))
        msgs[email] = construct_msg(chosen_loc, roles[chosen_idx], locs, 
                                    timestamp)
        del(roles[chosen_idx])

    for email, msg in msgs.items():
        print(email)
        print(msg)
        print()

    print(chosen_loc)
    print(locs)
    print(loc_cache)

    # Display time in a pretty way. Taken from stackoverflow
    print(timestamp)

    return # FIXME
    
    # choose a random location

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(src_email, src_password)

    msg = "Hello World"
    for email in player_emails:
        server.sendmail(src_email, email, msg)
    server.quit()

def construct_msg(loc, role, locs, timestamp):
    return role

if __name__ == "__main__":
    main()
