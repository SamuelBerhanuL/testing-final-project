# shop_logic.py

class Order:
    VALID_STATES = ["cart", "placed", "shipped", "delivered"]

    def __init__(self):
        self.state = "cart"
        self.items = []

    def add_item(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append(price)

    def calculate_total(self, is_student=False, has_coupon=False):
        """
        Decision Table Logic:
        - Student gets 10% off
        - Coupon gets $5 off (applied after student discount)
        - Boundary Value Logic: Free shipping if total is exactly >= $50
        """
        subtotal = sum(self.items)
        
        if is_student:
            subtotal *= 0.90
            
        if has_coupon:
            subtotal -= 5.0
            
        subtotal = max(0.0, subtotal) # Prevent negative total
        
        # Shipping boundary condition
        shipping = 0.0 if subtotal >= 50.0 else 10.0
        
        return round(subtotal + shipping, 2)

    def transition_state(self, new_state):
        """
        State Transition Logic:
        cart -> placed -> shipped -> delivered
        """
        if self.state == "cart" and new_state == "placed":
            self.state = "placed"
        elif self.state == "placed" and new_state == "shipped":
            self.state = "shipped"
        elif self.state == "shipped" and new_state == "delivered":
            self.state = "delivered"
        else:
            raise ValueError(f"Invalid transition from {self.state} to {new_state}")
