"""
nlu.py
------
Purpose:
    Handles Natural Language Understanding (NLU) by:
        - Detecting user intent
        - Extracting entities (order IDs, categories, etc.)
"""

import json
import re

# Load intents.json
with open("data/intents.json", "r", encoding="utf-8") as f:
    INTENTS = json.load(f)


# ---------------------------------------------
# GREETING KEYWORDS (fix for your main problem)
# ---------------------------------------------
GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]


def detect_intent_and_entities(user_input):
    """
    Returns:
        (intent: str, entities: dict)
    """

    intent_detected = "unknown"
    entities = {}

    text = user_input.lower().strip()

    # ---------------------------------------------
    # 1) GREETING INTENT (NEW FIX)
    # ---------------------------------------------
    for g in GREETINGS:
        if text.startswith(g):
            return "greet", {}

    # ---------------------------------------------
    # 2) INTENT DETECTION USING intents.json
    # ---------------------------------------------
    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            if phrase in text:  # simple keyword match
                intent_detected = intent
                break
        if intent_detected != "unknown":
            break

    # ---------------------------------------------
    # 3) Extract Order ID (ORD1234)
    # ---------------------------------------------
    order_match = re.search(r"\b(ord\d+)\b", text, re.IGNORECASE)
    if order_match:
        entities["order_id"] = order_match.group(1).upper()

    # ---------------------------------------------
    # 4) If ONLY an order ID is given
    # ---------------------------------------------
    if "order_id" in entities and intent_detected == "unknown":
        intent_detected = "provide_order_id"

    return intent_detected, entities
