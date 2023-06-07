import socket
import tqdm
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class Server():
    def __init__(self, address, port):
        self.recv_address = address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.recv_address, port))
        self.session_key = b''
        
    def receive_file_from_client(self):
        mode = self.client.recv(3).decode()
        
        print(f'MODE: {mode}')
        cipher = ''
        if mode == 'CBC':
            iv = self.client.recv(16)
            cipher = AES.new(self.session_key, AES.MODE_CBC, iv=iv)       
        
        elif mode == 'ECB':
            cipher = AES.new(self.session_key, AES.MODE_ECB)

        s = self.receive_text_from_client()
        file_name, file_size = s.split('*')
        file = open(file_name, "wb")
        file_bytes = b""
        data = b""
        done = False
        
        progress = tqdm.tqdm(unit="8", unit_scale=True, unit_divisor=1000, total=int(file_size)+5)

        
            
        while not done:
            received = self.client.recv(1040)
            received = cipher.decrypt(received)
            received = unpad(received, AES.block_size)

            data += received
            if data[-5:] == b'<END>':
                file_bytes = data[:-5]
                done = True
            else:
                file_bytes = data
            progress.update(len(received))
            time.sleep(0.15)
        
  
        file.write(file_bytes)
        file.close()

    def decryptCBC(self, iv, encrypted):
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(encrypted)
        plaintext = unpad(plaintext, AES.block_size).decode()

        return plaintext

    def decryptECB(self, text):
        cipher = AES.new(self.session_key, AES.MODE_ECB)
        plaintext = cipher.decrypt(text)
        plaintext = unpad(plaintext, AES.block_size).decode()
        
        return plaintext

    def receive_text_from_client(self):
        return self.client.recv(1024).decode()
    
    def receive_encrypted_from_client(self):
        return self.client.recv(1024)

    async def receive_key(self):
        return self.client.recv(1024)
    