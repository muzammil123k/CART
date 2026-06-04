from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import base # Assuming you export Base from database.py

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255)) # Store hashed passwords here
    created_at = Column(TIMESTAMP, server_default=func.now())
    carts = relationship("Cart", back_populates="user")


class Category(base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    products = relationship("Product", back_populates="category")


class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(255), index=True)
    price = Column(DECIMAL(10, 2))
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")


class Cart(base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(50), default="active") # e.g., active, abandoned, completed
    coupon = Column(String(50), nullable=True)
    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price_at_addition = Column(DECIMAL(10, 2))
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")