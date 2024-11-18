import socket
import threading

# Fonction pour envoyer des messages
def send_messages(client_socket):
    while True:
        message = input("Vous> ")
        if message.lower() == "exit":
            break
        client_socket.send(message.encode("utf-8"))

# Fonction pour recevoir des messages
def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode("utf-8")
        print(f"Serveur> {message}")

# Création du client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("88.126.194.166", 5555))  # Connexion à l'IP publique du serveur

# Afficher le message de bienvenue
print(client.recv(1024).decode("utf-8"))

# Lancer des threads pour envoyer et recevoir des messages en parallèle
send_thread = threading.Thread(target=send_messages, args=(client,))
receive_thread = threading.Thread(target=receive_messages, args=(client,))
send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()

client.close()
