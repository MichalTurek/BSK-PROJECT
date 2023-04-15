import socket
import tqdm
import os
import time

class Server():
    def __init__(self, address, port):
        self.recv_address = address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.recv_address, port))
        self.server.listen()
        self.client, self.addr = self.server.accept()
        #self.key = self.client.recv(1024).decode()
        
    def receive_file_from_client(self):
        file_name = self.client.recv(1024).decode()
        file_size = self.client.recv(1024).decode()
        file = open(file_name, "wb")
        file_bytes = b""
        data = b""
        done = False
        progress = tqdm.tqdm(unit="8", unit_scale=True, unit_divisor=1000, total=int(file_size))
        while not done:
            data += self.client.recv(1024)
            if data[-5:] == b'<END>':
                done = True
            else:
                file_bytes = data
            progress.update(1024)
            time.sleep(0.3)
  
        file.write(file_bytes)
        file.close()

    def receive_text_from_client(self):
        return self.client.recv(1024).decode()

    
    def receive_key(self):
        return self.client.recv(1024).decode()
    