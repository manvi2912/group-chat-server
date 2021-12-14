from tkinter import *
from tkinter.scrolledtext import ScrolledText as st
import socket
import select
import threading

HEADER_LENGTH=30
def connection_requests():
    while True:
        client_socket, client_address = server_socket.accept()
        user = client_socket.recv(1024)
        if user is False:
            continue
                
        sockets_list.append(client_socket) 
        clients[client_socket] = user.decode()
        print (f"accepted new connection from { client_address[0]}: {client_address[1]} username : {user.decode('utf-8')}")
        t = threading.Thread(target=receive_message, args=(client_socket,))
        t.start()

def update_chat(msg, user, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state==0:
        chatlog.insert(END, '           YOU: ' + msg, 'you')
    else:
        chatlog.insert(END, user + ': ' + msg)
    chatlog.config(state=DISABLED)
    # show the latest messages
    chatlog.yview(END)

def send():
    global textbox
    msg = textbox.get("1.0", END)
    if msg!="" and msg!="\n":
        update_chat(msg, "server", 0)
    textbox.delete("1.0", END)
    if msg:
        for client in clients:
            user="server"
            user_length = f"{len(user):<{HEADER_LENGTH}}".encode()
            client.send(user_length+user.encode()+msg.encode())

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            user = clients[client_socket]
            if not message:
                sockets_list.remove(client_socket)
                del clients[client_socket]
            else:
                if message.decode() != "" and message.decode()!="\n":
                    update_chat(message.decode(), user, 1)
                    for client in clients:
                        if client !=client_socket:
                            user_length = f"{len(user):<{HEADER_LENGTH}}".encode()
                            client.send(user_length+user.encode()+message)
                            
        except:
            sockets_list.remove(client_socket)
            del clients[client_socket]

def GUI():
    global chatlog
    global textbox
    gui = Tk()
    gui.title("Group Chat Server")
    gui.geometry("500x600")
    chatlog = st(gui, bg="white", font=("Times", 15),)
    chatlog.config(spacing1=10) 
    chatlog.config(spacing2=10)
    chatlog.config(spacing3=10) 
    chatlog.config(state=DISABLED)
    chatlog.tag_config('you', background="light green", justify="right",)
    sendbutton = Button(gui, bg='orange', fg='red', text='SEND', command=send)
    textbox = Text(gui, bg='white', font=("Times", 15))
    chatlog.place(x=10, y=10, height=550, width=480)
    textbox.place(x=10, y=565, height=30, width=415)
    sendbutton.place(x=430, y=565, height=30, width=60)
   # _thread.start_new_thread(receive_message, ())
    gui.mainloop()

if __name__ == '__main__':
    chatlog = textbox = None
    th = threading.Thread(target=GUI)
    th.start()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host =  socket.gethostbyname(socket.gethostname())
    port = 5050
    server_socket.bind((host, port))
    print(host)
    server_socket.listen()
    sockets_list = [server_socket]
    clients = {}
    connection_requests()
			    

			     
				        