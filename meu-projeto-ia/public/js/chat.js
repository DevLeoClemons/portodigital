const inputChat = document.querySelector('.chat-input-container input');
const btnSend = document.querySelector('.btn-send');

btnSend.addEventListener('click', () => {
    const texto = inputChat.value.trim();
    if (texto === "") return;

    console.log("Enviar para o backend Node.js:", texto);
    
    inputChat.value = ""; 
});

inputChat.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        btnSend.click();
    }
});