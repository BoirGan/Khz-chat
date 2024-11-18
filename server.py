import socket
import threading
import os

clients = []  # Liste des clients connectés
client_pseudonyms = {}  # Dictionnaire des pseudonymes des clients

# Fonction pour gérer les messages envoyés par les clients
def handle_client(client_socket, client_address):
    print(f"Connexion de {client_address}")
    
    # Demande du pseudonyme
    client_socket.send("Veuillez entrer un pseudonyme en utilisant la commande /pseudo 'NAME' : ".encode("utf-8"))
    
    while True:
        try:
            # Réception des données du client
            message = client_socket.recv(1024).decode("utf-8")
            
            # Commande pour définir le pseudonyme
            if message.startswith("/pseudo "):
                pseudonym = message.split(" ", 1)[1]  # On récupère le nom après /pseudo
                client_pseudonyms[client_socket] = pseudonym
                client_socket.send(f"Pseudonyme défini à {pseudonym}".encode("utf-8"))
                broadcast(f"{pseudonym} a rejoint le chat.", client_socket)
            else:
                # Si un message est envoyé, le transmettre à tous les clients
                if client_socket in client_pseudonyms:
                    pseudonym = client_pseudonyms[client_socket]
                    broadcast(f"{pseudonym}: {message}", client_socket)
                else:
                    client_socket.send("Veuillez définir un pseudonyme avec la commande /pseudo 'NAME'".encode("utf-8"))
        except:
            # En cas d'erreur (par exemple déconnexion), fermer la connexion
            print(f"Client {client_address} déconnecté.")
            clients.remove(client_socket)
            client_socket.close()
            break

# Fonction pour envoyer un message à tous les clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                # En cas d'erreur d'envoi, déconnecter le client
                clients.remove(client)
                client.close()

# Fonction pour démarrer le serveur
def start_server():
    # Récupérer le port à partir de la variable d'environnement 'PORT' de Render, ou utiliser un port par défaut
    port = int(os.getenv("PORT", 5555))  # Utilise le port de Render ou 5555 en local pour les tests

    # Créer un socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Lier le serveur à l'adresse 0.0.0.0 et au port dynamique
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Serveur démarré sur le port {port}. En attente de connexions...")

    while True:
        # Accepter une connexion client
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        
        # Lancer un thread pour gérer ce client
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

# Démarrer le serveur
if __name__ == "__main__":
    start_server()
