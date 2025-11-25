"""
rule_engine.py
-------------------
Purpose:
    Implements business logic rules for the chatbot.
    Processes detected intents and entities to provide meaningful
    information by interacting with the knowledge base (JSON files).

Why this module exists:
    - Separates decision-making from NLU and response formatting.
    - Keeps business logic centralized, easy to maintain.
    - Supports future expansion (more intents, complex rules).

Used by:
    - query_processor.py (orchestrator)
"""

from modules.data_loader import DataLoader

class RuleEngine:
    """
    RuleEngine
    -----------
    Applies chatbot rules based on user intent and extracted entities.

    Responsibilities:
        - Track order status
        - Provide return/refund policies
        - Recommend products
        - Centralized access to knowledge base (via DataLoader)
    
    Not responsible for:
        - Text cleaning
        - NLU processing
        - Formatting user response
    """

    def __init__(self):
        """
        Initialize RuleEngine with access to JSON knowledge base.
        """
        self.loader = DataLoader()
        self.orders = self.loader.load_json("orders.json")
        self.products = self.loader.load_json("products.json")
        self.faqs = self.loader.load_json("faqs.json")

    def track_order(self, order_id):
        """
        Retrieves order information for a given order ID.

        Parameters:
            order_id (str): The ID of the order.

        Returns:
            str: Human-readable order status.
        """
        if not order_id:
            return "Please provide a valid order ID."

        order_info = self.orders.get(order_id)
        if order_info:
            return f"Order #{order_id} is currently '{order_info['status']}'. Expected delivery: {order_info.get('delivery_date', 'N/A')}."
        else:
            return f"Order #{order_id} was not found in our system."

    def return_policy(self, order_id=None):
        """
        Provides return/refund information.

        Parameters:
            order_id (str, optional): Specific order ID for tailored info.

        Returns:
            str: Return policy message.
        """
        if order_id and order_id in self.orders:
            return f"You can return Order #{order_id} within {self.orders[order_id].get('return_days', 7)} days of delivery."
        else:
            return self.faqs.get("return_policy", "Our standard return policy allows returns within 7 days of delivery.")

    def recommend_product(self, category=None):
        """
        Recommends products from the catalog.

        Parameters:
            category (str, optional): Product category for filtered recommendation.

        Returns:
            str: List of recommended products.
        """
        recommendations = []
        for product_id, info in self.products.items():
            if category:
                if info.get("category") == category:
                    recommendations.append(f"{info['name']} (${info['price']})")
            else:
                recommendations.append(f"{info['name']} (${info['price']})")

        if recommendations:
            return "Here are some recommendations:\n" + "\n".join(recommendations[:5])
        else:
            return "Sorry, we have no products to recommend right now."

    def apply_rules(self, intent, entities):
        """
        Main interface to apply rules based on intent and entities.

        Parameters:
            intent (str): Detected intent.
            entities (dict): Extracted entities from NLU.

        Returns:
            str: Result of business logic processing.
        """
        if intent == "track_order":
            return self.track_order(entities.get("order_id"))
        elif intent == "return_policy":
            return self.return_policy(entities.get("order_id"))
        elif intent == "product_recommendation":
            return self.recommend_product(entities.get("category"))
        else:
            return "Sorry, I could not understand your request. Please try again or ask about orders, returns, or products."
