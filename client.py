import socket
import threading


class Client:
    def __init__(self):
        self.connection_to_server()

    def connection_to_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                host = input('enter host name : ')
                port = int(input('enter port : '))
                self.s.connect((host, port))

                break
            except:
                print("couldn't connect to server")

        self.username = input('enter username : ')
        self.s.send(self.username.encode())
        self.my_ip = socket.gethostbyname(socket.gethostname())
        self.s.send(self.my_ip.encode())

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()

    def handle_messages(self):
        while True:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        while True:
            self.s.send((self.username + ' ~> ' + input()).encode())


client = Client()
