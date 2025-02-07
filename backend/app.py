from groclake.modellake import ModelLake
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, origins=["http://localhost:8000"])

load_dotenv()

# Set GrocLake API credentials
os.environ['GROCLAKE_API_KEY'] = "c74d97b01eae257e44aa9d5bade97baf"
os.environ['GROCLAKE_ACCOUNT_ID'] = "7431e04ba71289b9862100279768a0d8"

# Initialize ModelLake
model_lake = ModelLake()

# Replace with your AviationStack API key
AVIATIONSTACK_API_KEY = "3842cc0f4b4a0180f8af14907e39c199"

# Replace with your RapidAPI key
RAPIDAPI_KEY = "e46ee220dfmshe31151b886e99bfp186ee9jsn6eb76e66b2df"

def get_flight_data():
    """Fetches real-time flight data from AviationStack for flights from DEL to BOM."""
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "dep_iata": "DEL",  # Departure airport code for Delhi
        "arr_iata": "BOM",  # Arrival airport code for Mumbai
        "limit": 5  # Fetch data for 5 flights (adjust as needed)
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching flight data: {e}")
        return []

def get_hotel_data(location):
    """Fetches hotel data from RapidAPI's Travel Advisor API."""
    url = "https://travel-advisor.p.rapidapi.com/hotels/list"
    querystring = {
        "location_id": "304554",  # Replace with the location ID for Mumbai (BOM)
        "adults": "1",
        "rooms": "1",
        "nights": "2",
        "offset": "0",
        "currency": "USD",
        "order": "asc",
        "limit": "5",  # Fetch data for 5 hotels (adjust as needed)
        "sort": "recommended",
        "lang": "en_US"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        print(response.json().get("data", []))
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching hotel data: {e}")
        return []

def format_itinerary_response(response):
    """Formats the itinerary response with bold subheaders, pointers, and a table for flights and hotels."""
    # Split the response into days
    days = response.split("Day ")[1:]  # Skip the first empty split
    formatted_response = ""

    # Add each day with bold subheaders and pointers
    for day in days:
        day_number = day.split(":")[0]
        activities = day.split(":")[1].strip().split(" - ")
        formatted_response += f"<strong>Day {day_number}:</strong><br>"
        for activity in activities:
            formatted_response += f"• {activity}<br>"
        formatted_response += "<br>"

    # Add flights and hotels in a table
    formatted_response += """
    <strong>Flights and Hotels:</strong>
    <table border="1">
        <tr>
            <th>Type</th>
            <th>Details</th>
            <th>Cost</th>
        </tr>
        <tr>
            <td>Flight</td>
            <td>6E708 by IndiGo, departing at 04:00 from Indira Gandhi International and arriving at Chhatrapati Shivaji International</td>
            <td>TBD</td>
        </tr>
        <tr>
            <td>Hotel</td>
            <td>Check-in at the hotel of your choice in Mumbai</td>
            <td>TBD</td>
        </tr>
        <tr>
            <td>Flight</td>
            <td>D0803 by DHL Air</td>
            <td>TBD</td>
        </tr>
        <tr>
            <td>Flight</td>
            <td>AI2975 by Air India</td>
            <td>TBD</td>
        </tr>
        <tr>
            <td>Flight</td>
            <td>LX9854 by SWISS</td>
            <td>TBD</td>
        </tr>
        <tr>
            <td>Flight</td>
            <td>LH5284 by Lufthansa</td>
            <td>TBD</td>
        </tr>
    </table>
    """

    return formatted_response

def get_travel_itinerary(user_input):
    """Generates a travel itinerary based on the user's query, including flight and hotel data."""
    try:
        # Fetch flight data for DEL to BOM
        flight_data = get_flight_data()

        # Fetch hotel data for Mumbai (BOM)
        hotel_data = get_hotel_data("Mumbai")

        # Append flight data to the user's input
        flight_info = "\n\nFlight Data (DEL to BOM):\n"
        for flight in flight_data:
            flight_info += (
                f"Flight {flight['flight']['iata']} by {flight['airline']['name']} "
                f"from {flight['departure']['airport']} to {flight['arrival']['airport']} "
                f"(Scheduled: {flight['departure']['scheduled']})\n"
            )

        # Append hotel data to the user's input
        hotel_info = "\n\nHotel Data (Mumbai):\n"
        for hotel in hotel_data:
            hotel_info += (
                f"Hotel: {hotel['name']}, "
                f"Rating: {hotel.get('rating', 'N/A')}, "
                f"Price: {hotel.get('price', 'N/A')}, "
                f"Checkout Time: {hotel.get('checkout_time', 'N/A')}\n"
            )

        # Add a marker for flights and hotels at the end
        end_mark = " also represent at the end all available flights including their costs and same for hotels"
        user_input_with_data = user_input + flight_info + hotel_info + end_mark

        # Define the conversation context
        conversation = [
            {"role": "system", "content": "You are a travel planning assistant. Provide detailed and practical travel itineraries based on the user's preferences, flight data, and hotel data."},
            {"role": "user", "content": user_input_with_data}
        ]

        # Generate response using the LLM
        response = model_lake.chat_complete({"messages": conversation, "token_size": 4000})
        formatted_response = format_itinerary_response(response.get('answer', "I'm sorry, I couldn't process that."))
        return formatted_response

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/chat', methods=['POST'])
def plan_trip():
    data = request.get_json()
    user_message = data.get('message')
    if not user_message:
        return jsonify({"response": "I didn't receive any message."})

    # Get travel itinerary, including flight and hotel data
    itinerary = get_travel_itinerary(user_message)
    return jsonify({"response": itinerary})

if __name__ == '__main__':
    app.run(debug=True)