import socket
import nacl.secret
import nacl.utils

serverprivatekey = 1337
primekey = 99971
generatorkey = 222

def Main():
	host = "127.0.0.1"
	port = 5001
    
	mySocket = socket.socket()
	mySocket.bind((host,port))
    
	mySocket.listen(5)
	conn, addr = mySocket.accept()
	print ("***SERVER: Connection from: " + str(addr))

	clientpublickey = conn.recv(1024).decode()
	if not clientpublickey:return
	                    
	clientpublickey = str(clientpublickey)
	print ("***SERVER: Received: " + str(clientpublickey))

	serverpublickey = str((generatorkey**serverprivatekey) % primekey)
	conn.send(serverpublickey.encode())
	secretkey = (int(clientpublickey)**serverprivatekey) % primekey
	print("***SERVER: secret key: " + str(secretkey)) 

	while True:
		messageRecieved = conn.recv(1024).decode() 
		if not messageRecieved: break
		print("\n***SERVER: Received message from User: " + str(messageRecieved)) 


	conn.close()

                
if __name__ == '__main__':
	Main()