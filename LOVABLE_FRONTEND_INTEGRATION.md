# 🎨 Lovable Frontend Integration Guide

This guide explains how to integrate your Lovable-built frontend with the LinkedIn Job Automation backend.

## 📋 Overview

Your backend is a **FastAPI** application running on `http://localhost:8000` with full API documentation, authentication, and job automation features. You can connect any frontend framework (React, Next.js, Vue, etc.) to it.

## 🔧 Backend Setup (Already Done ✅)

### Current Backend Features:
- ✅ FastAPI REST API
- ✅ CORS enabled for cross-origin requests
- ✅ Swagger UI documentation at `/docs`
- ✅ AutoAgentHire routes for job automation
- ✅ Authentication endpoints
- ✅ Job search and application APIs

### Backend is Running On:
- **API Base URL**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/`

## 🎯 Frontend Integration Steps

### 1. **Configure API Base URL in Lovable**

In your Lovable project, create an environment configuration:

```typescript
// src/config/api.ts
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Health
  health: `${API_BASE_URL}/`,
  
  // User Profile
  createProfile: `${API_BASE_URL}/api/user-profile`,
  getProfile: `${API_BASE_URL}/api/user-profile`,
  
  // Job Search
  searchJobs: `${API_BASE_URL}/api/search-jobs`,
  
  // Applications
  applyToJob: `${API_BASE_URL}/api/apply-job`,
  getApplications: `${API_BASE_URL}/api/applications`,
  
  // AutoAgentHire
  runAgent: `${API_BASE_URL}/api/run-agent`,
  getAgentStatus: `${API_BASE_URL}/api/agent-status`,
};
```

### 2. **Create `.env` file in Lovable Project**

```env
VITE_API_URL=http://localhost:8000
```

For production:
```env
VITE_API_URL=https://your-backend-domain.com
```

### 3. **API Client Setup**

Create an API client with axios or fetch:

```typescript
// src/lib/apiClient.ts
import axios from 'axios';
import { API_BASE_URL } from '@/config/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // For cookie-based auth
});

// Add request interceptor for auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### 4. **Example API Service Functions**

```typescript
// src/services/jobService.ts
import { apiClient } from '@/lib/apiClient';

export interface UserProfile {
  email: string;
  resume_text: string;
  linkedin_url?: string;
  target_roles: string[];
  target_locations: string[];
  openai_api_key?: string;
  gemini_api_key?: string;
}

export interface JobSearchParams {
  keywords: string;
  location: string;
  experience_level?: string;
  job_type?: string;
}

export const jobService = {
  // Create user profile
  async createProfile(profile: UserProfile) {
    const response = await apiClient.post('/api/user-profile', profile);
    return response.data;
  },

  // Search for jobs
  async searchJobs(params: JobSearchParams) {
    const response = await apiClient.post('/api/search-jobs', params);
    return response.data;
  },

  // Run AutoAgentHire
  async runAgent(config: any) {
    const response = await apiClient.post('/api/run-agent', config);
    return response.data;
  },

  // Get agent status
  async getAgentStatus(sessionId: string) {
    const response = await apiClient.get(`/api/agent-status/${sessionId}`);
    return response.data;
  },

  // Get applications
  async getApplications() {
    const response = await apiClient.get('/api/applications');
    return response.data;
  },
};
```

### 5. **React Query Setup (Recommended)**

```typescript
// src/hooks/useJobs.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { jobService } from '@/services/jobService';

export const useSearchJobs = () => {
  return useMutation({
    mutationFn: jobService.searchJobs,
    onSuccess: (data) => {
      console.log('Jobs found:', data);
    },
  });
};

export const useRunAgent = () => {
  return useMutation({
    mutationFn: jobService.runAgent,
    onSuccess: (data) => {
      console.log('Agent started:', data);
    },
  });
};

export const useApplications = () => {
  return useQuery({
    queryKey: ['applications'],
    queryFn: jobService.getApplications,
    refetchInterval: 5000, // Refresh every 5 seconds
  });
};
```

### 6. **Example Component Usage**

```tsx
// src/components/JobSearch.tsx
import { useState } from 'react';
import { useSearchJobs } from '@/hooks/useJobs';

export const JobSearch = () => {
  const [keywords, setKeywords] = useState('');
  const [location, setLocation] = useState('');
  const searchJobs = useSearchJobs();

  const handleSearch = async () => {
    try {
      const result = await searchJobs.mutateAsync({
        keywords,
        location,
      });
      console.log('Search results:', result);
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  return (
    <div className="job-search">
      <input
        type="text"
        value={keywords}
        onChange={(e) => setKeywords(e.target.value)}
        placeholder="Job title, keywords..."
      />
      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Location..."
      />
      <button 
        onClick={handleSearch}
        disabled={searchJobs.isPending}
      >
        {searchJobs.isPending ? 'Searching...' : 'Search Jobs'}
      </button>
    </div>
  );
};
```

## 🔐 Authentication

### JWT Token Flow:

1. **Login/Register**
```typescript
// src/services/authService.ts
export const authService = {
  async login(email: string, password: string) {
    const response = await apiClient.post('/api/auth/login', {
      email,
      password,
    });
    const { access_token } = response.data;
    localStorage.setItem('auth_token', access_token);
    return response.data;
  },

  async logout() {
    localStorage.removeItem('auth_token');
  },

  getToken() {
    return localStorage.getItem('auth_token');
  },
};
```

## 📡 Available API Endpoints

### Core Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/user-profile` | Create user profile |
| GET | `/api/user-profile` | Get user profile |
| POST | `/api/search-jobs` | Search for jobs |
| POST | `/api/apply-job` | Apply to a job |
| GET | `/api/applications` | Get all applications |
| POST | `/api/run-agent` | Run AutoAgentHire agent |
| GET | `/api/agent-status/{id}` | Get agent status |

