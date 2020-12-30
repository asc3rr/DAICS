# DAICS
Discord And IRC Channel Synchronization.

## Setup
First, clone the repository with: `git clone https://github.com/asc3rr/DAICS`

Then copy `config.json.example` to `config.json` by executing this: 
```sh
cp config.json.example config.json
```

## Configuration
After setup, you have to configure this program.

There is description of configuration example
```json
{
    "irc":{
        "server":{
            "host":"<address>", # irc server address
            "port":0 # irc server port
        },
        "bot":{
            "name":"<bot name>", # irc bot name
            "nick":"<bot nick>", # irc bot nick
            "channel":"<channel>" # irc channel to synchronize with discord
        }
    },
    "discord":{
        "webhook":"<webhook_url>", # discord webhook
        "token":"<bot_token>" # discord bot token
    }
}
```

## NOTICE
Bot supports only **one** discord channel and **one** IRC channel