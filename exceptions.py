class CartAPIException(Exception):
    """Base exception for the Cart API so we can catch them all if needed."""
    pass

class CartNotFoundError(CartAPIException):
    def __init__(self, cart_id: int):
        self.cart_id = cart_id
        self.message = f"Cart with ID {cart_id} was not found."
        super().__init__(self.message)

class InvalidCartStateError(CartAPIException):
    def __init__(self, cart_id: int, reason: str):
        self.cart_id = cart_id
        self.reason = reason
        self.message = f"Cannot process cart {cart_id}: {reason}"
        super().__init__(self.message)