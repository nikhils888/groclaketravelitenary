let dayCounter = 1;

// Show the selected tab and hide others
function showTab(tabId) {
    const tabs = document.querySelectorAll(".tab");
    const submenus = document.querySelectorAll(".submenu");

    tabs.forEach(tab => tab.classList.remove("active"));
    submenus.forEach(submenu => submenu.classList.remove("active"));

    document.getElementById(`${tabId}-tab`).classList.add("active");
    document.getElementById(`${tabId}-submenu`).classList.add("active");
}

// Add activity to itinerary
function addActivity() {
    const activityInput = document.getElementById("activity-input");
    const activity = activityInput.value.trim();

    if (activity === "") {
        alert("Please enter an activity.");
        return;
    }

    const tableBody = document.querySelector("#itinerary-table tbody");
    const row = tableBody.insertRow(-1);

    // Add non-editable day cell
    const dayCell = row.insertCell(0);
    dayCell.classList.add("day-cell");
    dayCell.textContent = `Day ${dayCounter}`;

    // Add editable activity cell
    const activityCell = row.insertCell(1);
    activityCell.classList.add("activity-cell");
    activityCell.contentEditable = true;
    activityCell.placeholder = "Enter activity";
    activityCell.textContent = activity;

    // Increment day counter
    dayCounter++;

    // Clear activity input
    activityInput.value = "";
}

// Add booking to bookings list
// Add booking to bookings list
function addBooking() {
  const bookingTypeInput = document.getElementById("booking-type-input");
  const bookingDetailsInput = document.getElementById("booking-details-input");
  const bookingType = bookingTypeInput.value.trim();
  const bookingDetails = bookingDetailsInput.value.trim();

  if (bookingType === "" || bookingDetails === "") {
      alert("Please enter both booking type and details.");
      return;
  }

  const list = document.getElementById("bookings-list");
  const listItem = document.createElement("li");
  listItem.innerHTML = `
      <input type="checkbox" id="${bookingType.toLowerCase().replace(/\s/g, '-')}">
      <label for="${bookingType.toLowerCase().replace(/\s/g, '-')}">
          <strong>${bookingType}:</strong> ${bookingDetails}
      </label>
  `;
  list.appendChild(listItem);

  // Make the booking item editable on double-click
  listItem.addEventListener("dblclick", () => {
      listItem.contentEditable = true;
      listItem.focus();
  });

  // Save changes when the user finishes editing
  listItem.addEventListener("blur", () => {
      listItem.contentEditable = false;
  });

  // Clear inputs
  bookingTypeInput.value = "";
  bookingDetailsInput.value = "";
}

// Handle chat form submission
document.getElementById("chat-form").addEventListener("submit", async function (e) {
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
        const botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot");

        const formattedReply = botReply
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") 
        .replace(/\n/g, "<br>"); 

        botMessage.innerHTML = formattedReply; 
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;


        // Display bot response
        // chatBox.innerHTML += `<div class="message bot">${botReply}</div>`;
        // chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error("Error:", error);
    }
});

// Show the Itinerary tab by default
showTab("itinerary");