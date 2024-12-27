from groclake.modellake import ModelLake
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['GROCLAKE_API_KEY'] = os.getenv('GROCLAKE_API_KEY')
os.environ['GROCLAKE_ACCOUNT_ID'] = os.getenv('GROCLAKE_ACCOUNT_ID')


# Initialize ModelLake
model_lake = ModelLake()

# Define the chatbot's persona
chatbot_name = "Yogic Guide"
chatbot_description = "A spiritual guide knowledgeable in the Bhagavad Gita and Yoga Sutras."
chatbot_instructions = "Answer with wisdom from the Bhagavad Gita and Yoga Sutras. Provide practical, compassionate advice to guide the user's spiritual journey."

# Introduce chatbot function
def introduce_chatbot():
    print(f"Welcome to {chatbot_name}!")
    print(f"Description: {chatbot_description}")
    print("Feel free to ask about life, spirituality, or yoga.\n")

# Spiritual Chatbot Loop
def spiritual_chatbot():
    introduce_chatbot()

    # Conversation history
    conversation_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print(f"{chatbot_name}: May your journey be filled with peace and wisdom. Goodbye!")
            break
        
        # Add user's input to history
        conversation_history.append({"role": "user", "content": user_input})

        # Prepare payload
        payload = {
            "messages": conversation_history,
            "max_tokens": 200,
            "temperature": 0.7  # Adjust for creativity or precision
        }

        try:
            # Get chatbot's response
            response = model_lake.chat_complete(payload)
            bot_reply = response.get("answer", "I am here to guide you, but I couldn't process that. Please rephrase.")

            # Display response
            print(f"{chatbot_name}: {bot_reply}\n")

            # Add to conversation history
            conversation_history.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print(f"Error: {e}")
            continue

# Run chatbot
spiritual_chatbot()
