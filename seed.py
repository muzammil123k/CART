import logging
from database import SessionLocal
import models


logger = logging.getLogger("db_seeder")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def seed_database():
    logger.info("Starting database seeding process...")
    db = SessionLocal()
    
    try:

        if db.query(models.User).first():
            logger.warning("Database is already seeded. Aborting to prevent duplicates.")
            return

    
        logger.info("Inserting users...")
        user1 = models.User(name="Alice Tech", email="alice@example.com", password="hashed_pass_1")
        user2 = models.User(name="Bob Builder", email="bob@example.com", password="hashed_pass_2")
        db.add_all([user1, user2])

        logger.info("Inserting categories...")
        cat_electronics = models.Category(name="Electronics", description="Gadgets and devices")
        cat_clothing = models.Category(name="Clothing", description="Apparel and accessories")
        db.add_all([cat_electronics, cat_clothing])
        
        db.commit() 

        # 3. Create Dummy Products
        logger.info("Inserting products...")
        prod1 = models.Product(
            name="Mechanical Keyboard", price=89.99, stock=50, category_id=cat_electronics.id
        )
        prod2 = models.Product(
            name="Wireless Mouse", price=25.50, stock=100, category_id=cat_electronics.id
        )
        prod3 = models.Product(
            name="Cotton T-Shirt", price=15.00, stock=200, category_id=cat_clothing.id
        )
        db.add_all([prod1, prod2, prod3])

        db.commit()
        logger.info("Database successfully seeded with dummy data!")

    except Exception as e:
        logger.error(f"Seeding failed due to an error: {str(e)}")
        db.rollback() 
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()