from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

# --- READ ---
def get_student(db: Session, student_id: int):
    # v2 style: use select() and scalar() for a single result
    statement = select(Student).where(Student.id == student_id)
    return db.scalar(statement)

def get_students(db: Session, skip: int = 0, limit: int = 100):
    # v2 style: use select() and scalars().all() for a list
    statement = select(Student).offset(skip).limit(limit)
    return db.scalars(statement).all()

# --- CREATE ---
def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        name=student.name, 
        major=student.major, 
        gpa=student.gpa
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# --- UPDATE ---
def update_student(db: Session, student_id: int, student_data: StudentUpdate):
    # 1. Get existing student using v2 syntax
    statement = select(Student).where(Student.id == student_id)
    db_student = db.scalar(statement)
    
    # 2. Return None if not found
    if not db_student:
        return None
    
    # 3. Update fields (Pydantic v2 model_dump)
    update_data = student_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_student, key, value)

    # 4. Commit
    db.commit()
    db.refresh(db_student)
    return db_student

# --- DELETE ---
def delete_student(db: Session, student_id: int):
    # 1. Get existing student using v2 syntax
    statement = select(Student).where(Student.id == student_id)
    db_student = db.scalar(statement)
    
    if not db_student:
        return None
        
    # 2. Delete and commit
    db.delete(db_student)
    db.commit()
    return db_student