import socket
import threading


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        while True:
            try:
                host = input('Enter host name: ')
                port = int(input('Enter port: '))
                self.s.connect((host, port))
                break
            except Exception as e:
                print("Couldn't connect to server, please try again.")

        self.username = input('Enter username: ')
        self.s.send(self.username.encode())
        self.password = input('Enter password: ')
        self.s.send(self.password.encode())
        self.my_ip = socket.gethostbyname(socket.gethostname())
        self.s.send(self.my_ip.encode())

        response = self.s.recv(1024).decode()
        if "Invalid username or password" in response:
            print(response)
            exit(0)
        else:
            threading.Thread(target=self.handle_messages, args=()).start()
            threading.Thread(target=self.input_handler, args=()).start()

    def handle_messages(self):
        while True:
            msg = self.s.recv(1024).decode()
            print(msg)

    def input_handler(self):
        while True:
            msg = input()
            self.s.send(f"{self.username} ~> {msg}".encode())

if __name__ == '__main__':
    client = Client()