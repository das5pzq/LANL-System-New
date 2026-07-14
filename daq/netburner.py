import socket 
from threading import Thread

class NetBurner(Thread):
    def __init__(self, ip_address="192.168.1.158", port=23):
        Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open()

    def open(self):
        try:
            self.client.bind((self.ip_address, self.port))
            self.client.listen()
            self.client.connect((self.ip_address, self.port))
        except ConnectionRefusedError:
            print(f"Connection refused: {self.ip_address}:{self.port} is not listening")

        except TimeoutError:
            print(f"Timeout connecting to {self.ip_address}:{self.port}")
        
        except OSError as e:
            print(f"Timeout connecting to {self.ip_address}:{self.port}")

        except Exception as e:
            print(f"Error connecting to {self.ip_address}:{self.port}: {e}")
    
    def close(self):
        self.client.close()

    def read(self):
        self.client.listen()
        conn, addr = self.client.accept()
        with conn: 
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
        return data

    def write(self, value):
        self.client.listen()
        conn, addr = self.client.accept()
        with conn:
            conn.send(value.to_bytes(1, 'big'))
