"""
nlu.py
------
Purpose:
    Detects the intent of the user input and extracts any relevant entities.
    Acts as the Natural Language Understanding (NLU) component.

Used by:
    - query_processor.py
"""

import json
import re

# Load intents.json
with open("data/intents.json", "r", encoding="utf-8") as f:
    INTENTS = json.load(f)


def detect_intent_and_entities(user_input):
    """
    Detects the intent and entities from user input using keyword matching.

    Args:
        user_input (str): Preprocessed user input (cleaned text)

    Returns:
        tuple: (intent (str), entities (dict))
            - intent: detected intent string
            - entities: dictionary of extracted entities
    """

    # Default values
    intent_detected = "unknown"
    entities = {}

    # Simple keyword-based matching
    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            # Exact phrase match
            if phrase in user_input:
                intent_detected = intent
                break
        if intent_detected != "unknown":
            break

    # Extract some simple entities (e.g., order number)
    # Look for patterns like #123, order 123, etc.
    order_match = re.search(r"#?(\d{3,})", user_input)
    if order_match:
        entities["order_number"] = order_match.group(1)

    return intent_detected, entities
