from dotenv import load_dotenv
from groclake.modellake import ModelLake
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


load_dotenv()

os.environ['GROCLAKE_API_KEY'] = os.getenv('GROCLAKE_API_KEY')
os.environ['GROCLAKE_ACCOUNT_ID'] = os.getenv('GROCLAKE_ACCOUNT_ID')

# Initialize ModelLake
model_lake = ModelLake()

def get_response(user_input):
    """Generates a spiritual response based on the user's query."""
    try:
        # Define the conversation context
        conversation = [
            {"role": "system", "content": "You are a spiritual guide well-versed in the Bhagavad Gita and the Yoga Sutras. Provide meaningful and thoughtful guidance to the user."},
            {"role": "user", "content": user_input}
        ]
        
        # Generate response
        response = model_lake.chat_complete({"messages": conversation, "max_tokens": 3000})
        return response.get('answer', "I'm sorry, I couldn't process that.")
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    if not user_message:
        return jsonify({"response": "I didn't receive any message."})

    bot_reply = get_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
