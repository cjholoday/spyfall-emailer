import smtplib

with open('config', 'r') as config_file:
    src_email = config_file.readline().rstrip()
    src_password = config_file.readline().rstrip()

with open('players', 'r') as emails_file:
    player_emails = [email.rstrip() for email in emails_file.readlines()]

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(src_email, src_password)

msg = "Hello World"
for email in player_emails:
    server.sendmail(src_email, email, msg)
server.quit()
