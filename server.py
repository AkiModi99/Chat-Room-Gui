import socket
import threading

HOST = '192.168.0.103'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

#Broadcast - One function which will send one common message to all the clients
def broadcast(message):
	for client in clients:
		client.send(message)


#Handle - This is going to handle all the connections singularly as well as the existing connections
def handle(client):
	while True:
		try:
			message = client.recv(1024)
			print(f"{nicknames[clients.index(client)]} says {message}")
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			nicknames.remove(nickname)
			break

#Receive - This is going to accept new connections
def receive():
	while True:
		client, address = server.accept()
		print(f"Connected with {str(address)}!")

		client.send("NEW CONNECTION ACQUIRED".encode('utf-8'))
		nickname = client.recv(1024)

		nicknames.append(nickname)
		clients.append(client)

		print(f"Nickname of the client is {nickname}".encode('utf-8'))
		broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
		client.send("Connected to the Server\n".encode('utf-8'))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()


print("Server is Active and Running...")
receive()