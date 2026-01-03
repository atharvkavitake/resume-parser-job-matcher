/**
 * API service for communicating with Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

const api = {
  // Resume endpoints
  uploadResume: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/upload-resume`, {
      method: 'POST',
      body: formData
    });
    
    return response.json();
  },

  getResumes: async () => {
    const response = await fetch(`${API_BASE_URL}/resumes`);
    return response.json();
  },

  getResume: async (resumeId) => {
    const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}`);
    return response.json();
  },

  deleteResume: async (resumeId) => {
    const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}`, {
      method: 'DELETE'
    });
    return response.json();
  },

  // Job endpoints
  uploadJob: async (jobData) => {
    const response = await fetch(`${API_BASE_URL}/upload-job`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jobData)
    });
    return response.json();
  },

  getJobs: async () => {
    const response = await fetch(`${API_BASE_URL}/jobs`);
    return response.json();
  },

  getJob: async (jobId) => {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
    return response.json();
  },

  deleteJob: async (jobId) => {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
      method: 'DELETE'
    });
    return response.json();
  },

  // Matching endpoints
  matchResumeToJob: async (resumeId, jobId) => {
    const response = await fetch(`${API_BASE_URL}/match`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ resume_id: resumeId, job_id: jobId })
    });
    return response.json();
  },

  matchAllResumesToJob: async (jobId) => {
    const response = await fetch(`${API_BASE_URL}/match-all/${jobId}`);
    return response.json();
  },

  matchResumeToAllJobs: async (resumeId) => {
    const response = await fetch(`${API_BASE_URL}/match-resume/${resumeId}`);
    return response.json();
  },

  // ATS Score endpoints
  getATSScore: async (resumeId) => {
    const response = await fetch(`${API_BASE_URL}/ats-score/${resumeId}`);
    return response.json();
  },

  // Job Recommendation endpoints
  getJobRecommendations: async (resumeId, limit = 10) => {
    const response = await fetch(`${API_BASE_URL}/recommend-jobs/${resumeId}?limit=${limit}`);
    return response.json();
  }
};

export default api;
