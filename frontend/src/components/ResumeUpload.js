import React, { useState } from 'react';
import api from '../services/api';
import './ResumeUpload.css';

function ResumeUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const ext = selectedFile.name.split('.').pop().toLowerCase();
      if (['pdf', 'docx', 'doc'].includes(ext)) {
        setFile(selectedFile);
        setMessage('');
      } else {
        setMessage('Please select a PDF or DOCX file');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const result = await api.uploadResume(file);
      if (result.success) {
        setMessage('Resume uploaded and parsed successfully!');
        setFile(null);
        if (onUploadSuccess) {
          onUploadSuccess(result.resume);
        }
      } else {
        setMessage(result.error || 'Upload failed');
      }
    } catch (error) {
      setMessage('Error uploading resume: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="resume-upload">
      <h2>Upload Resume</h2>
      <div className="upload-form">
        <input
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          disabled={uploading}
        />
        <button onClick={handleUpload} disabled={uploading || !file}>
          {uploading ? 'Uploading...' : 'Upload Resume'}
        </button>
      </div>
      {message && (
        <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
