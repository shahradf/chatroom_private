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


db = SqliteDatabase('people.db')


class Person(Model):
    id = AutoField()
    username = CharField(max_length=24)
    password = CharField(max_length=256)
    is_admin = BooleanField(default=False)
    ban = BooleanField(default=False)
    mute = BooleanField(default=False)

    # nickname = CharField(max_length=30)

    class Meta:
        database = db


db.connect()
db.create_tables([
    Person
])

user_login = input('username : ')
password_login = input('password : ')
is_user_admin = Person.select().where((Person.username == user_login) & (Person.is_admin == True))
if is_user_admin:
    user = is_user_admin[-1]
    if password_login == user.password:
        slow_print(f'welcome {user_login}')
    else:
        print('password is wrong')
        exit(0)
else:
    print('username is wrong')
    exit(0)
#clear()


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

            if user_db := Person.select().where(Person.username == username):
                user_db = user_db[-1]
                if password == user_db.password and user_db.ban == False:
                    print(f'new connection ip and username: {user_ip} -- {str(username)}')
                    self.broadcast(f'{username} connected')

                    self.username_lookup[c] = username
                    print(self.username_lookup)
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
                username = self.username_lookup[c]
                if user_db := Person.select().where(Person.username == username):
                    user_db = user_db[-1]
                    if user_db.mute == False:
                        msg = c.recv(1024)
                        if user_db.is_admin == True:
                            msg_an = msg.decode().split()
                            if msg_an[0] == '!kick':
                                username = msg_an[1]
                                user_select = self.username_lookup.keys()
                                for user_f in user_select:
                                    if self.username_lookup[user_f] == username:
                                        user_f.shutdown(socket.SHUT_RDWR)
                                        self.clients.remove(user_f)

                    else:
                        c.send('you\'r muted'.encode())
                        c.shutdown(socket.SHUT_RDWR)
                        self.clients.remove(c)
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
