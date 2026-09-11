# tests/test_shop_logic.py
import pytest
from shop_logic import Order

# --- 1. Equivalence Partitioning (EP) ---
def test_add_item_valid():
    order = Order()
    order.add_item(10.0)
    assert len(order.items) == 1

def test_add_item_invalid_negative():
    order = Order()
    with pytest.raises(ValueError):
        order.add_item(-5.0)

# --- 2. Boundary Value Analysis (BVA) ---
def test_shipping_boundary_below():
    order = Order()
    order.add_item(49.99)
    assert order.calculate_total() == 59.99 # $10 shipping added

def test_shipping_boundary_exact():
    order = Order()
    order.add_item(50.00)
    assert order.calculate_total() == 50.00 # Free shipping

def test_shipping_boundary_above():
    order = Order()
    order.add_item(50.01)
    assert order.calculate_total() == 50.01 # Free shipping

# --- 3. Decision Tables ---
def test_discount_no_student_no_coupon():
    order = Order()
    order.add_item(100.0)
    assert order.calculate_total(is_student=False, has_coupon=False) == 100.0

def test_discount_student_no_coupon():
    order = Order()
    order.add_item(100.0)
    assert order.calculate_total(is_student=True, has_coupon=False) == 90.0

def test_discount_no_student_with_coupon():
    order = Order()
    order.add_item(100.0)
    assert order.calculate_total(is_student=False, has_coupon=True) == 95.0

def test_discount_student_and_coupon():
    order = Order()
    order.add_item(100.0)
    # 10% off 100 = 90. Then $5 off = 85. Free shipping applies.
    assert order.calculate_total(is_student=True, has_coupon=True) == 85.0

# --- 4. State Transitions ---
def test_valid_state_transitions():
    order = Order()
    assert order.state == "cart"
    order.transition_state("placed")
    assert order.state == "placed"
    order.transition_state("shipped")
    assert order.state == "shipped"

def test_invalid_state_transition():
    order = Order()
    with pytest.raises(ValueError):
        order.transition_state("shipped") # Cannot jump from cart to shipped
