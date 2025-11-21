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

@app.api_route("/god_endpoint", methods=["GET", "POST", "DELETE"])
async def do_stuff(request: Request):
    """
    The 'God Function'. It does everything.
    """
    global last_user
    
    # ❌ BAD: Parsing raw JSON without Pydantic validation
    try:
        data = await request.json()
    except:
        data = {}

    # ❌ BAD: Hardcoded database path & Direct connection inside route
    # This creates a new connection for every request (slow!)
    con = sqlite3.connect("production_database.db")
    cur = con.cursor()

    # ❌ BAD: Blocking I/O in an async function
    # This freezes the ENTIRE server for 2 seconds. No one else can connect.
    time.sleep(2)

    action = request.query_params.get("action")

    if action == "login":
        username = data.get("username")
        password = data.get("password")
        
        # ❌ CRITICAL SECURITY FLAW: SQL Injection Vulnerability
        # A user can send password="' OR '1'='1" to login as admin
        query = f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'"
        print(f"Executing: {query}") # ❌ BAD: Logging secrets to console
        
        res = cur.execute(query).fetchone()
        if res:
            return {"status": "Logged in", "user_data": res}
        else:
            return "Fail" # ❌ BAD: Inconsistent return types (Dict vs String)

    elif action == "create_student":
        name = data.get("name")
        # ❌ BAD: Manual validation logic mixed with DB logic
        if len(name) < 2:
            return {"error": "Name too short"}
            
        # ❌ BAD: Creating tables on the fly inside a route
        cur.execute("CREATE TABLE IF NOT EXISTS students (id int, name text)")
        
        # ❌ BAD: Manual ID generation (Subject to race conditions)
        last_id = cur.execute("SELECT MAX(id) FROM students").fetchone()[0] or 0
        new_id = last_id + 1
        
        cur.execute(f"INSERT INTO students VALUES ({new_id}, '{name}')")
        con.commit()
        
        last_user = name # Setting global state
        return {"msg": "Created"}

    elif action == "nuke_db":
        # ❌ BAD: Dangerous logic exposed on public endpoint without auth
        cur.execute("DROP TABLE students")
        return {"msg": "Bye bye data"}

    con.close() # ❌ BAD: If an error happens above, this never runs (Connection Leak)
    
    return {"info": "I don't know what you want"}