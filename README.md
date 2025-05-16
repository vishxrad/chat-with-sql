# Chat with SQL AI Assistant

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


## Project Structure

```
sql/
├── app.py              # Main FastAPI application
├── static/             # Static files directory
│   └── index.html     # Frontend interface
├── .env               # Environment variables
└── README.md          # Project documentation
```

## Docker Container

1. Pull image:
   ```bash
   sudo docker pull visharxd/chat-with-sql:latest
   ```

2. Make a container of the image:
    ```bash
    sudo docker run -d --name my-sql-chatbot -p 8000:8000 visharxd/chat-with-sql:latest
    ```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vishxrad/chat-with-sql.git
cd chat-with-sql
```

2. Set up a virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies with uv:
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install fastapi "uvicorn" python-dotenv mysql-connector-python requests

# Generate requirements.txt (optional)
uv pip freeze > requirements.txt
```

4. Create a `.env` file:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=student_db
OLLAMA_API_URL=http://localhost:11434/api
OLLAMA_MODEL=llama3.2
```

## Database Setup

1. Log into MySQL:
```bash
mysql -u root -p
```

2. Create and populate the database:
```sql
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE students (
    StudentID INT NOT NULL PRIMARY KEY,
    FullName VARCHAR(100),
    ContactNumber BIGINT,
    Fees BIT(1) NOT NULL, 
    Course VARCHAR(50)
);

-- Insert sample data
INSERT INTO students VALUES 
(1001, 'John Smith', 9876543210, b'1', 'Computer Science'),
(1002, 'Sarah Johnson', 9876543211, b'0', 'Data Science'),
(1003, 'Michael Chen', 9876543212, b'1', 'Cybersecurity');
```

## Ollama Setup

### Linux Installation
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

### Download Required Model
```bash
ollama pull llama3
```

### Test Ollama
```bash
curl -X POST http://localhost:11434/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## Running the Application

1. Start MySQL server:
```bash
sudo systemctl start mysql
```

2. Ensure Ollama is running:
```bash
ollama serve
```

3. Run the FastAPI application:
```bash
python app.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/student/login` - Student login with contact number
- `POST /api/chat` - AI chat interaction
- `GET /` - Serves the frontend interface

## Production Deployment Considerations

1. **Security**:
   - Implement proper authentication
   - Use HTTPS
   - Secure database connections
   - Configure CORS properly

2. **Performance**:
   - Use connection pooling
   - Implement caching
   - Optimize database queries

3. **Infrastructure**:
   - Use production ASGI server (Gunicorn/Uvicorn)
   - Set up monitoring and logging
   - Consider containerization

## Troubleshooting

### Database Issues
- Verify MySQL credentials
- Check server status
- Confirm network connectivity

### Ollama Issues
- Verify service is running
- Check model availability
- Monitor resource usage

### Application Issues
- Check logs for errors
- Verify environment variables
- Test API endpoints individually

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
