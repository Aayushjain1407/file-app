from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from io import BytesIO
from unstructured.partition.pdf import partition_pdf

def create_raw_file(db: Session, file_data: bytes, user_id: int, filename: str):
    # Save the raw file to the database
    db_raw_file = models.RawFile(
        user_id=user_id,
        filename=filename,
        file_data=file_data,
        # created_at=datetime.utcnow()
    )
    
    db.add(db_raw_file)
    db.commit()
    db.refresh(db_raw_file)
    return db_raw_file

def create_file_extraction(db: Session, file_id: int, user_id: int, extracted_data: str):
    # Save the extracted data to the database
    db_extraction = models.FileExtraction(
        file_id=file_id,
        user_id=user_id,
        extracted_data=extracted_data,
        created_at=datetime.utcnow()
    )
    db.add(db_extraction)
    db.commit()
    db.refresh(db_extraction)
    return db_extraction

def extract_text_from_pdf(file_data: bytes):
    # Use unstructured.io to extract text from the PDF file
    document = partition_pdf(BytesIO(file_data))
    extracted_text = "\n".join([page.text for page in document])
    return extracted_text
