import enum
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from api.deps import get_current_user

from core.database import get_db
from core.security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from models.users import User, UserRole
from schemas.user import UserCreate, UserResponse, Token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to register: {user_data.email}")
    
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pw = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw, 
        full_name=user_data.full_name,
        role=user_data.role.value if isinstance(user_data.role, enum.Enum) else user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={
            "sub": user.email, 
            "role": str(user.role), 
            "user_id": str(user.id)
        }, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def get_user_progress_and_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns the current user's profile completion status.
    Checks all JSONB columns to build a complete progress map for the frontend.
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Safely extract all JSONB column data
    academic = getattr(user, 'academic_data', {}) or {}
    aptitude = getattr(user, 'apti_data', {}) or {}
    personality = getattr(user, 'personality_data', {}) or {}
    lifestyle = getattr(user, 'lifestyle_data', {}) or {}
    financial = getattr(user, 'financial_data', {}) or {}
    passion = getattr(user, 'passion_strength_data', {}) or {}
    aspiration = getattr(user, 'aspiration_data', {}) or {}
    interests = getattr(user, 'career_interest_data', {}) or {}
    
    # Send a comprehensive progress map and raw data to the Flutter app
    return {
        "user_id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "progress": {
            "profile_done": len(academic) > 0, 
            "basic_assessment_done": len(academic) > 0,
            "personality_done": len(personality) > 0,
            "passion_done": len(passion) > 0,
            "lifestyle_done": len(lifestyle) > 0,
            "financial_done": len(financial) > 0,
            "family_link_done": len(financial) > 0,
            "interests_done": len(interests) > 0,
            "dreams_done": len(aspiration) > 0,
            "aptitude_done": len(aptitude) > 0,
            "academic_done": len(academic) > 0
        },
        "apti_data": aptitude,            
        "personality_data": personality,  
        "academic_data": academic         
    }