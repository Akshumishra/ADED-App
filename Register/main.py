from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

app = FastAPI()

# CORS for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
password = quote_plus("Akshita_9204")
client = MongoClient(f"mongodb+srv://akshitamishra421:{password}@cluster0.3crbjxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["aded_database"]
users_col = db["users"]
contact_col = db["contact_messages"]
history_col = db["history"]

# Pydantic models
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

# Utility: log user activity
def log_user_activity(email: str, activity: str):
    history_col.insert_one({
        "email": email,
        "activity": activity,
        "timestamp": datetime.utcnow()
    })

# Routes
@app.get("/")
def home():
    return {"message": "ADED FastAPI backend working!"}

@app.post("/register")
async def register(user: User):
    if users_col.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    user_data["role"] = "user"
    users_col.insert_one(user_data)
    log_user_activity(user.email, "User registered")
    return {"message": "User registered successfully!"}

@app.post("/login")
async def login(user: UserLogin):
    user_in_db = users_col.find_one({"email": user.email})
    if not user_in_db or not pwd_context.verify(user.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    log_user_activity(user.email, "User logged in")
    return {
        "message": "Login successful",
        "user_id": str(user_in_db["_id"]),
        "fullName": user_in_db["fullName"]
    }

@app.post("/contact")
async def submit_contact(message: ContactMessage):
    result = contact_col.insert_one(message.dict())
    log_user_activity(message.email, "Submitted help form")
    return {"message": "Message received successfully!", "id": str(result.inserted_id)}

@app.post("/log_activity")
async def log_activity(user_email: EmailStr, activity: str):
    log_user_activity(user_email, activity)
    return {"message": "Activity logged successfully."}

@app.post("/admin/view_user_activity")
async def view_user_activity(
    admin_email: str = Form(...),
    admin_password: str = Form(...)
):
    admin = users_col.find_one({"email": admin_email})
    if not admin or not pwd_context.verify(admin_password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    if admin.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden. Admins only.")

    activities = list(history_col.find().sort("timestamp", -1))
    for act in activities:
        act["_id"] = str(act["_id"])
        act["timestamp"] = act["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return {"activities": activities}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
