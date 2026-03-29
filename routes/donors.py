from fastapi import APIRouter, Depends, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models, schemas, auth
from models import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/donors", tags=["donors"])

@router.get("/stats")
def get_donor_stats(db: Session = Depends(get_db)):
    total = db.query(models.User).count()
    
    cooldown_threshold = datetime.utcnow() - timedelta(days=90)
    available = db.query(models.User).filter(
        models.User.is_available == True,
        (models.User.last_donation_date == None) | (models.User.last_donation_date < cooldown_threshold)
    ).count()
    
    return {"total_donors": total, "available_now": available}

@router.get("/search", response_model=List[schemas.UserResponse])
def search_donors(blood_group: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Simple search: find available donors with matching blood group
    # Cooldown logic: last_donation_date > 90 days ago or None
    cooldown_threshold = datetime.utcnow() - timedelta(days=90)
    
    donors = db.query(models.User).filter(
        models.User.id != current_user.id, # Don't show me
        models.User.blood_group == blood_group,
        models.User.is_available == True,
        (models.User.last_donation_date == None) | (models.User.last_donation_date < cooldown_threshold)
    ).all()
    
    return donors

@router.put("/status", response_model=schemas.UserResponse)
def update_status(status_update: schemas.UserUpdate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if status_update.is_available is not None:
        current_user.is_available = status_update.is_available
    if status_update.latitude is not None:
        current_user.latitude = status_update.latitude
    if status_update.longitude is not None:
        current_user.longitude = status_update.longitude
    if status_update.lat is not None:
        current_user.lat = status_update.lat
    if status_update.lng is not None:
        current_user.lng = status_update.lng
    if status_update.full_name is not None:
        current_user.full_name = status_update.full_name
        
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/log-donation", response_model=schemas.UserResponse)
def log_donation(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    current_user.last_donation_date = datetime.utcnow()
    current_user.is_available = False # Automatically mark as unavailable after donation
    
    donation = models.DonationHistory(user_id=current_user.id, donation_date=current_user.last_donation_date)
    db.add(donation)
    
    db.commit()
    db.refresh(current_user)
    return current_user
