import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './JobList.css';

function JobList({ onSelectJob, selectedJobId }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const result = await api.getJobs();
      if (result.success) {
        setJobs(result.jobs);
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await api.deleteJob(jobId);
        fetchJobs();
      } catch (error) {
        alert('Error deleting job: ' + error.message);
      }
    }
  };

  if (loading) {
    return <div className="job-list">Loading jobs...</div>;
  }

  return (
    <div className="job-list">
      <h2>Jobs ({jobs.length})</h2>
      {jobs.length === 0 ? (
        <p className="empty-message">No jobs uploaded yet</p>
      ) : (
        <div className="job-items">
          {jobs.map((job) => (
            <div
              key={job._id}
              className={`job-item ${selectedJobId === job._id ? 'selected' : ''}`}
              onClick={() => onSelectJob && onSelectJob(job._id)}
            >
              <div className="job-info">
                <h3>{job.title || 'Untitled'}</h3>
                <p className="job-company">{job.company || 'No company'}</p>
                {job.location && <p className="job-location">📍 {job.location}</p>}
                <div className="job-skills">
                  <div className="skills-group">
                    <strong>Required:</strong>
                    {job.required_skills && job.required_skills.slice(0, 3).map((skill, idx) => (
                      <span key={idx} className="skill-badge required">{skill}</span>
                    ))}
                    {job.required_skills && job.required_skills.length > 3 && (
                      <span className="skill-more">+{job.required_skills.length - 3} more</span>
                    )}
                  </div>
                </div>
              </div>
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(job._id);
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default JobList;

