# Spyfall Emailer

## Setup

Use a virtual environment for click:
```
$ python3 -m venv env
$ . env/bin/activate
$ pip install click
```

Modify ```example/config``` to match the email from which you will be sending game details. Note that you will have to disable some security settings for said email. Currently, only gmail emails are supported for administering the game.

## Creating a game

Don't forget to source the virtual environment every time before running ```spyfall.py```. 

Now list all the players' emails in example/players. If run without ```--config``` or ```--emails``` spyfall.py will assume the files are located in the working directory.

Finally run the script. Game details are recorded in ```log.txt```


```
$ . env/bin/activate
$ python3 spyfall.py --config example/config --emails example/players
(or)
$ python3 spyfall.py # uses 'config' and 'players' by default
```

