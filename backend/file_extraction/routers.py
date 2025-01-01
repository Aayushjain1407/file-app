from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from core.security import get_current_user
from . import models, schemas, services
from users.models import User
from db.session import get_db

router = APIRouter()

# Route to upload files and extract data
@router.post("/upload-file/", response_model=schemas.FileExtractionCreate)
async def upload_file(
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),  # File parameter comes after
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Save the raw file in the database
        raw_file = services.create_raw_file(
            db=db,
            file_data=file_content,
            user_id=user_id,
            filename=file.filename
        )
        
        # Extract text from PDF
        extracted_text = services.extract_text_from_pdf(file_content)
        
        # Create file extraction record
        extracted_data = services.create_file_extraction(
            db=db,
            file_id=raw_file.id,
            user_id=user_id,
            extracted_data=extracted_text
        )
        
        return extracted_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route to fetch extracted data by user ID
@router.get("/extracted-data/{user_id}", response_model=List[schemas.FileExtraction])
async def get_extracted_data(user_id: int, db: Session = Depends(get_db)):
    try:
        extracted_data = db.query(models.FileExtraction)\
            .filter(models.FileExtraction.user_id == user_id)\
            .all()
            
        if not extracted_data:
            raise HTTPException(status_code=404, detail=f"No extracted data found for user {user_id}")
            
        return extracted_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/extraction/{file_id}", response_model=schemas.FileExtraction)
async def get_extraction(file_id: int, db: Session = Depends(get_db)):
    try:
        extraction = db.query(models.FileExtraction)\
            .filter(models.FileExtraction.file_id == file_id)\
            .first()
            
        if not extraction:
            raise HTTPException(status_code=404, detail=f"No extraction found for file {file_id}")
            
        return extraction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    