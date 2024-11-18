import tkinter as tk
from tkinter import messagebox
import threading
import socket

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("khz-chat.onrender.com", 10000))  # Utilisez l'URL et le port corrects


# Fonction pour recevoir les messages du serveur dans la GUI
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                messages_display.insert(tk.END, f"{message}\n")
                messages_display.yview(tk.END)  # Faire défiler vers le bas
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            break

# Fonction pour envoyer un message au serveur
def send_message(event=None):  # Ajout de event=None pour la compatibilité avec bind
    message = message_entry.get()
    if message.strip():
        # Afficher le message localement avec un préfixe "Vous>"
        messages_display.insert(tk.END, f"Vous> {message}\n")
        messages_display.yview(tk.END)
        
        # Envoyer le message au serveur
        client_socket.send(message.encode("utf-8"))
        message_entry.delete(0, tk.END)
    else:
        messagebox.showinfo("Erreur", "Veuillez entrer un message.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Chat Windows XP")
root.geometry("400x400")
root.config(bg="#A3A3A3")

# Style de la fenêtre inspiré de Windows XP
root.option_add("*Font", "Arial 10")  # Polices de Windows XP (utilisation de Arial)
root.option_add("*Background", "#A3A3A3")  # Fond gris

# Liste des messages
chat_frame = tk.Frame(root, bg="#A3A3A3")
chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Zone de défilement pour afficher les messages
scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Utiliser un widget Text pour afficher les messages avec défilement horizontal et vertical
messages_display = tk.Text(chat_frame, width=50, height=15, wrap=tk.WORD, font=("Arial", 10), bg="#E0E0E0", fg="#000000")
messages_display.pack()

# Ajouter une barre de défilement horizontale et verticale
messages_display.config(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)
scrollbar.config(command=messages_display.yview)

# Zone de saisie du message
message_entry = tk.Entry(root, width=40, font=("Arial", 10), relief="sunken", bg="#FFFFFF")
message_entry.pack(pady=5)

# Lier la touche "Enter" pour envoyer le message
message_entry.bind("<Return>", send_message)

# Bouton pour envoyer le message
send_button = tk.Button(root, text="Envoyer", command=send_message, font=("Arial", 10), relief="raised", bg="#A3A3A3", activebackground="#D0D0D0")
send_button.pack(pady=5)

# Fonction pour quitter
def quit_chat():
    client_socket.close()
    root.quit()

# Bouton pour quitter
quit_button = tk.Button(root, text="Quitter", command=quit_chat, font=("Arial", 10), relief="raised", bg="red", fg="white")
quit_button.pack(pady=5)

# Lancer un thread pour recevoir les messages
threading.Thread(target=receive_messages, daemon=True).start()

# Démarrer la boucle principale Tkinter
root.mainloop()
