import React, { useState, useEffect } from 'react';
import api from '../services/api';
import ATSScore from './ATSScore';
import './ResumeList.css';

function ResumeList({ onSelectResume, selectedResumeId, showATS = false, refreshTrigger, onResumesLoaded }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResumes();
  }, [refreshTrigger]);

  const fetchResumes = async () => {
    try {
      const result = await api.getResumes();
      if (result.success) {
        setResumes(result.resumes);
        if (onResumesLoaded) {
          onResumesLoaded(result.resumes);
        }
      }
    } catch (error) {
      console.error('Error fetching resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (resumeId) => {
    if (window.confirm('Are you sure you want to delete this resume?')) {
      try {
        await api.deleteResume(resumeId);
        fetchResumes();
      } catch (error) {
        alert('Error deleting resume: ' + error.message);
      }
    }
  };

  if (loading) {
    return <div className="resume-list">Loading resumes...</div>;
  }

  return (
    <div className="resume-list">
      <h2>Resumes ({resumes.length})</h2>
      {resumes.length === 0 ? (
        <p className="empty-message">No resumes uploaded yet</p>
      ) : (
        <div className="resume-items">
          {resumes.map((resume) => (
            <div
              key={resume._id}
              className={`resume-item ${selectedResumeId === resume._id ? 'selected' : ''}`}
              onClick={() => onSelectResume && onSelectResume(resume._id)}
            >
              <div className="resume-info">
                <div className="resume-header-row">
                  <h3>{resume.name || 'Unknown'}</h3>
                  {resume.ats_score && (
                    <div className="ats-score-badge">
                      ATS: {resume.ats_score.ats_score}
                    </div>
                  )}
                </div>
                <p className="resume-email">{resume.email || 'No email'}</p>
                <div className="resume-skills">
                  {resume.skills && resume.skills.slice(0, 5).map((skill, idx) => (
                    <span key={idx} className="skill-badge">{skill}</span>
                  ))}
                  {resume.skills && resume.skills.length > 5 && (
                    <span className="skill-more">+{resume.skills.length - 5} more</span>
                  )}
                </div>
              </div>
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(resume._id);
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
      
      {showATS && selectedResumeId && (
        <div className="ats-score-section">
          <ATSScore 
            resumeId={selectedResumeId}
            resumeName={resumes.find(r => r._id === selectedResumeId)?.name}
          />
        </div>
      )}
    </div>
  );
}

export default ResumeList;
