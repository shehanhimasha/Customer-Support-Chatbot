"""
app.py
-------------------
Purpose:
    Core application logic for the Customer Support Chatbot.
    Orchestrates the flow of user input through the modules:
        1. Query Processor
        2. NLU (Intent & Entity Detection)
        3. Rule Engine (Business Logic)
        4. Response Generator (Final output)

Why this module exists:
    - Keeps main.py minimal and clean.
    - Separates application logic from user interaction.
    - Central place to manage chatbot pipeline.

Used by:
    - main.py (entry point)
"""

from modules.query_processor import process_user_query

def chatbot_response(user_input):
    """
    Processes user input and returns the final chatbot response.

    Parameters:
        user_input (str): The text input from the user.

    Returns:
        str: Final formatted response to display to the user.
    """
    response = process_user_query(user_input)
    return response
