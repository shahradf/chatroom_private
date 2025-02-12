Chatroom Application in Python

This project is a simple chatroom application developed using Python's socket programming. It allows multiple clients to connect to a server and exchange messages in real-time.
Features

    User Authentication: Users must provide a valid username and password to connect.
    Admin Controls: Administrators can manage user access and permissions.
    Real-Time Messaging: Clients can send and receive messages instantly.
    User Management: Administrators can mute or ban users as needed.

Requirements

    Python 3.x
    peewee library for database management

Installation

    Clone the Repository:

    git clone https://github.com/shahradf/chatroom_private
    cd chatroom_private

Install Dependencies:

    pip install peewee

    Set Up the Database:

    The application uses a SQLite database to store user information. Ensure that the database file is present in the project directory. If not, it will be created automatically upon running the server for the first time.

Usage

    Start the Server:

python server.py

The server will prompt for an administrator username and password. Enter the credentials to proceed.

Start the Client:

python client.py

The client will prompt for the server's host and port, followed by the username and password. Enter the credentials to connect to the chatroom.