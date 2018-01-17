import smtplib
import click

@click.command()
@click.option('-c', '--config', type=str,
        help="Specifies the source email's config file. DEFAULT=config")
@click.argument('emails_filename', type=str, nargs=1)
@click.argument('session_name', type=str, nargs=1)
def main(emails_filename, session_name, config):
    if config is None:
        config = "config"

    with open(config, 'r') as config_file:
        src_email = config_file.readline().rstrip()
        src_password = config_file.readline().rstrip()

    with open(emails_filename, 'r') as emails_file:
        player_emails = [email.rstrip() for email in emails_file.readlines()]

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(src_email, src_password)

    msg = "Hello World"
    for email in player_emails:
        server.sendmail(src_email, email, msg)
    server.quit()

if __name__ == "__main__":
    main()
