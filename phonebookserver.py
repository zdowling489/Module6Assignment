"""
File: phonebookserver.py
Project 10.10
Server for providing phonebook access.
Uses client handlers to handle clients' requests.
"""

from socket import *
from chatclienthandler import ChatClientHandler
from threadsafetranscript import ThreadSafeTranscript


HOST = "localhost"
PORT = 5000
ADDRESS = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
server.listen(5)
transcript = ThreadSafeTranscript()

while True:
    try:
        fName = str(input("Please enter file name followed by extension: "))
        f = open(fName, 'r')
        while True:
            print("Waiting for connection . . .")
            client, address = server.accept()
            print("... connected from: ", address)
            handler = ChatClientHandler(client, transcript)
            handler.start()
    except IOError:
        print("ERROR: You either do not have proper permissions, or file name is incorrect.(" + fName + ")")
        print("File name should be: AddressBook.txt.\n")

# The server now just waits for connections from clients
# and hands sockets off to client handlers

