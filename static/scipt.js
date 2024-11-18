const socket = io(); // Connecte au serveur Flask

const inputBox = document.getElementById('input-box');
const messages = document.getElementById('messages');

// Envoi d'un message lorsque l'utilisateur appuie sur "Entrée"
inputBox.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        const message = inputBox.value;
        if (message.trim()) {
            socket.send(`VOUS : ${message}`);
            inputBox.value = ''; // Efface l'input
        }
    }
});

// Réception et affichage des messages
socket.on('message', function(msg) {
    const newMessage = document.createElement('div');
    newMessage.textContent = msg;
    messages.appendChild(newMessage);

    // Scroll vers le bas automatiquement
    messages.scrollTop = messages.scrollHeight;
});
