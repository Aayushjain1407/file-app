from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RawFileBase(BaseModel):
    user_id: int
    filename: str
    created_at: Optional[datetime] = None

class RawFileCreate(RawFileBase):
    file_data: bytes  # To handle file upload as binary

class FileExtractionBase(BaseModel):
    user_id: int
    extracted_data: Optional[str] = None
    created_at: Optional[datetime] = None

class FileExtractionCreate(FileExtractionBase):
    file_id: int

# Models used for response
class RawFile(RawFileBase):
    id: int


    class Config:
        orm_mode = True

class FileExtraction(FileExtractionBase):
    id: int
    file_id: int

    class Config:
        orm_mode = True
