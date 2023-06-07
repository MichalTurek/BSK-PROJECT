import socket
import tqdm
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class Client():
    def __init__(self, address, port):
        self.send_address = address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session_key = b''
        self.cipher_mode = ''
    
    def send_text(self, text):
        self.client.send("send_text".encode())
        print(f'MODE: {self.cipher_mode}')
        self.client.send(self.cipher_mode.encode())
        cipher = ''
        text = bytes(text, 'utf-8')
        if self.cipher_mode == 'CBC':
            cipher = AES.new(self.session_key, AES.MODE_CBC)
            ciphered_text = cipher.encrypt(pad(text, AES.block_size))

            self.client.send(cipher.iv)
            self.client.send(ciphered_text)

        elif self.cipher_mode == 'ECB':
            cipher = AES.new(self.session_key, AES.MODE_ECB)
            ciphered_text = cipher.encrypt(pad(text, AES.block_size))

            self.client.send(ciphered_text)
        
        else:
            return
        
        

    def send_file(self, filepath):
        self.client.send("send_file".encode())
        cipher = ''
        print(f'MODE: {self.cipher_mode}')
        self.client.send(self.cipher_mode.encode())

        if self.cipher_mode == 'CBC':
            cipher = AES.new(self.session_key, AES.MODE_CBC)
            self.client.send(cipher.iv)
        
        elif self.cipher_mode == 'ECB':
            cipher = AES.new(self.session_key, AES.MODE_ECB)

        
        
        with open(filepath, "rb") as f:
            file_size = os.path.getsize(filepath)
            idx = filepath[::-1].find('.')
            extension = filepath[-idx:]
            self.client.send(f"received_file.{extension}*{str(file_size)}".encode())

            data = f.read()
            progress = tqdm.tqdm(unit="8", unit_scale=True, unit_divisor=1000, total=int(file_size))
            packet_size = 1024

            while True:
                if packet_size > len(data):
                    padded = pad(data, AES.block_size)
                    encrypted = cipher.encrypt(padded)
                    self.client.send(encrypted)
                    progress.update(1024)
                    break
   
                time.sleep(0.15)
                padded = pad(data[:packet_size], AES.block_size)

                encrypted = cipher.encrypt(padded)
                self.client.send(encrypted)
                progress.update(1024)
                data = data[packet_size:]

            self.client.send(cipher.encrypt(pad(b"<END>", AES.block_size)))

    def send_key(self, key):
        self.client.send(key)


    def set_cipher_mode(self, mode):
        self.cipher_mode = mode


        
