import socket
import time

# working

s = socket.socket()
s.connect(("127.0.0.1", 6667))

s.send("CAP LS\r\n".encode())
s.send("NICK asc3rr\r\n".encode())
s.send("USER asc3rr asc3rr 127.0.0.1 :Borys\r\n".encode())

time.sleep(15)
print(s.recv(4096).decode())

s.send("JOIN #main\r\n".encode())
print(s.recv(4096).decode())
s.send("PRIVMSG #main hello\r\n".encode())
print(s.recv(4096).decode())