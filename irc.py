import threading
import sender
import socket
import time
import json

# TODO
# sending messages to discord
# discord bridge(module like this)


def join(channel):
    global irc

    irc.send(f"JOIN {channel}\r\n".encode())

def send(msg):
    global channel
    global irc

    irc.send(f"PRIVMSG {channel} {msg}\r\n".encode())

def extract_msg(resp):
    global channel

    resp = resp.split("PRIVMSG")

    #getting author
    author_section = resp[0]
    unprocessed_author = author_section.replace(":", "")

    author = unprocessed_author.split("!")[0]

    #getting message
    msg_section = resp[1]

    msg = msg_section.replace(f"{channel} :", "")

    return author, msg

def ping(host):
    global irc

    content = f"PING :{host}\r\n"

    irc.send(content.encode())

def listen_for_packages(conn:socket.socket, host:str):
    while True:
        resp = irc.recv(2048).decode()

        if "PRIVMSG" in resp:
            author, msg = extract_msg(resp)
            sender.send(author, msg)

        elif "PING" in resp:
            resp_packet = f"PONG :{host} {host}\r\n"

            irc.send(resp_packet.encode())


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

print("[*] Initializing discord sender")
sender.init()

print(f"[*] Joining channel {channel}")
irc.send(f"JOIN {channel}\r\n".encode())

time.sleep(2.5)

print("[*] Starting packet handler thread")
packet_thread = threading.Thread(target=listen_for_packages, args=(irc, config["server"]["host"]))
packet_thread.start()

print("[*] All threads are running")