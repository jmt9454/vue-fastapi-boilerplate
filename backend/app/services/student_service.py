from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

# --- READ ---
def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

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

# --- UPDATE (New) ---
def update_student(db: Session, student_id: int, student_data: StudentUpdate):
    # 1. Get the existing student
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    # 2. If not found, return None (Router handles the 404)
    if not db_student:
        return None
    
    # 3. Update only the fields that were sent
    # exclude_unset=True means "don't update fields that weren't in the JSON"
    update_data = student_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_student, key, value)

    # 4. Commit and Refresh
    db.commit()
    db.refresh(db_student)
    return db_student

# --- DELETE (New) ---
def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if not db_student:
        return None
        
    db.delete(db_student)
    db.commit()
    return db_student