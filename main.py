import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import os 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
def open_file():
    text_transfer_file.set("loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        #text box
        text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
        text_box.insert(1.0, page_content)
        text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=1, row=3)

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
def eryk_connect():
    pass
def connect():
    connected = False
    popup = tk.Toplevel()
    info = tk.Label(popup, text="Give another user address:", font="Raleway")
    info.grid(columnspan=3, column=1, row=0)
    text_input = tk.Text(popup,height = 1,width = 20)
    text_input.grid(columnspan=3,column=1, row=1)
    text_transfer_file = tk.StringVar()
    file_btn = tk.Button(popup, textvariable=text_transfer_file, command=lambda:eryk_connect(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    text_transfer_file.set("connect")
    file_btn.grid(columnspan=3,column=1, row=2)
    popup.attributes('-topmost',True)
    popup.grab_set()

    
if __name__ == '__main__':
   
    
    root = tk.Tk()
    canvas = tk.Canvas(root, width=500, height=300)
    root.withdraw()
    check_if_keys_exist()
    connect()
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
    instructions = tk.Label(root, text="write your message", font="Raleway")
    instructions.grid(columnspan=3, column=0, row=3)
    text_input = tk.Text(root,height = 5,
                    width = 20)
    text_input.grid(columnspan=3,column=0, row=4)
    #file transfer button 
    text_transfer_file = tk.StringVar()
    file_btn = tk.Button(root, textvariable=text_transfer_file, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    text_transfer_file.set("send file")
    file_btn.grid(column=1, row=2)
    #message tranfer button
    text_transfer_message = tk.StringVar()
    message_btn = tk.Button(root, textvariable=text_transfer_message, command=lambda:send_message(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    text_transfer_message.set("send message")
    message_btn.grid(column=1,row=5)

    canvas = tk.Canvas(root, width=600, height=250)
    canvas.grid(columnspan=3)

    
    root.mainloop()