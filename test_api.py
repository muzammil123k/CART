from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

def test_create_cart():
    response = client.post("/carts/", json={"user_id": 1})
    if response.status_code != 200:
        print(f"\nFastAPI Validation Error: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data