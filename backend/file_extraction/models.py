from sqlalchemy import Column, Integer, String, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.basemodel import BaseModel

class RawFile(BaseModel):
    __tablename__ = "raw_files"


    # Primary Key for the raw file record
    id = Column(Integer, primary_key=True, index=True)
    
    # User ID who uploaded the file
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The original file name
    filename = Column(String, nullable=False)
    
    # The content of the file (binary data for raw file storage)
    file_data = Column(LargeBinary, nullable=False)
    

    # Relationship with FileExtraction
    file_extraction = relationship("FileExtraction", back_populates="raw_file", uselist=False)
    user = relationship("User", back_populates="raw_file")

class FileExtraction(BaseModel):
    __tablename__ = "file_extraction"

    # Primary Key for the file extraction record
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key for the raw file uploaded
    file_id = Column(Integer, ForeignKey("raw_files.id"), nullable=False)
    
    # User ID who uploaded the file (optional as you can link this through RawFile)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The extracted data from the file (could be text, structured JSON, etc.)
    extracted_data = Column(Text, nullable=True)
    
    # Relationship to RawFile
    raw_file = relationship("RawFile", back_populates="file_extraction")
