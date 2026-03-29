import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import SessionLocal, User, Base, engine
from auth import get_password_hash
from datetime import datetime, timedelta

def seed():
    # Only seed if users table is empty
    db = SessionLocal()
    if db.query(User).count() > 0:
        print("Database already has data. Skipping seed.")
        return

    print("Seeding database...")
    
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    
    for i, bg in enumerate(blood_groups):
        user = User(
            full_name=f"Donor {bg}",
            email=f"donor{i}@example.com",
            hashed_password=get_password_hash("password123"),
            blood_group=bg,
            city=cities[i % len(cities)],
            phone=f"+91 98765 4321{i}",
            is_available=True,
            lat=17.385 + (i * 0.01), # Dispersion around Hyderabad
            lng=78.486 + (i * 0.01)
        )
        db.add(user)
    
    db.commit()
    print("Seeding complete! 8 donors added.")
    db.close()

if __name__ == "__main__":
    seed()
