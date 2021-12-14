from tkinter import *
import socket
from tkinter.scrolledtext import ScrolledText as st
import select
import threading
HEADER_LENGTH=30
def initialize_client():
    login = Tk()
    login.geometry("440x200")
    labelText=StringVar()
    labelText.set("Enter your username")
    labelDir=Label(login, textvariable=labelText, height=4, font=("Arial", 25))
    labelDir.place(x=20, y=20, height=30)
    user = Entry(login, font=("Roman", 25))
    user.place(x=20, y=70, height=50, width=400)
    def save():
        global username
        username = user.get()
        if username:
            print(username)
            login.destroy()
    savebutton = Button(login, bg='orange', fg='red', text='SAVE', command=save)
    
    savebutton.place(x=20, y=140, width=400)
    login.mainloop()
    #username=input("enter your user name:")
    if username:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        port = 5050
        print(host)
        client_socket.connect((host, port))
        client_socket.send(username.encode())
        return client_socket

def update_chat(msg, user, state):
    global chatlog

    chatlog.config(state=NORMAL)
    if state==0:
        chatlog.insert(END, 'YOU: ' + msg, "you")
    else:
        chatlog.insert(END, user + ': ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)

def send():
    global textbox
    msg = textbox.get("1.0", END)
    if msg!="" and msg!="\n":
        update_chat(msg, username, 0)
    client_socket.send(msg.encode())
    textbox.delete("1.0", END)

def recieve_message(username, message):
	try:
         if message.decode() != "" and message.decode()!="\n":
             update_chat(msg=message.decode(), user=username.decode(), state=1)
             if not message:
                 return False
             else:
                 return message
	except:
         return False 

def GUI():
    global chatlog
    global textbox
    global flag
    flag=0
    gui = Tk()
    gui.title("Group Chat Server")
    gui.geometry("500x650")
    welcome = Label(gui, text="Welcome "+username, bg="orange", font=("Times",25), padx=5, pady=5).pack(padx=5, pady=5)
    chatlog = st(gui, bg="white", font=("Times", 15))
    chatlog.tag_config('you', background="light green", justify="right", )
    chatlog.config(spacing1=10) 
    chatlog.config(spacing2=10)
    chatlog.config(spacing3=10) 
    chatlog.config(state=DISABLED)
    sendbutton = Button(gui, bg='orange', fg='red', text='SEND', command=send)
    textbox = Text(gui, bg='white', font=("Times", 15))
    chatlog.place(x=10, y=55, height=550, width=480)
    textbox.place(x=10, y=610, height=30, width=415)
    sendbutton.place(x=430, y=610, height=30, width=60)
   # _thread.start_new_thread(receive_message, ())
    gui.mainloop()
    flag=1

if __name__ == '__main__':
    chatlog = textbox = None
    client_socket = initialize_client()
    th = threading.Thread(target=GUI)
    th.start()
    try:
        while True:
            if flag==1:
                break
            user_length  = client_socket.recv(HEADER_LENGTH)
            user_length = int(user_length.decode())
            username = client_socket.recv(user_length)
            message = client_socket.recv(1024)
            recieve_message(username, message)

            #print(f'{username} > {message}')
    except IOError as e:
        if e.errno != errno.EAGAIN and  e.errno != errno.EWOULDBLOCK:
            print( 'reading error' , str (e))
            sys.exit()
    except  Exception as e:
        print ('Genral error', str(e))
        pass