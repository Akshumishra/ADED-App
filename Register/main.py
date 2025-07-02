import bcrypt
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from urllib.parse import quote_plus
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime

app = FastAPI()

# Enable CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
password = quote_plus("Akshita_9204")  # your MongoDB password
client = MongoClient(f"mongodb+srv://akshitamishra421:{password}@cluster0.3crbjxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["aded_database"]
collection = db["users"]
contact_collection = db["contact_messages"]
history_collection = db["history"]

# Models for request validation
class User(BaseModel):
    fullName: str
    DOB: str
    gender: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Utility to log user activity
def log_user_activity(email, activity):
    history_collection.insert_one({
        "email": email,
        "activity": activity,
        "timestamp": datetime.now()
    })

# Routes
@app.get("/")
def read_root():
    return {"message": "ADED App FastAPI is working!"}

@app.post("/log_activity")
async def log_activity(
    user_email: str = Form(...),
    activity: str = Form(...)
):
    log_user_activity(user_email, activity)
    return {"message": "Activity logged"}


@app.post("/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    fullName: str = Form(...),
    DOB: str = Form(...),
    gender: str = Form(...),
    role: str = Form("user")  # Default to user
):
    if collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(password)
    user_data = {
        "email": email,
        "password": hashed_password,
        "role": role,
        "fullName": fullName,
        "DOB": DOB,
        "gender": gender
    }
    collection.insert_one(user_data)
    log_user_activity(email, "User registered")
    return {"message": "User registered successfully!"}

@app.post("/login")
async def login_user(user: UserLogin):
    user_in_db = collection.find_one({"email": user.email})
    if not user_in_db:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not pwd_context.verify(user.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    log_user_activity(user.email, "User logged in")
    return {"message": "Login successful", "user_id": str(user_in_db["_id"]), "fullName": user_in_db["fullName"]}

@app.post("/contact")
async def submit_contact(contact: ContactMessage):
    try:
        result = contact_collection.insert_one(contact.dict())
        log_user_activity(contact.email, "Submitted help form")
        return {"message": "Message received successfully!", "id": str(result.inserted_id)}
    except Exception as e:
        print("CONTACT ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to submit message")

@app.post("/admin/view_user_activity")
async def view_user_activity(
    admin_email: str = Form(...),
    admin_password: str = Form(...)
):
    admin = collection.find_one({"email": admin_email})
    if not admin or not pwd_context.verify(admin_password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    if admin.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden. Admins only.")

    activities = list(history_collection.find().sort("timestamp", -1))
    for act in activities:
        act["_id"] = str(act["_id"])
        act["timestamp"] = act["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return {"activities": activities}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
