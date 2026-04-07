import os
import logging
import psycopg2
import json
from psycopg2.extras import Json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from api.deps import get_current_user
from models.users import User

# 1. Router Setup
router = APIRouter(prefix="/api/v1/assessments", tags=["Submission"])

# 2. Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
logger = logging.getLogger(__name__)

# 3. The Mapping Logic
COLUMN_MAPPING = {
    "profile": "profile_data",
    "academic": "academic_data",
    "aptitude": "apti_data",
    "personality": "personality_data",
    "lifestyle": "lifestyle_data",
    "financial": "financial_data",
    "passion": "passion_strength_data",
    "aspiration": "aspiration_data",
    "interests": "career_interest_data"
}

# --- SCHEMAS ---

class UniversalSubmission(BaseModel):
    module_key: str  
    payload: Dict[str, Any]  

class SaveProgressBody(BaseModel):
    test_key: str  # e.g. "aptitude"
    session_questions: List[Any]  
    answers: Dict[str, Any]  
    current_index: int

# --- ENDPOINTS ---

@router.post("/submit-generic")
async def submit_generic_assessment(
    submission: UniversalSubmission,
    current_user: User = Depends(get_current_user)
):
    """
    Universal sync endpoint: identifies the user via auth token and persists data to JSONB.
    """
    key = submission.module_key.lower()
    target_column = COLUMN_MAPPING.get(key)
    
    if not target_column:
        logger.warning(f"Submission attempt for unsupported module: {key}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid module key: '{key}'. Supported: {list(COLUMN_MAPPING.keys())}"
        )

    query = f"""
    UPDATE users 
    SET {target_column} = %s, 
        updated_at = NOW() 
    WHERE id = %s;
    """

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (Json(submission.payload), str(current_user.id)))
            conn.commit()
            
        logger.info(f"Successfully synced {key} for User: {current_user.id}")
        return {
            "status": "success",
            "message": f"Module '{key}' successfully saved.",
            "module_synced": key
        }
    except Exception as e:
        logger.error(f"Database Error during {key} submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Data persistence failed.")


@router.patch("/save-progress")
async def save_test_progress(
    body: SaveProgressBody,
    current_user: User = Depends(get_current_user)
):
    """
    Saves mid-test progress into the user's JSONB column using the || operator.
    """
    target_col = COLUMN_MAPPING.get(body.test_key.lower())
    if not target_col:
        raise HTTPException(status_code=400, detail=f"Unsupported test_key: {body.test_key}")

    progress_payload = {
        "_status": "in_progress",
        "_session_questions": body.session_questions,
        "_answers": body.answers,
        "_current_index": body.current_index,
    }

    query = f"""
    UPDATE users
    SET {target_col} = COALESCE({target_col}, '{{}}'::jsonb) || %s::jsonb,
        updated_at = NOW()
    WHERE id = %s;
    """
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (json.dumps(progress_payload), str(current_user.id)))
            conn.commit()
        return {"status": "saved", "current_index": body.current_index}
    except Exception as e:
        logger.error(f"save-progress error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save progress.")


@router.get("/progress/{test_key}")
async def get_test_progress(
    test_key: str, 
    current_user: User = Depends(get_current_user)
):
    """
    Returns in-progress test state so the frontend can resume.
    """
    target_col = COLUMN_MAPPING.get(test_key.lower())
    if not target_col:
        raise HTTPException(status_code=400, detail=f"Unsupported test_key: {test_key}")

    query = f"SELECT {target_col} FROM users WHERE id = %s;"
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (str(current_user.id),))
                row = cur.fetchone()

        if not row or not row[0]:
            return {"in_progress": False}

        col_data = row[0] if isinstance(row[0], dict) else json.loads(row[0])
        if col_data.get("_status") == "in_progress":
            return {
                "in_progress": True,
                "session_questions": col_data.get("_session_questions", []),
                "answers": col_data.get("_answers", {}),
                "current_index": col_data.get("_current_index", 0),
            }
        return {"in_progress": False}
    except Exception as e:
        logger.error(f"get-progress error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch progress.")