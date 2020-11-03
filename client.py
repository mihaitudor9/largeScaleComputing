import socket


host = '10.97.30.195'
#host = 'OTA-VM-334'
port = 8080
  
s = socket.socket()
s.connect((host, port))
  
message = input('-> ')
while message != 'q':
    s.send(message.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print('Received from server: ' + data)
    message = input('==> ')

s.close()