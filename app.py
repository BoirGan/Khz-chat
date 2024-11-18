from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Clé secrète pour Flask
socketio = SocketIO(app)  # Activation de Socket.IO

# Route principale pour afficher la page HTML
@app.route('/')
def index():
    return render_template('index.html')

# Gestion des messages envoyés par les clients
@socketio.on('message')
def handle_message(msg):
    print(f"Message reçu : {msg}")  # Affiche le message dans la console
    send(msg, broadcast=True)  # Diffuse le message à tous les clients connectés

# Point d'entrée principal
if __name__ == '__main__':
    socketio.run(app, debug=True)  # Lancement du serveur Flask
