# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Login
```http
POST /auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "refresh_token": "eyJ..."
}
```

### Jobs

#### Search Jobs
```http
POST /jobs/search
```

Request body:
```json
{
  "keywords": "Python Developer",
  "location": "San Francisco, CA",
  "experience_level": "Mid Level",
  "max_results": 50
}
```

Response:
```json
{
  "jobs_found": 25,
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "description": "...",
      "url": "https://..."
    }
  ]
}
```

#### Get Job Details
```http
GET /jobs/{job_id}
```

Response:
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "company": "Tech Corp",
  "location": "San Francisco, CA",
  "description": "Detailed job description...",
  "requirements": "5+ years of Python...",
  "salary_min": 120000,
  "salary_max": 180000
}
```

#### Analyze Job Match
```http
POST /jobs/{job_id}/analyze
```

Response:
```json
{
  "match_score": 85.5,
  "strengths": [
    "Strong Python experience",
    "Relevant tech stack"
  ],
  "gaps": [
    "No Kubernetes experience"
  ],
  "reasoning": "Your profile is a strong match..."
}
```

### Applications

#### Create Application
```http
POST /applications
```

Request body:
```json
{
  "job_id": 1,
  "cover_letter": "Dear Hiring Manager...",
  "custom_responses": {
    "why_interested": "I am passionate about..."
  }
}
```

Response:
```json
{
  "id": 1,
  "job_id": 1,
  "status": "draft",
  "created_at": "2024-01-01T12:00:00"
}
```

#### List Applications
```http
GET /applications?status=applied&limit=10
```

Response:
```json
{
  "total": 25,
  "applications": [
    {
      "id": 1,
      "job_id": 1,
      "status": "applied",
      "applied_at": "2024-01-01T12:00:00"
    }
  ]
}
```

#### Update Application Status
```http
PUT /applications/{application_id}/status
```

Request body:
```json
{
  "status": "interview",
  "notes": "Scheduled for next week"
}
```

### User Profile

#### Upload Resume
```http
POST /users/resume
Content-Type: multipart/form-data
```

Form data:
- file: (binary)

Response:
```json
{
  "id": 1,
  "file_path": "/data/resumes/user1_resume.pdf",
  "parsed_data": {
    "skills": ["Python", "FastAPI", "Docker"],
    "experience": [...]
  }
}
```

#### Update Preferences
```http
PUT /users/preferences
```

Request body:
```json
{
  "desired_roles": ["Python Developer", "Backend Engineer"],
  "min_salary": 100000,
  "enable_auto_apply": false,
  "max_applications_per_day": 10
}
```

#### Get Job Matches
```http
GET /users/matches?limit=10
```

Response:
```json
{
  "matches": [
    {
      "job_id": 1,
      "match_score": 92.5,
      "reasoning": "Excellent match based on skills...",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- Per minute: 60 requests
- Per hour: 1000 requests

Headers included in responses:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp
