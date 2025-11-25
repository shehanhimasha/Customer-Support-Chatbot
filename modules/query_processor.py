"""
query_processor.py
-------------------
Purpose:
    Orchestrates the chatbot pipeline:
        - Preprocess user input
        - Detect intent & extract entities
        - Apply business rules
        - Generate final response
"""

import re
from modules.nlu import detect_intent_and_entities
from modules.rule_engine import RuleEngine
from modules.response_generator import ResponseGenerator

# -----------------------------
# Initialize engines / modules
# -----------------------------
rule_engine = RuleEngine()
response_gen = ResponseGenerator()


class QueryProcessor:
    """
    Handles preprocessing:
        - validation
        - text cleaning
        - normalization
    """

    def validate_input(self, text):
        """Checks for empty or meaningless input."""
        if not text or not isinstance(text, str):
            return False

        # Reject input with only symbols/spaces
        if re.fullmatch(r"[\s\W_]+", text):
            return False

        return True

    def clean_text(self, text):
        """Normalizes text for better NLP performance."""
        text = text.lower()
        text = re.sub(r"[^\w\s,.!?]", " ", text)      # remove emojis
        text = re.sub(r"[^a-zA-Z0-9\s,.!?]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def process(self, text):
        """Runs validation + cleaning."""
        if not self.validate_input(text):
            return None
        return self.clean_text(text)


# Singleton instance
query_processor_instance = QueryProcessor()


# -----------------------------
# Top-level pipeline controller
# -----------------------------
def process_user_query(user_input):
    """
    FULL PIPELINE:
        1. Clean input
        2. Detect intent + entities
        3. Auto-adjust intent (order-ID only case)
        4. Apply business rules
        5. Generate final response
    """

    # 1) Preprocessing
    cleaned_input = query_processor_instance.process(user_input)
    if not cleaned_input:
        return "⚠️ Sorry, I didn't understand that. Please try again."

    # 2) Intent + entity detection
    intent, entities = detect_intent_and_entities(cleaned_input)

    # ----------------------------------------------------
    # 3) AUTO-FIX: If the user only typed "ORD1234"
    #    → Treat it as "track_order"
    # ----------------------------------------------------
    if intent == "provide_order_id":
        intent = "track_order"

    # 4) Apply rule engine
    rule_output = rule_engine.apply_rules(intent, entities)

    # 5) Build response
    return response_gen.generate(rule_output, intent)
