import dhooks
import json

def init():
    global config
    global hook

    config = json.load(open("config.json"))["discord"]
    hook = dhooks.Webhook(config["webhook"])

def send(author:str, msg:str):
    global hook

    message_content = f"<{author}> {msg}"

    hook.send(message_content)