// Toggle submenus
function toggleSubmenu(id) {
  const submenu = document.getElementById(`${id}-submenu`);
  submenu.style.display = submenu.style.display === "block" ? "none" : "block";
}

// Stop event propagation for submenu elements
document.querySelectorAll(".submenu input, .submenu button").forEach(element => {
  element.addEventListener("click", (e) => {
      e.stopPropagation();
  });
});

// Add activity to itinerary
function addActivity() {
  const dayInput = document.getElementById("day-input");
  const activityInput = document.getElementById("activity-input");
  const day = dayInput.value.trim();
  const activity = activityInput.value.trim();

  if (day === "" || activity === "") {
      alert("Please enter both day and activity.");
      return;
  }

  const table = document.getElementById("itinerary-table");
  const row = table.insertRow(-1);
  const dayCell = row.insertCell(0);
  const activityCell = row.insertCell(1);

  dayCell.textContent = day;
  activityCell.textContent = activity;

  // Clear inputs
  dayInput.value = "";
  activityInput.value = "";
}

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

      // Display bot response
      chatBox.innerHTML += `<div class="message bot">${botReply}</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
      console.error("Error:", error);
  }
});