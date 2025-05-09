# Student Portal with AI Assistant

A FastAPI-based student portal backend with an AI-powered chat assistant using Ollama. The system allows students to log in using their contact number and interact with an AI assistant that has access to their personal information.

## Features

- Student authentication via contact number
- Personal student information display
- AI-powered chat assistant using Ollama
- Real-time chat interface
- MySQL database integration
- CORS support for frontend integration

## Prerequisites

- Python 3.8+
- MySQL Server
- Ollama (Local LLM server)
- Node.js (for development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sql
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install fastapi uvicorn python-dotenv mysql-connector-python requests
```

4. Create a `.env` file:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=sql_test
OLLAMA_API_URL=http://localhost:11434/api
OLLAMA_MODEL=your_model_name
```

5. Set up the MySQL database:
```sql
CREATE DATABASE sql_test;
USE sql_test;

CREATE TABLE students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(100) NOT NULL,
    ContactNumber VARCHAR(15) UNIQUE NOT NULL,
    Course VARCHAR(50) NOT NULL,
    Fees BIT(1) DEFAULT 0
);
```

## Running the Application

1. Start MySQL server:
```bash
sudo systemctl start mysql
```

2. Start Ollama server:
```bash
ollama serve
```

3. Run the FastAPI application:
```bash
python app.py
```

The application will be available at `http://localhost:8000`

## Project Structure

```
sql/
├── app.py              # Main FastAPI application
├── static/             # Static files directory
│   └── index.html     # Frontend interface
├── .env               # Environment variables
└── README.md          # Project documentation
```

## API Endpoints

- `POST /api/student/login` - Student login with contact number
- `POST /api/chat` - AI chat interaction
- `GET /` - Serves the frontend interface

## Frontend

The frontend is built with vanilla JavaScript and provides:
- Login form
- Student information display
- Real-time chat interface with AI assistant

## Security Considerations

- This is a development setup and needs additional security measures for production
- The CORS policy is set to allow all origins (`*`)
- Implement proper authentication and session management for production
- Secure the database connection and API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]