# -*- coding: utf-8 -*-
import socket

def server():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    print(ip)
    port = 8080
    
    s = socket.socket()
    s.bind((ip, port))
    
    s.listen(1)
    
    while True:
        c, adress = s.accept()
        print("Connection from: " + str(adress))
        
        try:
            while True:
                data = c.recv(1024).decode('utf-8')
                if not data:
                    break
                print('from online user: ' + data)
                data = 'Hello World! Received data: ' + data
                c.send(data.encode('utf-8'))
        except socket.error as e:
            print("Exception caught for ", e.strerror)
        
        c.close()
        
    
    
if __name__ == '__main__':
    server()
    

