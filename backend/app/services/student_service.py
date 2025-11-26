from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.crud_base import CRUDBase

class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    # You can add specific custom methods here if needed in the future
    # def get_by_name(self, db: Session, name: str): ...
    pass


student = CRUDStudent(Student)