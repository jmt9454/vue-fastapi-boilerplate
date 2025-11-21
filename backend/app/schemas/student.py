from pydantic import BaseModel
from typing import Optional

# 1. Base Model (Shared properties)
class StudentBase(BaseModel):
    name: str
    major: str
    gpa: Optional[str] = None

# 2. Create Model (What we need to receive to make a student)
class StudentCreate(StudentBase):
    pass

# 3. Update Model (NEW: Everything is optional for updates)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[str] = None

# 4. Response Model (What we send back)
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True