### Full API Documentation:
Visit `http://localhost:8000/docs` for interactive API documentation with:
- Request/response schemas
- Try-it-out functionality
- Authentication testing

## 🚀 Development Workflow

### Running Both Applications:

1. **Start Backend** (Already running):
```bash
cd LinkedIn-Job-Automation-with-AI
source venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start Lovable Frontend**:
```bash
cd your-lovable-project
npm run dev
```

Frontend will typically run on `http://localhost:5173` (Vite default)

### CORS Configuration:

The backend is already configured to accept requests from:
- ✅ `http://localhost:3000` (React default)
- ✅ `http://localhost:5173` (Vite default)
- ✅ `http://localhost:8501` (Streamlit)
- ✅ `https://*.lovable.app` (Lovable production)
- ✅ `https://*.lovable.dev` (Lovable dev)

## 📦 Example: Complete Job Application Flow

```typescript
// src/pages/JobApplication.tsx
import { useState } from 'react';
import { jobService } from '@/services/jobService';

export const JobApplication = () => {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');

  const handleAutoApply = async () => {
    setLoading(true);
    try {
      // 1. Create user profile
      await jobService.createProfile({
        email: 'user@example.com',
        resume_text: 'Your resume content...',
        target_roles: ['Software Engineer', 'AI Engineer'],
        target_locations: ['Remote', 'San Francisco'],
        gemini_api_key: 'your-key',
      });

      // 2. Run the agent
      const result = await jobService.runAgent({
        keywords: 'AI Engineer',
        location: 'Remote',
        max_applications: 5,
      });

      setStatus(`Agent started! Session: ${result.session_id}`);

      // 3. Poll for status
      const interval = setInterval(async () => {
        const status = await jobService.getAgentStatus(result.session_id);
        setStatus(`Status: ${status.status} - ${status.jobs_applied} jobs applied`);
        
        if (status.status === 'completed') {
          clearInterval(interval);
          setLoading(false);
        }
      }, 5000);

    } catch (error) {
      console.error('Error:', error);
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleAutoApply} disabled={loading}>
        {loading ? 'Running...' : 'Start Auto Apply'}
      </button>
      <p>{status}</p>
    </div>
  );
};
```

## 🎨 Lovable-Specific Tips

### 1. **Use Lovable's Built-in Components**

Lovable provides beautiful pre-built components. Use them with your API:

```tsx
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";

export const JobCard = ({ job }) => {
  const { toast } = useToast();
  
  const handleApply = async () => {
    try {
      await jobService.applyToJob(job.id);
      toast({
        title: "Success!",
        description: "Application submitted",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to apply",
        variant: "destructive",
      });
    }
  };

  return (
    <Card>
      <h3>{job.title}</h3>
      <p>{job.company}</p>
      <Button onClick={handleApply}>Quick Apply</Button>
    </Card>
  );
};
```

### 2. **State Management with Zustand** (if using)

```typescript
// src/store/jobStore.ts
import { create } from 'zustand';

interface JobStore {
  jobs: any[];
  loading: boolean;
  setJobs: (jobs: any[]) => void;
  setLoading: (loading: boolean) => void;
}

export const useJobStore = create<JobStore>((set) => ({
  jobs: [],
  loading: false,
  setJobs: (jobs) => set({ jobs }),
  setLoading: (loading) => set({ loading }),
}));
```

## 🌐 Production Deployment

### Backend Deployment Options:

1. **Railway** (Recommended for FastAPI):
   - Connect GitHub repo
   - Auto-deploy on push
   - Environment variables in dashboard

2. **Render**:
   - Free tier available
   - Easy FastAPI deployment

3. **AWS/GCP/Azure**:
   - Docker container deployment
   - More control, more setup

### Connecting Lovable Production to Backend:

1. Deploy backend and get production URL (e.g., `https://api.yourapp.com`)
2. Update `.env` in Lovable:
   ```env
   VITE_API_URL=https://api.yourapp.com
   ```
3. Update CORS in backend `.env`:
   ```env
   CORS_ORIGINS=https://your-lovable-app.lovable.app
   ```

## ✅ Testing the Integration

### 1. Test Health Check:

```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "name": "AutoAgentHire",
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Test from Lovable:

```typescript
// In browser console or component
fetch('http://localhost:8000/')
  .then(res => res.json())
  .then(data => console.log(data));
```

### 3. Test API Call:

```typescript
import { apiClient } from '@/lib/apiClient';

apiClient.get('/')
  .then(res => console.log('Backend connected:', res.data))
  .catch(err => console.error('Connection failed:', err));
```

## 📚 Additional Resources

- **Backend API Docs**: http://localhost:8000/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **React Query**: https://tanstack.com/query
- **Axios**: https://axios-http.com

## 🆘 Troubleshooting

### CORS Errors:
- Add your Lovable URL to `CORS_ORIGINS` in `.env`
- Restart the backend after changes

### Connection Refused:
- Check backend is running on port 8000
- Verify API_BASE_URL in frontend config

### 401 Unauthorized:
- Check if auth token is being sent
- Verify token format in headers

## 🎉 Next Steps

1. ✅ Backend is running and configured
2. 📝 Copy API configuration to your Lovable project
3. 🔧 Set up API client and services
4. 🎨 Build UI components that call the APIs
5. 🚀 Test the integration locally
6. 🌐 Deploy when ready!

---

**Need Help?** Check the API documentation at http://localhost:8000/docs for all available endpoints and request/response formats.
