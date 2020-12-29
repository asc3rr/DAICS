import socket
import time

# not working

class IRCClient:
    irc_sock = None # socket object

    # client info
    name = ""
    nick = ""

    # server info
    host = ""
    port = 0

    def __init__(self, config:dict):
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]

        self.name = config["bot"]["name"]
        self.nick = config["bot"]["nick"]

    def connect(self):
        # preparing headers
        some_header = "CAP LS\r\n" # dont know what is this doing
        nick_header = f"NICK {self.nick}\r\n"
        user_header = f"USER {self.nick} {self.nick} 127.0.0.1 :{self.name}\r\n"

        # setting socket
        self.irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_sock.connect((self.host, self.port))

        self.irc_sock.send(some_header.encode())
        self.irc_sock.send(nick_header.encode())
        self.irc_sock.send(user_header.encode())

        time.sleep(15)

        print(self.irc_sock.recv(8192))

        self.ping()

    def ping(self):
        self.irc_sock.send(f"PING {self.host}\r\n'".encode())
        print(self.irc_sock.recv(2048))

    def join(self, channel:str):
        command = f"JOIN {channel}\r\n"
        print(command)

        s.send("JOIN #main\r\n".encode())

        self.irc_sock.send(command.encode())
        print(self.irc_sock.recv(2048))

    def send(self, is_user:bool, receiver:str, msg:str):
        processed_reciever = "#"

        if not "#" in receiver and not is_user:
            processed_reciever += receiver

        else:
            processed_reciever = receiver

        self.irc_sock.send(f"PRIVMSG {processed_reciever} {msg}\r\n".encode())
        print(self.irc_sock.recv(2048))