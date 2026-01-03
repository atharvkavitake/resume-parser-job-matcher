import React, { useState } from 'react';
import api from '../services/api';
import './JobUpload.css';

function JobUpload({ onUploadSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    description: '',
    required_skills: '',
    preferred_skills: '',
    experience_required: '',
    location: ''
  });
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title || !formData.description) {
      setMessage('Title and description are required');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const jobData = {
        ...formData,
        required_skills: formData.required_skills
          ? formData.required_skills.split(',').map(s => s.trim()).filter(s => s)
          : [],
        preferred_skills: formData.preferred_skills
          ? formData.preferred_skills.split(',').map(s => s.trim()).filter(s => s)
          : [],
        experience_required: parseInt(formData.experience_required) || 0
      };

      const result = await api.uploadJob(jobData);
      if (result.success) {
        setMessage('Job uploaded successfully!');
        setFormData({
          title: '',
          company: '',
          description: '',
          required_skills: '',
          preferred_skills: '',
          experience_required: '',
          location: ''
        });
        if (onUploadSuccess) {
          onUploadSuccess(result.job);
        }
      } else {
        setMessage(result.error || 'Upload failed');
      }
    } catch (error) {
      setMessage('Error uploading job: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="job-upload">
      <h2>Upload Job Description</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Job Title *</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Company</label>
          <input
            type="text"
            name="company"
            value={formData.company}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Description *</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="5"
            required
          />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Required Skills (comma-separated)</label>
            <input
              type="text"
              name="required_skills"
              value={formData.required_skills}
              onChange={handleChange}
              placeholder="Python, JavaScript, React"
            />
          </div>
          <div className="form-group">
            <label>Preferred Skills (comma-separated)</label>
            <input
              type="text"
              name="preferred_skills"
              value={formData.preferred_skills}
              onChange={handleChange}
              placeholder="MongoDB, Docker"
            />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Experience Required (years)</label>
            <input
              type="number"
              name="experience_required"
              value={formData.experience_required}
              onChange={handleChange}
              min="0"
            />
          </div>
          <div className="form-group">
            <label>Location</label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
            />
          </div>
        </div>
        <button type="submit" disabled={uploading}>
          {uploading ? 'Uploading...' : 'Upload Job'}
        </button>
      </form>
      {message && (
        <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
    </div>
  );
}

export default JobUpload;
