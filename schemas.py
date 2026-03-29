from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    blood_group: str
    city: Optional[str] = None
    phone: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_available: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class UserResponse(UserBase):
    id: int
    is_available: bool
    last_donation_date: Optional[datetime] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

class DonationCreate(BaseModel):
    location: Optional[str] = None

class DonationResponse(BaseModel):
    id: int
    donation_date: datetime
    location: Optional[str] = None

    class Config:
        from_attributes = True

class EmergencyAlertCreate(BaseModel):
    blood_group: str
    requester_name: str
    location_name: str
    latitude: float
    longitude: float

class EmergencyAlertResponse(EmergencyAlertCreate):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
