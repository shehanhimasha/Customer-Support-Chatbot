"""
query_processor.py
-------------------
Purpose:
    Provides a preprocessing pipeline to clean and normalize user inputs
    before being sent to the NLU (Natural Language Understanding) module,
    and orchestrates the chatbot pipeline.

Responsibilities:
    - Validate and clean user input.
    - Detect intent & extract entities.
    - Apply business rules.
    - Generate final response.

Used by:
    - app.py (chatbot controller)
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
    QueryProcessor
    ---------------
    Applies text-cleaning and normalization steps.
    """

    def __init__(self):
        pass  # Reserved for future extensions (e.g., slang dictionaries)

    def validate_input(self, text):
        """
        Ensures the input contains meaningful characters.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not text or not isinstance(text, str):
            return False

        # Reject inputs containing only symbols or spaces
        if re.fullmatch(r"[\s\W_]+", text):
            return False

        return True

    def clean_text(self, text):
        """
        Performs text normalization and cleaning.

        Steps:
            1. Lowercase conversion.
            2. Remove emojis/special Unicode characters.
            3. Remove unwanted punctuation.
            4. Replace multiple spaces with a single space.

        Returns:
            str: Cleaned text.
        """
        # 1. Lowercase
        text = text.lower()

        # 2. Remove emojis and unusual unicode characters
        text = re.sub(r"[^\w\s,.!?]", " ", text)

        # 3. Remove unsupported punctuation 
        text = re.sub(r"[^a-zA-Z0-9\s,.!?]", " ", text)

        # 4. Normalize spacing
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def process(self, text):
        """
        Full preprocessing pipeline.

        Returns:
            str | None:
                - Cleaned text if valid.
                - None if invalid input.
        """
        if not self.validate_input(text):
            return None

        cleaned = self.clean_text(text)
        return cleaned


# -----------------------------
# Create a singleton instance
# -----------------------------
query_processor_instance = QueryProcessor()


# -----------------------------
# Top-level orchestration function
# -----------------------------
def process_user_query(user_input):
    """
    Orchestrates the chatbot pipeline:
    1. Cleans input using QueryProcessor
    2. Detects intent & entities using NLU
    3. Applies business rules using RuleEngine
    4. Generates final response using ResponseGenerator

    Parameters:
        user_input (str): Raw text from the user

    Returns:
        str: Final chatbot response
    """
    # Step 1: Preprocess input
    cleaned_input = query_processor_instance.process(user_input)
    if not cleaned_input:
        return "⚠️ Sorry, I didn't understand that. Please try again."

    # Step 2: NLU: detect intent and entities
    intent, entities = detect_intent_and_entities(cleaned_input)

    # Step 3: Apply business rules
    rule_output = rule_engine.apply_rules(intent, entities)

    # Step 4: Generate response
    response = response_gen.generate(rule_output, intent)

    return response
