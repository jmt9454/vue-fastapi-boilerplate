from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.services import student_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. GET ALL
@router.get("/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return student_service.get_students(db, skip=skip, limit=limit)

# 2. GET ONE (New)
@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_service.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# 3. CREATE
@router.post("/", response_model=StudentResponse)
def create_new_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db=db, student=student)

# 4. UPDATE (New)
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    updated_student = student_service.update_student(db=db, student_id=student_id, student_data=student)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

# 5. DELETE (New)
@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = student_service.delete_student(db=db, student_id=student_id)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted_student