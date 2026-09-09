import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import HTTPException

# Load environment variables
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Check if keys exist
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found in .env file")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI app (Yahi line miss ho gayi thi)
app = FastAPI(title="Secure API with Supabase Auth")

@app.on_event("startup")
async def startup_event():
    print("Server running and connected to Supabase")

@app.get("/")
def root():
    return {"status": "Server is up and running!"}

class UserCredentials(BaseModel):
    email: str
    password: str

# 2. Sign Up Route
@app.post("/auth/signup", status_code=201)
def signup(user: UserCredentials):
    try:
        # Supabase mein user register karein
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return res
    except Exception as e:
        # Agar user already exist karta hai ya koi error hai
        raise HTTPException(status_code=400, detail=str(e))

# 3. Log In Route
@app.post("/auth/login", status_code=200)
def login(user: UserCredentials):
    try:
        # Supabase mein login karein
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return res
    except Exception as e:
        # Agar password galat hai toh 401 error return karein
        raise HTTPException(status_code=401, detail="Invalid login credentials")