🌤️ Weather API with JWT Authentication
A production-ready Flask REST API with JWT authentication, weather data integration, and comprehensive logging.

📋 Table of Contents
Features
Tech Stack
Project Structure
Installation
Configuration
API Documentation
Authentication Flow
Testing
Deployment
Contributing
License

✨ Features
Core Features
✅ JWT Authentication - Secure token-based authentication

✅ User Management - Registration, login, profile management

✅ Weather API - Real-time weather data from OpenWeatherMap

✅ Rate Limiting - Prevent API abuse

✅ Comprehensive Logging - Request/response logging with rotation

✅ CORS Support - Cross-origin resource sharing

✅ Health Checks - Monitoring endpoints

Security Features
🔒 Password hashing with bcrypt

🔒 JWT access/refresh tokens

🔒 Token expiration (15 min access, 30 day refresh)

🔒 Input validation and sanitization

🔒 SQL injection protection (SQLAlchemy)

🔒 CORS configuration for production

Developer Features
📝 Swagger/OpenAPI documentation ready

🧪 Easy testing with Postman/Insomnia

📊 Structured logging

🔄 Database migration support

🐳 Docker support

🛠️ Tech Stack
Category	Technology	Version
Framework	Flask	2.3.3
Database	SQLAlchemy + SQLite	Latest
Authentication	JWT (Flask-JWT-Extended)	4.5.3
Password Hashing	bcrypt (Flask-Bcrypt)	1.0.1
API Testing	Postman/Insomnia	-
Environment	python-dotenv	1.0.0
CORS	Flask-CORS	4.0.0
📁 Project Structure
text
my-flask-app/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration management
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication routes
│   ├── routes.py            # API routes
│   └── utils.py             # Helper functions
├── logs/                    # Application logs
├── instance/                # Instance-specific files
│   └── app.db              # SQLite database
├── tests/                   # Unit tests
│   ├── test_auth.py
│   ├── test_routes.py
│   └── test_utils.py
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
└── README.md              # This file
🚀 Installation
Prerequisites
Python 3.8+

pip

SQLite3

Git

1. Clone the Repository
bash
git clone https://github.com/yourusername/my-flask-app.git
cd my-flask-app
2. Create Virtual Environment
bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
3. Install Dependencies
bash
pip install --upgrade pip
pip install -r requirements.txt
4. Environment Variables
bash
# Copy example environment file
cp .env.example .env

# Edit .env with your values
nano .env
5. Initialize Database
bash
# The database will be created automatically on first run
python run.py
⚙️ Configuration
Environment Variables
Create a .env file with these variables:

bash
# Flask
SECRET_KEY=your-secret-key-here
DEBUG=True

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Weather API
WEATHER_API_KEY=your-openweather-api-key
WEATHER_API_URL=http://api.openweathermap.org/data/2.5/weather

# Database
DATABASE_URL=sqlite:///app.db

# CORS (Production)
CORS_ORIGINS=https://your-frontend.com,https://admin.your-frontend.com
Configuration Classes
python
# Development
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

# Testing
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Production
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
📚 API Documentation
Authentication Endpoints
Register User
http
POST /api/auth/register
Content-Type: application/json

{
    "username": "alice",
    "email": "alice@example.com",
    "password": "secret123"
}
Response:

json
{
    "message": "User created successfully",
    "user": {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "created_at": "2024-01-15T10:30:45",
        "is_active": true
    },
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
Login
http
POST /api/auth/login
Content-Type: application/json

{
    "username": "alice",
    "password": "secret123"
}
Response:

json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
Refresh Token
http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
Response:

json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
Get Current User
http
GET /api/auth/me
Authorization: Bearer <access_token>
Public Endpoints
Get Weather
http
GET /weather?location=London
Response:

json
{
    "location": "London",
    "temperature": 15.5,
    "humidity": 72,
    "description": "broken clouds",
    "country": "GB"
}
Get Random Quote
http
GET /quote
Response:

json
{
    "quote": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs"
}
Get Client IP
http
GET /my-ip
Response:

json
{
    "ip": "192.168.1.100",
    "timestamp": 1705313245.123
}
Health Check
http
GET /health
Response:

json
{
    "status": "healthy",
    "timestamp": 1705313245.123
}
Protected Endpoints
Get Profile (Requires Auth)
http
GET /api/protected/profile
Authorization: Bearer <access_token>
Response:

json
{
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2024-01-15T10:30:45",
    "is_active": true
}
Protected Weather (Requires Auth)
http
GET /api/protected/weather?location=London
Authorization: Bearer <access_token>
Response:

json
{
    "location": "London",
    "temperature": 15.5,
    "humidity": 72,
    "description": "broken clouds",
    "country": "GB",
    "requested_by": "alice"
}
Status Codes
Status	Description
200	Success
201	Created
400	Bad Request
401	Unauthorized
403	Forbidden
404	Not Found
409	Conflict
500	Internal Server Error
🔐 Authentication Flow
JWT Token Lifecycle
text
1. Register/Login
   ↓
2. Receive access_token (15 min) + refresh_token (30 days)
   ↓
3. Use access_token for API calls
   ↓
4. Token expires (401 response)
   ↓
5. Use refresh_token to get new access_token
   ↓
6. Continue using new access_token
Using Tokens
bash
# Set token in environment
export TOKEN="eyJhbGciOiJIUzI1NiIs..."

# Use in requests
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/protected/profile
🧪 Testing
Running Tests
bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
Test with curl
bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}'

