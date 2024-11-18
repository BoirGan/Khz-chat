import socket
import threading

clients = []  # Liste des clients connectés
client_pseudonyms = {}  # Dictionnaire des pseudonymes des clients
lock = threading.Lock()  # Verrou pour synchroniser l'accès aux ressources partagées

# Fonction pour gérer les messages envoyés par les clients
def handle_client(client_socket, client_address):
    print(f"Connexion de {client_address}")
    
    # Demande du pseudonyme
    client_socket.send("Veuillez entrer un pseudonyme en utilisant la commande /pseudo 'NAME' : ".encode("utf-8"))
    
    while True:
        try:
            # Réception des données du client
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break  # Si le message est vide, le client a probablement quitté

            # Commande pour afficher l'aide
            if message == "/help":
                help_message = (
                    "Commandes disponibles :\n"
                    "/pseudo <nom> : Définir votre pseudonyme.\n"
                    "/help : Afficher cette aide.\n"
                    "Message : Envoyer un message aux autres utilisateurs.\n"
                )
                client_socket.send(help_message.encode("utf-8"))
            # Commande pour définir le pseudonyme
            elif message.startswith("/pseudo "):
                pseudonym = message.split(" ", 1)[1].strip()  # On récupère le nom après /pseudo
                if pseudonym:  # Vérifier si le pseudonyme n'est pas vide
                    with lock:
                        client_pseudonyms[client_socket] = pseudonym
                    client_socket.send(f"Pseudonyme défini à {pseudonym}".encode("utf-8"))
                    broadcast(f"{pseudonym} a rejoint le chat.", client_socket)
                else:
                    client_socket.send("Pseudonyme invalide. Veuillez essayer à nouveau.".encode("utf-8"))
            else:
                # Si un message est envoyé, le transmettre à tous les clients
                if client_socket in client_pseudonyms:
                    pseudonym = client_pseudonyms[client_socket]
                    broadcast(f"{pseudonym}: {message}", client_socket)
                else:
                    client_socket.send("Veuillez définir un pseudonyme avec la commande /pseudo 'NAME'".encode("utf-8"))
        except Exception as e:
            print(f"Erreur avec le client {client_address}: {e}")
            break
    # Déconnexion propre
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in client_pseudonyms:
            del client_pseudonyms[client_socket]
    client_socket.close()

# Fonction pour envoyer un message à tous les clients
def broadcast(message, client_socket):
    with lock:
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen(5)
    print("Serveur démarré. En attente de connexions...")

    while True:
        client_socket, client_address = server.accept()
        with lock:
            clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

# Démarrer le serveur
start_server()
