from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import requests
import json

# Load environment variables
load_dotenv()

# App configuration
app = FastAPI(title="Student Portal Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "sql_test")
}

# Ollama configuration
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Pydantic models
class LoginRequest(BaseModel):
    contact_number: str

class ChatRequest(BaseModel):
    message: str
    student_id: int

class StudentData(BaseModel):
    student_id: int
    full_name: str
    contact_number: str
    course: str
    fees_paid: bool

# Database connection helper
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to database"
        )

# Get student information from database
def get_student_by_contact(contact_number: str) -> Optional[Dict[str, Any]]:
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT StudentID, FullName, ContactNumber, Fees, Course
        FROM students
        WHERE ContactNumber = %s
        """
        
        cursor.execute(query, (contact_number,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result:
            # Convert the BIT(1) value to boolean
            result['Fees'] = bool(result['Fees'])
            
            # Map the database field names to our StudentData model names
            return {
                "student_id": result['StudentID'],
                "full_name": result['FullName'],
                "contact_number": str(result['ContactNumber']),
                "course": result['Course'],
                "fees_paid": result['Fees']
            }
        return None
    
    except Error as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# Student cache for storing student data during the session
# In a production app, use a proper session management system
student_cache = {}

# Routes
@app.post("/api/student/login", response_model=StudentData)
async def login(request: LoginRequest):
    student = get_student_by_contact(request.contact_number)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found with the given contact number"
        )
    
    # Store student data in cache for later use
    student_cache[student["student_id"]] = student
    
    return student

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Check if we have student data in cache
    student = student_cache.get(request.student_id)
    
    if not student:
        # If not in cache, try to get from database
        # In a real app, you might want to authenticate this request
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT StudentID, FullName, ContactNumber, Fees, Course
            FROM students
            WHERE StudentID = %s
            """
            
            cursor.execute(query, (request.student_id,))
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if result:
                # Convert the BIT(1) value to boolean
                result['Fees'] = bool(result['Fees'])
                
                student = {
                    "student_id": result['StudentID'],
                    "full_name": result['FullName'],
                    "contact_number": str(result['ContactNumber']),
                    "course": result['Course'],
                    "fees_paid": result['Fees']
                }
                student_cache[student["student_id"]] = student
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student not found"
                )
        
        except Error as e:
            print(f"Database error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    
    # Prepare context for the LLM
    system_prompt = f"""
    You are a helpful assistant for a student portal. You have access to the following information about the student:
    
    Student ID: {student['student_id']}
    Name: {student['full_name']}
    Course: {student['course']}
    Fees Status: {'Paid' if student['fees_paid'] else 'Unpaid'}
    
    You should help the student with course information, fee status, and general inquiries.
    If they ask about unpaid fees, remind them gently about making payments.
    If they ask about their course, provide encouragement and general information.
    Do not make up specific details not included in the student data.
    """
    
    try:
        # Call Ollama API with the correct format
        response = requests.post(
            f"{OLLAMA_API_URL}/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"{system_prompt}\n\nUser: {request.message}\nAssistant:",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Ollama API error: {response.text}")
            raise Exception(f"Ollama API returned status code {response.status_code}")
            
        response_data = response.json()
        # Ollama's response format has a 'response' field
        llm_response = response_data.get('response', '')
        
        return {"response": llm_response}
    
    except requests.exceptions.RequestException as e:
        print(f"Ollama API connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to Ollama service. Make sure Ollama is running."
        )
    except Exception as e:
        print(f"LLM API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error communicating with Ollama service"
        )

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint to serve the HTML file
@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)