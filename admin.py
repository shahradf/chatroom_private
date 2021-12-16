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
clear()


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = input('enter host name : ')
# port = int(input('enter port : '))
# username = input('enter username : ')
# s.send(username.encode())
# password = input('enter password : ')
# s.send(password.encode())
# my_ip = socket.gethostbyname(socket.gethostname())
# s.send(my_ip.encode())
# check = s.recv(1024).decode()
# if check == 'exit("idont know what shuld i say:?.")':
#    print('username or password wrong .')
#    exit(0)


# def send_arg_to_server(arg):
#    s.send(arg.encode())


def mute(user):
    person_ba_p_kochik = Person.select().where(Person.username == user)[-1]
    person_ba_p_kochik.mute = True
    person_ba_p_kochik.save()


def ban(user):
    person_ba_p_kochik = Person.select().where(Person.username == user)[-1]
    person_ba_p_kochik.ban = True
    person_ba_p_kochik.save()


def unmute(user):
    person_ba_p_kochik = Person.select().where(Person.username == user)[-1]
    person_ba_p_kochik.mute = False
    person_ba_p_kochik.save()


def unban(user):
    person_ba_p_kochik = Person.select().where(Person.username == user)[-1]
    person_ba_p_kochik.ban = False
    person_ba_p_kochik.save()


# def kick(username) -> None:
#    send_arg_to_server(f'!kick {username}')


def server_manager():
    clear()
    while True:
        print('''
        [] -> !clear ...
        [] -> !cmd ...
        [] -> !cmd_r ...
        [] -> !mute ...
        [] -> !unmute
        [] -> !kick ...
        [] -> !ban ...
        [] -> !unban
        ''')
        message_s = input('')
        if message_s == '!mute':
            uesrname_select = input('enter username : ')
            mute(uesrname_select)
        if message_s == '!unmute':
            uesrname_select = input('enter username : ')
            unmute(uesrname_select)
        if message_s == '!ban':
            uesrname_select = input('enter username : ')
            ban(uesrname_select)
        if message_s == '!unban':
            uesrname_select = input('enter username : ')
            unban(uesrname_select)


server_manager()