# Protected endpoint
curl -X GET http://localhost:5000/api/protected/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Test with Postman
Import Collection

Download: postman_collection.json

Import into Postman

Set Environment

json
{
    "base_url": "http://localhost:5000",
    "access_token": "{{login_response.access_token}}"
}
Automate Token

Add to Login tests:

javascript
if (responseCode.code === 200) {
    const jsonData = JSON.parse(responseBody);
    pm.environment.set("access_token", jsonData.access_token);
}
🚀 Deployment
Local Development
bash
python run.py
# Visit http://localhost:5000
Production (Gunicorn)
bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
Production (Docker)
dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
bash
# Build and run
docker build -t flask-weather-api .
docker run -p 5000:5000 flask-weather-api
Production (Nginx + Gunicorn)
nginx
server {
    listen 80;
    server_name api.weather-app.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
📊 Monitoring
Health Checks
bash
# Basic health
curl http://localhost:5000/health

# Detailed health (future)
curl http://localhost:5000/health/detailed
Logging
bash
# View logs
tail -f logs/app.log

# Rotating logs (automatic)
# Files: app.log, app.log.1, app.log.2, ...
🔧 Troubleshooting
Common Issues
1. JWT Token Expired
json
{
    "error": "Token has expired"
}
Solution: Use refresh token endpoint to get new access token.

2. Database Locked (SQLite)
text
sqlite3.OperationalError: database is locked
Solution: Use PostgreSQL in production:

python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/db'
3. CORS Errors (Browser)
text
Access to fetch at 'http://localhost:5000/weather' from origin 'http://localhost:3000' has been blocked by CORS policy
Solution: Update CORS configuration:

python
CORS(app, origins=['http://localhost:3000', 'https://yourdomain.com'])
📝 Development Guidelines
Code Style
Follow PEP 8

Use type hints

Write docstrings for all functions

Keep functions small and focused

Git Workflow
text
main → feature-branch → PR → merge
Commit Messages
bash
feat: Add user authentication
fix: Resolve database connection timeout
docs: Update API documentation
test: Add login test cases
chore: Update dependencies
Branch Strategy
bash
# Feature branches
feature/add-authentication

# Bug fixes
fix/login-timeout

# Documentation
docs/update-readme

# Releases
release/v1.0.0
📄 License
MIT License - See LICENSE for details.

🤝 Contributing
Fork the repository

Create feature branch

Commit changes

Push to branch

Open Pull Request

Pull Request Checklist
□ Tests pass
□ Code documented
□ No breaking changes
□ README updated
□ PR description provided
📞 Support
Issues: GitHub Issues

Email: your.email@example.com

Documentation: Wiki

🎯 Roadmap
Phase 1 (Current)
☑ JWT Authentication
☑ User registration/login
☑ Weather API integration
☑ Basic logging
Phase 2 (Next)
□ Email verification
□ Password reset
□ Rate limiting
□ API versioning
Phase 3 (Future)
□ Admin dashboard
□ User roles/permissions
□ Webhook support
□ Analytics
🙏 Acknowledgments
Flask team for the excellent framework

OpenWeatherMap for weather data

JWT team for authentication standard

Community contributors

📊 API Statistics
Endpoint	Method	Public	Rate Limit
/api/auth/register	POST	Yes	10/min
/api/auth/login	POST	Yes	10/min
/api/auth/refresh	POST	Yes	5/min
/api/auth/me	GET	No	20/min
/weather	GET	Yes	60/min
/api/protected/profile	GET	No	30/min
/api/protected/weather	GET	No	30/min
/quote	GET	Yes	100/min
/health	GET	Yes	Unlimited
⭐ Star Us on GitHub!
If you find this project useful, please star it on GitHub!

Happy Coding! 🚀
