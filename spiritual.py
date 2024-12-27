import os
from flask import Flask, request, jsonify
from groclake.modellake import ModelLake
from dotenv import load_dotenv
import traceback

load_dotenv()

os.environ['GROCLAKE_API_KEY'] = os.getenv('GROCLAKE_API_KEY')
os.environ['GROCLAKE_ACCOUNT_ID'] = os.getenv('GROCLAKE_ACCOUNT_ID')

model_lake = ModelLake()

# Initialize Flask app
app = Flask(__name__)

SYSTEM_MESSAGE = "You are a spiritual guide, deeply knowledgeable in the Bhagavad Gita and the Yoga Sutras."

@app.route('/', methods=['GET','POST'])
def index():
    try:

        # Get user input and history
        user_input = request.json.get('message', '').strip()
        conversation_history = request.json.get('history', [])

        # Validate user input
        if not user_input:
            return jsonify({"error": "Message field cannot be empty."}), 400

        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Create payload for ModelLake
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                *conversation_history
            ],
            "max_tokens": 150
        }

        # Generate response using ModelLake
        response = model_lake.chat_complete(payload)
        bot_reply = response.get('answer', "Sorry, I couldn't process that.")

        # Append bot reply to conversation history
        conversation_history.append({"role": "assistant", "content": bot_reply})

        # Return response
        return jsonify({"reply": bot_reply, "history": conversation_history})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)
