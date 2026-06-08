from fastapi import FastAPI , Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import List
import schemas
import database
import models
import exceptions
import logging

file_handler = logging.FileHandler("server_activity.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger("cart_api")
logger.setLevel(logging.INFO) 
logger.handlers.clear()
logger.addHandler(file_handler)
logger.propagate = False
for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    uvicorn_logger = logging.getLogger(logger_name)
    uvicorn_logger.handlers.clear() 
    uvicorn_logger.addHandler(file_handler)
    uvicorn_logger.propagate = False
app = FastAPI()

models.base.metadata.create_all(bind=database.engine)

@app.exception_handler(exceptions.CartNotFoundError)
async def cart_not_found_handler(request, exc: exceptions.CartNotFoundError):
    logger.warning(exc.message)
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "detail": exc.message},
    )

@app.exception_handler(exceptions.InvalidCartStateError)
async def invalid_cart_state_handler(request, exc: exceptions.InvalidCartStateError):
    logger.warning(f"Business logic error on cart {exc.cart_id}: {exc.reason}")
    return JSONResponse(
        status_code=400,
        content={"error": "Bad Request", "detail": exc.message},
    )

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
    db_item = models.CartItem(
        cart_id=cart_id,
        product_id=item_in.product_id,
        quantity=item_in.quantity,
        price_at_addition=product.price  # Safe now, because we know product exists!
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/carts/{cart_id}/items/{item_id}")
def remove_item_from_cart(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
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
    items_count = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).count()
    if items_count == 0:
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