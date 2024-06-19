import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 1234
USER_LIMIT = 5
active_clients = []

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message == "/quit":
                removeClient(client, username)
                break
            if message != '':
                timestamp, content = message.split('~', 1)
                final_msg = f"{timestamp}~{username}~{content}"
                sendMessageToAll(final_msg)
            else:
                print(f"The message sent from client {username} is empty")
        except:
            removeClient(client, username)
            break

def sendMessageToClient(client, message):
    client.sendall(message.encode())

def sendMessageToAll(message):
    for user in active_clients:
        sendMessageToClient(user[1], message)

def removeClient(client, username):
    global active_clients
    if (username, client) in active_clients:
        active_clients.remove((username, client))
        print(f"Client {username} has disconnected")
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}~SERVER~{username} has left the chat"
        sendMessageToAll(message)
        client.close()

def clientHandler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}~SERVER~{username} joined the chat"
            sendMessageToAll(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(USER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=clientHandler, args=(client,)).start()

if __name__ == '__main__':
    main()
