import json
import irc

config = json.load(open("config.json"))["irc"]

conn = irc.IRCClient(config)
conn.connect()
conn.join("#main")
conn.send(False, "#main", "hello")