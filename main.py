import discord
import time
import json
import irc

config = json.load(open("config.json"))["discord"]

client = discord.Client()

@client.event
async def on_message(msg):
    author = str(msg.author)
    content = str(msg.content)

    if author.split("#")[-1] != "0000":
        msg_to_irc = f"<{author}> {content}"

        irc.send(msg_to_irc)

client.run(config["token"])