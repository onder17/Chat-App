"""IMS-Internet Message Structure-Chat Programming"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def gelen_mesaj():
    """Function of perceptioning message"""
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            mesaj_listesi.insert(tkinter.END, msg)
        except OSError:
            break # İf the user exit from the chat

def gonder(event=None):
    """Function of sending message"""
    msg = mesajim.get()
    mesajim.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{exit}":
        client_socket.close()
        app.quit()

def cikis_durumu(event=None):
    """Control function of exit case"""
    mesajim.set("{exit}")
    gonder()



app = tkinter.Tk()
app.title("CHAT APP")

mesaj_alani = tkinter.Frame(app)
mesajim = tkinter.StringVar()
mesajim.set("Enter your message:")  ## Message of the sending field
scrollbar = tkinter.Scrollbar(mesaj_alani)
mesaj_listesi = tkinter.Listbox(mesaj_alani, height=45, width=120,
                                yscrollcommand=scrollbar.set) ## The dimensions of chat space
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
mesaj_listesi.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesaj_listesi.see("end")
mesaj_listesi.pack()
mesaj_alani.pack()

giris_alani = tkinter.Entry(app, textvariable=mesajim)
giris_alani.bind("<Return>", gonder) ##For sending message with enter button
giris_alani.pack()
gonder_buton = tkinter.Button(app, text="Send!", command=gonder) ## Message of the sending button
gonder_buton.pack()

app.protocol("WM_DELETE_WINDOW", cikis_durumu)

HOST = '127.0.0.1' ## same with server.py host info
PORT = 19055 #input("Server Port (OTO:19055): ") ## same with server.py port info



if not PORT:
    PORT = 19055
else:
    PORT = int(PORT)

BUFFERSIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=gelen_mesaj)
receive_thread.start()
tkinter.mainloop()