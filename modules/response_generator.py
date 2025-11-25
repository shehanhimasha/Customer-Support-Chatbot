"""
response_generator.py
-------------------
Purpose:
    Formats and generates final responses for the chatbot.
    Converts the raw output of the RuleEngine into readable, conversational messages.

Why this module exists:
    - Separates response formatting from business logic.
    - Keeps chatbot messages consistent and friendly.
    - Allows future personalization and multi-lingual support.

Used by:
    - query_processor.py (orchestrator)
"""

import random

class ResponseGenerator:
    """
    ResponseGenerator
    -----------------
    Responsibilities:
        - Format raw output from the RuleEngine.
        - Add conversational phrases to improve UX.
        - Handle unknown or unsupported intents gracefully.

    Not responsible for:
        - Understanding user input (NLU does this)
        - Applying business rules (RuleEngine does this)
        - Data storage or persistence
    """

    def __init__(self):
        # Predefined templates for unknown queries or errors
        self.unknown_responses = [
            "I'm sorry, I didn't quite get that. Can you please rephrase?",
            "Hmm, I couldn't understand. Could you clarify?",
            "Oops! I didn't understand that. Try asking about orders, returns, or products."
        ]

    def generate(self, rule_output, intent=None):
        """
        Generates a friendly chatbot response.

        Parameters:
            rule_output (str): Raw text returned by the RuleEngine
            intent (str, optional): Detected intent for context-aware responses

        Returns:
            str: Final user-friendly chatbot response
        """

        # Handle unknown intent
        if intent == "unknown" or not rule_output:
            return random.choice(self.unknown_responses)

        # Add conversational phrase for certain intents
        if intent == "track_order":
            return f"✅ Here's the update for your order:\n{rule_output}"

        if intent == "return_policy":
            return f"📦 Return/Refund Info:\n{rule_output}"

        if intent == "product_recommendation":
            return f"💡 Recommended products:\n{rule_output}"

        # Default fallback
        return rule_output
