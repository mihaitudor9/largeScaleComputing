# -*- coding: utf-8 -*-
import socket
import json
from _thread import *

import cherrypy as cherrypy
import requests
import simplejson as simplejson




# a function that handles requests from the individual client by a thread
#threaded_client() connects to each individual client on the different address given by the server
def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server\n'))
    while True:
        # using recv() function to get data from each client independently and then we simply return the reply to the
        # particular client with the same message with string concatenate “Server Says” in the beginning.
        data = connection.recv(1024)
        reply = 'Server Says: ' + data.decode('utf-8')
        data = data[0]
        print(" Received message is '{}'".format(data))
        if not data:
            break
        connection.sendall(str.encode(reply))

    connection.close()

def server():
    ServerSocket = socket.socket()
    # declare host and port on which we need to communicate with clients
   # host = socket.gethostname()
   # ip = socket.gethostbyname(host)
    ip = "127.0.0.1"
    print(ip)
    port = 13370
    ThreadCount = 0
    #if it binds successfully then it starts waiting for the client otherwise
    # it returns the error that occurred while establishing a connection
    try:
        ServerSocket.bind((ip, port))
    except socket.error as e:
        print(str(e))
    print('Waitiing for a Connection..')
    ServerSocket.listen(5)
    # use a while loop to make it run Server endlessly until we manually stop the Server
    while True:
        # accept connection from client using accept() function of socket server.
        # It returns the type of client which has connected and along with the unique thread number or address provided to it.
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        # Registration(id, firstname, publickey, ServerSocket, client1)
        # use start_new_thread() function of thread class which creates or assign a new thread to each client to handle them individually.
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
      # ThreadCount == 1:
            #change the path according to location of config_1.json in your laptop

       # if ThreadCount == 2:

    ServerSocket.close()

#def Registration(id, firstname,  publickey, s,client1):

if __name__ == '__main__':
    #obj1 = reading('/Users/wafaaaljbawi/Desktop/largeScaleComputing/data/config_1.json')
  #  ip = obj1['server']['ip']
  #  print('Retrieved IP address from JSON: ')
   # print(ip)

   # port = obj1['server']['port']
    print('Using port: ')
  #  print(port)
    print('-------------')
    server()
