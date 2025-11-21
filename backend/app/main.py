from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- CORS ---
origins = os.getenv("ALLOW_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTER ROUTERS ---
app.include_router(students.router, prefix="/students", tags=["Students"])

@app.get("/")
def read_root():
    return {"message": "Backend is running!", "status": "success"}
