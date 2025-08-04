document.getElementById("send-btn").addEventListener("click", async () => {
    const input = document.getElementById("user-input").value;

    const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
    });

    const data = await response.json();

    if (data.response) {
        document.getElementById("ai-response").innerText = data.response;
    } else {
        document.getElementById("ai-response").innerText = "Hubo un error.";
    }
});
