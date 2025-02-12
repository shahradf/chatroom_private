import socket
import threading
from peewee import SqliteDatabase, Model, CharField, AutoField, BooleanField
from time import sleep
from sys import exit

# Define the database connection and Person model
db = SqliteDatabase('ur_database')

class Person(Model):
    id = AutoField()
    username = CharField(max_length=24)
    password = CharField(max_length=256)
    is_admin = BooleanField(default=False)
    ban = BooleanField(default=False)
    mute = BooleanField(default=False)

    class Meta:
        database = db

class Server:
    def __init__(self):
        db.connect()
        db.create_tables([Person])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.username_lookup = {}
        self.start_server()

    def start_server(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 8569
        self.s.bind((host, port))
        self.s.listen(100)

        print(f"Server running on host: {host}, port: {port}")
        while True:
            c, addr = self.s.accept()
            threading.Thread(target=self.handle_new_connection, args=(c, addr)).start()

    def handle_new_connection(self, c, addr):
        username = c.recv(1024).decode()
        password = c.recv(1024).decode()
        user_ip = c.recv(1024).decode()

        user_db = Person.select().where(Person.username == username).first()

        if user_db and password == user_db.password and not user_db.ban:
            self.broadcast(f'{username} connected from {user_ip}')
            self.username_lookup[c] = username
            self.clients.append(c)
            threading.Thread(target=self.handle_client_messages, args=(c, addr)).start()
        else:
            c.send('Invalid username or password, or user is banned.'.encode())
            c.close()

    def broadcast(self, msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client_messages(self, c, addr):
        try:
            while True:
                msg = c.recv(1024).decode()
                if msg:
                    self.handle_admin_commands(c, msg)
                    self.broadcast(f"{self.username_lookup[c]}: {msg}")
        except Exception as e:
            self.remove_client(c)

    def handle_admin_commands(self, c, msg):
        username = self.username_lookup.get(c)
        if not username:
            return
        user_db = Person.select().where(Person.username == username).first()
        if user_db.is_admin and msg.startswith('!kick'):
            target_user = msg.split()[1]
            self.kick_user(target_user)

    def kick_user(self, username):
        for client, user in self.username_lookup.items():
            if user == username:
                client.send("You have been kicked.".encode())
                client.close()
                self.remove_client(client)

    def remove_client(self, c):
        self.clients.remove(c)
        print(f"{self.username_lookup[c]} left the room.")
        self.broadcast(f"{self.username_lookup[c]} has left the room.")
        del self.username_lookup[c]


if __name__ == '__main__':
    server = Server()