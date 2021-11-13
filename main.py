import socket
import threading


class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = socket.gethostbyname(socket.gethostname())
        port = int(8569)

        self.clients = []

        self.s.bind((host, port))
        self.s.listen(100)

        print('running on host: ' + str(host))
        print('running on port: ' + str(port))

        self.username_lookup = {}

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode()
            user_up = c.recv(1024).decode()
            print(f'new connection ip and username: {user_up} -- {str(username)}')
            self.broadcast(f'{username} connected')

            self.username_lookup[c] = username

            self.clients.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client(self, c, addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)

                print(str(self.username_lookup[c]) + ' left the room.')
                self.broadcast(str(self.username_lookup[c]) + ' has left the room.')

                break

            if msg.decode() != '':
                print('new message: ' + str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)


server = Server()
