import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const apiService = {
  // Auth
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/token', {
      username: email,
      password: password,
    });
    return response.data;
  },

  register: async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // Dashboard
  getDashboardStats: async () => {
    const response = await api.get('/reports/dashboard');
    return response.data;
  },

  // Jobs
  searchJobs: async (searchParams: any) => {
    const response = await api.post('/jobs/search', searchParams);
    return response.data;
  },

  getJobs: async (params: any = {}) => {
    const response = await api.get('/jobs', { params });
    return response.data;
  },

  getJob: async (jobId: number) => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  // Applications
  getApplications: async (params: any = {}) => {
    const response = await api.get('/applications', { params });
    return response.data;
  },

  createApplication: async (applicationData: any) => {
    const response = await api.post('/applications', applicationData);
    return response.data;
  },

  batchApply: async (jobIds: number[]) => {
    const response = await api.post('/applications/batch-apply', { job_ids: jobIds });
    return response.data;
  },

  updateApplication: async (applicationId: number, updateData: any) => {
    const response = await api.put(`/applications/${applicationId}`, updateData);
    return response.data;
  },

  // Reports
  getAnalytics: async (days: number = 30) => {
    const response = await api.get(`/reports/analytics?days=${days}`);
    return response.data;
  },
};

export default api;