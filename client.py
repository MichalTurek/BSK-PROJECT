import socket
import tqdm
import os
import time

class Client():
    def __init__(self, address, port):
        self.send_address = address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def send_text(self, text):
        self.client.send("send_text".encode())
        self.client.send(text.encode())

    def send_file(self, filepath):
        self.client.send("send_file".encode())

        with open(filepath, "rb") as f:
            file_size = os.path.getsize(filepath)
            idx = filepath[::-1].find('.')
            extension = filepath[-idx:]
            self.client.send(f"received_file.{extension}".encode())
            self.client.send(str(file_size).encode())

            data = f.read()
            progress = tqdm.tqdm(unit="8", unit_scale=True, unit_divisor=1000, total=int(file_size))
            packet_size = 1024

            while True:
                if packet_size > len(data):
                    self.client.send(data)
                    progress.update(1024)
                    break
   
                time.sleep(0.08)
                self.client.send(data[:packet_size])
                progress.update(1024)
                data = data[packet_size:]

            self.client.send(b"<END>")

    def send_key(self, key):
        self.client.send(key.encode())



        
