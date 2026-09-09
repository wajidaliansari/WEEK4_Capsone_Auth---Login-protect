import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv

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