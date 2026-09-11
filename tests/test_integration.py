# tests/test_integration.py
import pytest
from app import app, current_order
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset the global order state before each test
        current_order.state = "cart"
        current_order.items = []
        yield client
def test_integration_add_item_route(client):
    """Integration: Tests if the /add web route successfully updates the Order object"""
    # Send a POST request simulating a user typing 15.50 into the form
    response = client.post('/add', data={'price': '15.50'})
    
    # It should redirect back to the home page (status code 302)
    assert response.status_code == 302
    
    # Check if the core logic was actually updated
    assert len(current_order.items) == 1
    assert current_order.items[0] == 15.50