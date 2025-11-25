"""
main.py
-------------------
Purpose:
    Entry point to run the chatbot via command-line interface (CLI).
    Handles user input and displays responses from the chatbot.

Why this module exists:
    - Keeps CLI or interface logic separate from core application logic.
    - Allows the chatbot to be extended to other interfaces (web/mobile) without touching the core pipeline.
"""

from app import chatbot_response

def start_chatbot():
    """
    Starts the chatbot loop to interact with the user via CLI.
    """
    print("Welcome to E-Commerce Support Chatbot!")
    print("Type 'exit' to quit.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Thank you! Have a great day! 👋")
            break

        # Get chatbot response
        response = chatbot_response(user_input)

        # Display response
        print(f"Chatbot: {response}\n")

if __name__ == "__main__":
    start_chatbot()
