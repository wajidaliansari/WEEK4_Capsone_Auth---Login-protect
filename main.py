from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI(title="Auth - Login & Protect API")


security = HTTPBearer()


class UserCredentials(BaseModel):
    email: str
    password: str


@app.post("/auth/signup", status_code=201)
def signup(user: UserCredentials):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/auth/login", status_code=200)
def login(user: UserCredentials):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return response
    except Exception as e:
         
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")


def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Supabase se token verify karwayen
        user_response = supabase.auth.get_user(token)
        return user_response
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/protected/profile")
def get_profile(current_user = Depends(verify_access_token)):
    return {
        "message": "Welcome! You have successfully accessed the protected route.",
        "user_data": current_user
    }