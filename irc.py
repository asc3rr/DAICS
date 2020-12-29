import threading
import socket
import time
import json

def join(channel):
    global irc

    irc.send(f"JOIN {channel}\r\n".encode())

def send(channel, msg):
    global irc

    irc.send(f"PRIVMSG {channel} {msg}\r\n".encode())

def get_response(channel):
    global irc

    resp = irc.recv(2048).decode()

    if "PRIVMSG" in resp:
        msg_section = resp.split("PRIVMSG")[1]

        msg = msg_section.replace(channel + " :", "")

        return msg

    else:
        return None

def ping(host):
    global irc

    content = f"PING :{host}\r\n"

    irc.send(content.encode())

def ping_loop(conn:socket.socket, host:str):
    while True:
        packet = f"PING :{host}\r\n"
        irc.send(packet.encode())
        data = irc.recv(1024)

        time.sleep(30)

config = json.load(open("config.json"))["irc"]

server_data = (config["server"]["host"], config["server"]["port"])

nick = config["bot"]["nick"]
name = config["bot"]["name"]
channel = config["bot"]["channel"]

irc = socket.socket()
irc.connect(server_data)

print("[*] Sending headers")
irc.send("CAP LS\r\n".encode())
irc.send(f"NICK {nick}\r\n".encode())
irc.send(f"USER {nick} {nick} 127.0.0.1 :{name}\r\n".encode())
print("[*] Headers sent, waiting 15 secs")

time.sleep(15)

# connecting and sending "hello"
# change to listening for messages and sending them to discord

print("[*] Starting connection keeper thread")
ping_thread = threading.Thread(target=ping_loop, args=(irc, config["server"]["host"]))
ping_thread.start()

print(f"[*] Joining channel {channel}")
irc.send(f"JOIN {channel}\r\n".encode())

print(f"[*] Starting listening for messages")

while True:
    response = get_response(channel)

    if response:
        ## sending message to discord
        print(response)