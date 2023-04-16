import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import os 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from client import Client
from server import Server
import threading
import time
import random

def open_file():
    text_transfer_file.set("loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file")
    if file:
        

        file_btn.set("Browse")
    text_transfer_file.set("send file")

def send_message():
    print(text_input.get(1.0, "end-1c"))
    pass 

def check_if_keys_exist():
    popup = tk.Toplevel()
    info = tk.Label(popup, text="Select directory that contains public and private key", font="Raleway")
    info.grid(columnspan=3, column=0, row=0)

    popup.attributes('-topmost',True)
    popup.grab_set()
    folder_selected = tk.filedialog.askdirectory()
    if not os.path.exists(folder_selected+"public_key.pem") or not os.path.exists(folder_selected+"private_key.pem"):
        generate_keys(folder_selected)
    popup.destroy()

def generate_keys(folder_selected):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())
    with open(folder_selected + '/private_key.pem', 'wb') as f:
        f.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(folder_selected +'/public_key.pem', 'wb') as f:
        f.write(pem)

def create_server():
    global server, public_key, recv_text, mylabel

    # TO TEST IF WORKS
    number = 0
    while True:
        if number == 10:
            return
        number = random.randint(1, 100)
        mylabel.config(text=f'hejka naklejka{number}')
        time.sleep(0.3)
    return
    server = Server('localhost', 9999)
    public_key = server.receive_key()       #TODO add session key receiving

    while True:
        text = server.receive_text_from_client()

        if text == "send_text":
            txt = server.receive_text_from_client()
            recv_text += f'{txt}\n'
            mylabel.config(text=recv_text) # update te messagebox
            #print(recv_text)
        
        elif text == "send_file":
            server.receive_file_from_client()

        elif text == "":
            return # text == '' when connection is lost
        
def check_address(text, window=None):
    try:
        text.index(':')
    except ValueError:
        return
    else:
        text = text.split(':')
        print(text)
        if window is not None:
            window.destroy()
        create_client(text[0], int(text[1]))

def create_client(addr, port):
    global client, connected

    client = Client(addr, port)
    while True:
        try:
            client.client.connect((addr, port))
        except ConnectionRefusedError:
            continue
        else:
            #when connected successfully change status to connected
            #do it here
            #-------------------#
            connected = True
            #client.send_key() #send encrypted public key
            #meanwhile server retrieves public key
            return
 
    

def connect():
    popup = tk.Tk()
    info = tk.Label(popup, text="Give another user address:", font="Raleway")
    info.grid(columnspan=3, column=1, row=0)
    text_input = tk.Text(popup,height = 1,width = 20)
    text_input.grid(columnspan=3,column=1, row=1)
    file_btn = tk.Button(popup, text='connect', command=lambda: check_address(text_input.get("1.0", "end-1c"), window=popup), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    file_btn.grid(columnspan=3,column=1, row=2)
    popup.attributes('-topmost',True)
    popup.grab_set()
    popup.mainloop()
    #create_client(text_input.get("1.0", "end-1c"), popup)

def client_handler():
    global client
    connect()
    while True:
        if not connected:
            client = create_client(client.send_address, client.port)


def main():
    global mylabel, client, server, connected, session_key
    connected = False


    root = tk.Tk()
    canvas = tk.Canvas(root, width=500, height=300)
    root.withdraw()
    check_if_keys_exist()

    root.deiconify()

    canvas.grid(columnspan=10, rowspan=10)
    #logo
    logo = Image.open('logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)
    #file transfer text
    instructions = tk.Label(root, text="Select file to transfer", font="Raleway")
    instructions.grid(columnspan=3, column=0, row=1)
    #message fransfer text
    instructions2 = tk.Label(root, text="write your message", font="Raleway")
    instructions2.grid(columnspan=3, column=0, row=3)
    text_input = tk.Text(root,height = 5,
                    width = 20)
    text_input.grid(columnspan=3,column=0, row=4)
    #file transfer button 
    file_btn = tk.Button(root, text='send file', command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    file_btn.grid(column=1, row=2)
    #message tranfer button
    message_btn = tk.Button(root, text='send message', command=lambda:send_message(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    message_btn.grid(column=1,row=5)
    #field to show received text
    mylabel = tk.Label(root, text=f"messages:", font="Raleway")
    mylabel.grid(columnspan=3, column=0, row=6)

    #connection status
    connection = tk.Label(root, text=f"Status: {connected}", font="Raleway")
    connection.grid(columnspan=3, column=0, row=10)

    canvas = tk.Canvas(root, width=600, height=250)
    canvas.grid(columnspan=3)

    t1 = threading.Thread(target=create_server, args=(), daemon=True) #watki sa usuwane przy zakonczeniu programu
    t1.start()
    t2 = threading.Thread(target=lambda:client_handler(), args=(), daemon=True)
    t2.start()
    
    root.mainloop()


if __name__ == '__main__':
    main()
    