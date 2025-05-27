#Chat Programming-IMS
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 19055
BUFFERSIZE = 1024  ##determining a packet size
ADDR = (HOST, PORT) ##HOST have ip,port like a door for streaming
SERVER = socket(AF_INET, SOCK_STREAM) ##AF_INET for ip address, for streaming-->SOCK_STREAM
SERVER.bind(ADDR)

def coming_message():
    """Control function of coming messages."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s connected." % client_address)
        client.send(bytes("Chat Application" +
                          "------>Please enter your username: ", "utf8")) ##utf8-->A type of Unicode character coding
        addresses[client] = client_address
        Thread(target=connect_client, args=(client,)).start()

def connect_client(client):
    """Supply the client connection"""
    name = client.recv(BUFFERSIZE).decode("utf8")
    welcome = 'Welcome %s! For exiting type {exit}!' %name
    client.send(bytes(welcome, "utf8"))
    msg = "%s connected the chat!" %name
    stream(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFFERSIZE)
        if msg != bytes("{exit}", "utf8"):
            stream(msg, name+": ")
        else:
            client.send(bytes("{exit}", "utf8"))
            client.close()
            del clients[client]
            stream(bytes("%s exited from the chat." %name, "utf8"))
            break

def stream(msg, prefix=""):
    """Function of streaming message"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(10) # Maximum 10 clients
    print("Connection is waiting...")
    ACCEPT_THREAD = Thread(target=coming_message())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()