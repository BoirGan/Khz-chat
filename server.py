import socket
import threading

# Fonction qui gère chaque client
def handle_client(client_socket, addr):
    print(f"Connexion de : {addr}")
    client_socket.send("Bienvenue dans le serveur simplifié.".encode("utf-8"))

    while True:
        message = client_socket.recv(1024)
        if not message:
            break
        print(f"Message reçu de {addr} : {message.decode('utf-8')}")
        client_socket.send(f"Message reçu : {message.decode('utf-8')}".encode("utf-8"))

    print(f"Déconnexion de : {addr}")
    client_socket.close()

# Création du serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5555))  # Écoute sur toutes les interfaces
server.listen(5)  # Nombre de connexions en attente

print("Serveur démarré. En attente de connexions...")

while True:
    # Acceptation des connexions
    client_socket, addr = server.accept()
    
    # Lancer un thread pour gérer chaque client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()

server.close()
