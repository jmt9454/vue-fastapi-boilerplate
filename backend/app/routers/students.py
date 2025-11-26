from app.routers.router_base import CRUDRouter
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services.student_service import student

# Instantiate the generic router
# This automatically generates all standard CRUD endpoints
student_router = CRUDRouter(
    service=student,
    create_schema=StudentCreate,
    update_schema=StudentUpdate,
    read_schema=StudentResponse,
)

# Export the internal APIRouter so main.py can include it
router = student_router.router

# --- CUSTOM ENDPOINTS ---
# You can still add custom routes to this specific router if needed
# @router.get("/custom-route")
# def my_custom_logic():
#     return {"message": "This is a custom endpoint alongside the generic ones"}