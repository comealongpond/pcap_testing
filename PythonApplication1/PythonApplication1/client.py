import socket
import nacl.secret
import nacl.utils

clientprivatekey = 137
primekey = 99971
generatorkey = 222
#A = (generatorkey**clientkey) % primekey

def Main():
	host = '127.0.0.1'
	port = 5001
	
	mySocket = socket.socket()
	mySocket.connect((host,port))
	
	clientpublickey = str((generatorkey**clientprivatekey) % primekey)
	
	
	mySocket.send(clientpublickey.encode())
	serverpublickey = mySocket.recv(1024).decode()
			
	print ("***CLIENT: Received: " + serverpublickey)


	secretkey = (int(serverpublickey)**clientprivatekey) % primekey
	print("***CLIENT: secret key: " + str(secretkey))

	message = raw_input("Enter your message: ")
	while message != 'q':
		print("***CLIENT: Sending \"" + message + "\"")
		mySocket.send(message)
		message = raw_input("Enter your message: ")
		
	mySocket.close()


#def encrypt(message, secretkey):
	#box = nacl.secret.SecretBox(secretkey)
	#return box.encrypt(message)



if __name__ == '__main__':
	Main()