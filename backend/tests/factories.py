from polyfactory.factories.pydantic_factory import ModelFactory
from app.schemas.student import StudentCreate, StudentUpdate

# Automatically generates random data matching the StudentCreate schema
class StudentCreateFactory(ModelFactory[StudentCreate]):
    __model__ = StudentCreate

# Automatically generates random data matching the StudentUpdate schema
class StudentUpdateFactory(ModelFactory[StudentUpdate]):
    __model__ = StudentUpdate