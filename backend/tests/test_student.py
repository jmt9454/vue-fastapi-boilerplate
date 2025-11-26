from tests.generic_test_base import CRUDApiTestBase
from tests.factories import StudentCreateFactory, StudentUpdateFactory

class TestStudentRoutes(CRUDApiTestBase):
    """
    Runs all CRUD tests for the /students endpoint 
    using the Student factories.
    """
    url_prefix = "/students"
    create_factory = StudentCreateFactory
    update_factory = StudentUpdateFactory