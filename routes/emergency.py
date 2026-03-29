from fastapi import APIRouter, Depends, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models, schemas, auth
from models import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/emergency", tags=["emergency"])

@router.post("/alert", response_model=schemas.EmergencyAlertResponse)
def create_alert(alert: schemas.EmergencyAlertCreate, db: Session = Depends(get_db)):
    new_alert = models.EmergencyAlert(**alert.dict())
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

@router.get("/alerts", response_model=List[schemas.EmergencyAlertResponse])
def get_active_alerts(db: Session = Depends(get_db)):
    return db.query(models.EmergencyAlert).filter(models.EmergencyAlert.is_active == True).all()

@router.put("/alert/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.EmergencyAlert).filter(models.EmergencyAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_active = False
    db.commit()
    return {"message": "Alert resolved"}
