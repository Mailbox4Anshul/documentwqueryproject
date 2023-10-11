document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.getElementById("uploadForm");
    const uploadMessage = document.getElementById("uploadMessage");
    const chatSection = document.getElementById("chatSection");
    const queryForm = document.getElementById("queryForm");
    const chatWindow = document.getElementById("chatWindow");
    const queryInput = document.getElementById("queryInput");

    uploadForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        const fileInput = document.getElementById("fileInput");
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/upload', {method: 'POST', body: formData});
            const result = await response.json();
            uploadMessage.innerHTML = result.message;
            
            if (result.message === "File(s) successfully processed") {
                chatSection.classList.remove("hidden");
            }
        } catch (error) {
            console.log("Error uploading file:", error);
        }
    });

    queryForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        const query = queryInput.value;
        
        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query})
            });
            const result = await response.json();
            
            chatWindow.innerHTML += `<div class="user-message">You: ${query}</div>`;
            chatWindow.innerHTML += `<div class="server-message">Your Virtual Assistant: ${result.response}</div>`;
            
            queryInput.value = '';
            chatWindow.scrollTop = chatWindow.scrollHeight;
        } catch (error) {
            console.log("Error querying:", error);
        }
    });
});
