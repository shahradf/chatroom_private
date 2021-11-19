import socket
import threading
from peewee import *
from os import system
from sys import stdout
from time import sleep
from sys import exit
from platform import system as osname


def clear():
    if osname == 'nt':
        system('cls')
    else:
        system('clear')


def slow_print(vorody):
    for c in vorody + '\n':
        stdout.write(c)
        stdout.flush()
        sleep(10. / 100)


def banner():
    print('''
    [] -> clear(-)
    [] -> cmd(...)
    [] -> cmd_r(...)
    [] -> mute(...)
    [] -> kick(...)
    [] -> ban(...)
    ''')


def server_manager():
    while True:
        message_s = input('')


user_login = input('username : ')
password_login = input('password : ')
if user_login == 'shahrad8b':
    if password_login == 'login("/w let me in mosi")':
        slow_print('welcome shahrad')
    else:
        print('password is wrong')
        exit(0)
else:
    print('username is wrong')
    exit(0)
clear()

db = SqliteDatabase('people.db')


class Person(Model):
    id = AutoField()
    username = CharField(max_length=24)
    password = CharField(max_length=256)

    class Meta:
        database = db


db.connect()
db.create_tables([
    Person
])


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
            password = c.recv(1024).decode()
            user_ip = c.recv(1024).decode()

            user_db = Person.select().where(Person.username == username)
            if user_db:
                user_db = user_db[-1]
                if password == user_db.password:
                    print(f'new connection ip and username: {user_ip} -- {str(username)}')
                    self.broadcast(f'{username} connected')

                    self.username_lookup[c] = username

                    self.clients.append(c)
                    print(self.clients)

                    threading.Thread(target=self.handle_client, args=(c, addr,)).start()
                else:
                    c.send('exit("idont know what shuld i say:?.")'.encode())
            else:
                c.send('exit("idont know what shuld i say:?.")'.encode())

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
banner()
