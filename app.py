from fastapi import FastAPI , Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import List
import schemas
import database
import models
import logging


logger = logging.getLogger("cart_api")
logger.setLevel(logging.INFO) 

console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
app = FastAPI()


models.base.metadata.create_all(bind=database.engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/carts/", response_model=schemas.CartResponse)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db)):
    db_cart = models.Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@app.post("/carts/{cart_id}/items/", response_model=schemas.CartItemResponse)
def add_item_to_cart(cart_id: int, item_in: schemas.CartItemCreate, db: Session = Depends(get_db)):

    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    product = db.query(models.Product).filter(models.Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    item_data = item_in.model_dump()
    item_data["cart_id"] = cart_id 
    new_cart_item = models.CartItem(**item_data)
    
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    
    return new_cart_item

@app.delete("/carts/{cart_id}/items/{item_id}")
def remove_item_from_cart(cart_id: int, item_id: int, db: Session = Depends(get_db)):

    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.cart_id == cart_id
    ).first()
   
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in this cart")
        
    db.delete(item)
    db.commit()
    
    return {"detail": f"Item {item_id} successfully removed from cart {cart_id}"}


@app.post("/carts/{cart_id}/checkout", response_model=schemas.CartResponse)
def checkout_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    if cart.status == "completed":
        raise HTTPException(status_code=400, detail="Cart is already checked out")
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cannot checkout an empty cart")
    cart.status = "completed"
    db.commit()
    db.refresh(cart)
    
    return cart

@app.delete("/carts/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(cart)
    db.commit()
    
    return {"detail": f"Cart {cart_id} and all its items have been permanently deleted"}