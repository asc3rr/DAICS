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

def ping_loop(conn:socket.socket, host:str):
    while True:
        packet = f"PING :{host}\r\n"
        irc.send(packet.encode())
        data = irc.recv(1024).decode()
        
        time.sleep(30)

def listen_for_messages(conn:socket.socket):
    while True:
        response = irc.recv(2048).decode()

        if "PRIVMSG" in response:
            author, msg = extract_msg(response)

            sender.send(author, msg)

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

print("[*] Starting connection keeper thread")
ping_thread = threading.Thread(target=ping_loop, args=(irc, config["server"]["host"]))
ping_thread.start()

print(f"[*] Joining channel {channel}")
irc.send(f"JOIN {channel}\r\n".encode())

print(f"[*] Listening for messages")
message_thread = threading.Thread(target=listen_for_messages, args=(irc,))
message_thread.start()

print("[*] All threads are running")