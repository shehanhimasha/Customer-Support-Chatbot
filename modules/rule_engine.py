"""
rule_engine.py
-------------------
Purpose:
    Implements business logic rules for the chatbot.
"""

from modules.data_loader import DataLoader


class RuleEngine:
    """
    Applies chatbot rules based on user intent and extracted entities.
    """

    def __init__(self):
        self.loader = DataLoader()
        self.orders = self.loader.load_json("orders.json") or {}
        self.products = self.loader.load_json("products.json") or {}
        self.faqs = self.loader.load_json("faqs.json") or {}

    # -------------------------
    # Intent Handlers
    # -------------------------

    def greet(self):
        return "👋 Hi there! How can I help you today? You can ask about orders, returns, or products."

    def ask_order_id(self):
        return "Please provide your order ID (e.g., ORD1234)."

    def track_order(self, order_id):
        if not order_id:
            return "Please provide a valid order ID."

        order_info = self.orders.get(order_id)
        if order_info:
            return (
                f"Order **{order_id}** is currently **'{order_info['status']}'**.\n"
                f"📅 Expected delivery: {order_info.get('delivery_date', 'N/A')}."
            )
        else:
            return f"❌ Order **{order_id}** was not found in our system."

    def return_policy(self, order_id=None):
        if order_id and order_id in self.orders:
            return (
                f"You can return Order **{order_id}** within "
                f"{self.orders[order_id].get('return_days', 7)} days of delivery."
            )

        return self.faqs.get(
            "return_policy",
            "Our standard return policy allows returns within 7 days of delivery."
        )

    def recommend_product(self, category=None):
        recommendations = []

        for product_id, info in self.products.items():
            if category:
                if info.get("category") == category:
                    recommendations.append(f"{info['name']} (${info['price']})")
            else:
                recommendations.append(f"{info['name']} (${info['price']})")

        if recommendations:
            return "Here are some recommendations:\n" + "\n".join(recommendations[:5])

        return "Sorry, we have no products to recommend right now."

    # -------------------------
    # Main Rule Dispatcher
    # -------------------------

    def apply_rules(self, intent, entities):
        """
        Decides which business rule to apply based on detected intent.
        """

        # Greeting intent
        if intent == "greet":
            return self.greet()

        # User typed only an order ID
        if intent == "provide_order_id":
            return self.track_order(entities.get("order_id"))

        # Normal intents
        if intent == "track_order":
            return self.track_order(entities.get("order_id"))

        if intent == "return_policy":
            return self.return_policy(entities.get("order_id"))

        if intent == "product_recommendation":
            return self.recommend_product(entities.get("category"))

        # Unknown fallback
        return "Sorry, I could not understand your request. Please try again or ask about orders, returns, or products."
