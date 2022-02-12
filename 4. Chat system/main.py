from http import client
from msilib.schema import ListBox
import socket
import time
import threading
import os
from tkinter import *


root = Tk()
root.geometry("300x500")
root.config(bg="white")


def func():
    t=threading.Thread(target=recv)
    t.start()

def recv():
    listensocket = socket.socket()
    port = 3050
    maxconnection = 99
    ip = socket.gethostname()
    print(ip)

    listensocket.bind(('', port))
    listensocket.listen(maxconnection)
    (clientsocket, address) = listensocket.accept()

    while True:
        sendermessenger = clientsocket.recv(1024).decode()
        if not sendermessenger == "":
            time.sleep(5)
            lstbx.insert(0, "Client : " + sendermessenger)

s = 0
def sendmsg():
    global s
    if s==0:
        s= socket.socket()
        hostname='MinhDuy'
        port=4050
        s.connect(hostname, port)

        msg = messengerbox.get()
        lstbx.insert(0,"You : " + msg)
        s.send(msg.encode())

    else:
        msg = messengerbox.get()
        lstbx.insert(0,"You : " + msg)
        s.send(msg.encode())


def threadsendmsg():
    th = threading.Thread(target=sendmsg)
    th.start()


startchatimage = PhotoImage(file='start.png')

buttons = Button(root, image=startchatimage, command=func, borderwidth=0)
buttons.place(x=55, y=1)

messenger = StringVar()
messengerbox = Entry(root, textvariable=messenger, font=(
    'calibre', 10, 'normal'), border=2, width=32)
messengerbox.place(x=10, y=444)

sendmessengerimg = PhotoImage(file='send.png')

sendmessengerbutton = Button(root, image=sendmessengerimg, command=threadsendmsg, borderwidth=0)
sendmessengerbutton.place(x=260, y=440)

lstbx = Listbox(root, height=20, width=43)
lstbx.place(x=15, y=80)

root.mainloop()
