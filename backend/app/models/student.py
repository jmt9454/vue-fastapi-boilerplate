from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    major = Column(String)
    gpa = Column(String, nullable=True) # Adding a field to show flexibility