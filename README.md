# SMTP-discord-relay
Routes SMTP messages to discord webhook

## Use
First you need a Discord webhook url
go to your server or any server you have administrator, edit the chanel where you want the messages to cum, Integrations > New Webhook > Copy Webhook URL
now edit the `./server.py` and set url varble to the discord web hook url

```
$ python -m venv ./venv/
# ./venv/bin/python ./server.py
```
