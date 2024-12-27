document.getElementById("chat-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const userInput = document.getElementById("user-input").value;

  if (userInput.trim() === "") return;

  // Display user message
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div class="message user">${userInput}</div>`;
  document.getElementById("user-input").value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Send message to backend
  try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
      });
      

      const data = await response.json();
      const botReply = data.response;

      // Display bot response
      chatBox.innerHTML += `<div class="message bot">${botReply}</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
      console.error("Error:", error);
  }
});
