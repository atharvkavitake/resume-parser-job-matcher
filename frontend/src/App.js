import React, { useState } from 'react';
import { useTheme } from './contexts/ThemeContext';
import './App.css';
import ResumeUpload from './components/ResumeUpload';
import JobUpload from './components/JobUpload';
import ResumeList from './components/ResumeList';
import JobList from './components/JobList';
import MatchResults from './components/MatchResults';
import JobRecommendations from './components/JobRecommendations';
import ThemeToggle from './components/ThemeToggle';

function App() {
  const { isDarkMode } = useTheme();
  const [selectedResumeId, setSelectedResumeId] = useState(null);
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [showMatchResults, setShowMatchResults] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [resumes, setResumes] = useState([]);
  const [currentStep, setCurrentStep] = useState(1); // 1: Upload Resume, 2: Upload Job, 3: View Results

  const handleResumeUpload = () => {
    setShowMatchResults(false);
    setCurrentStep(2);
    // Trigger refresh
    setTimeout(() => setRefreshTrigger(prev => prev + 1), 500);
  };

  const handleJobUpload = () => {
    setShowMatchResults(false);
    setCurrentStep(3);
    // Trigger refresh
    setTimeout(() => setRefreshTrigger(prev => prev + 1), 500);
  };

  const handleMatch = () => {
    if (selectedResumeId && selectedJobId) {
      setShowMatchResults(true);
    } else {
      alert('Please select both a resume and a job to match');
    }
  };

  return (
    <div className={`App ${isDarkMode ? 'dark' : 'light'}`}>
      <header className="App-header">
        <div className="header-content">
          <div className="header-left">
            <h1>Resume Parser & Job Matcher</h1>
            <p>AI-Powered Resume Analysis & Job Matching</p>
          </div>
          <ThemeToggle />
        </div>
        <div className="progress-steps">
          <div className={`step ${currentStep >= 1 ? 'active' : ''}`}>
            <div className="step-number">1</div>
            <div className="step-label">Upload Resume</div>
          </div>
          <div className={`step-connector ${currentStep >= 2 ? 'active' : ''}`}></div>
          <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>
            <div className="step-number">2</div>
            <div className="step-label">Upload Job</div>
          </div>
          <div className={`step-connector ${currentStep >= 3 ? 'active' : ''}`}></div>
          <div className={`step ${currentStep >= 3 ? 'active' : ''}`}>
            <div className="step-number">3</div>
            <div className="step-label">View Results</div>
          </div>
        </div>
      </header>

      <div className="App-container">
        <div className="App-sidebar">
          <div className="sidebar-section">
            <ResumeUpload onUploadSuccess={handleResumeUpload} />
          </div>
          <div className="sidebar-section">
            <JobUpload onUploadSuccess={handleJobUpload} />
          </div>
        </div>

        <div className="App-main">
          <div className="main-section">
            <ResumeList
              onSelectResume={(id) => {
                setSelectedResumeId(id);
                setSelectedJobId(null); // Clear job selection when resume changes
                setShowMatchResults(false);
              }}
              selectedResumeId={selectedResumeId}
              showATS={true}
              refreshTrigger={refreshTrigger}
              onResumesLoaded={setResumes}
            />
          </div>

          <div className="main-section">
            <JobList
              onSelectJob={setSelectedJobId}
              selectedJobId={selectedJobId}
            />
          </div>

          {selectedResumeId && selectedJobId && (
            <div className="match-section">
              <button className="match-button" onClick={handleMatch}>
                Match Resume to Job
              </button>
            </div>
          )}

          {showMatchResults && selectedResumeId && selectedJobId && (
            <div className="main-section">
              <MatchResults
                resumeId={selectedResumeId}
                jobId={selectedJobId}
                onClose={() => setShowMatchResults(false)}
              />
            </div>
          )}

          {/* Show job recommendations when only resume is selected */}
          {selectedResumeId && !selectedJobId && (
            <div className="main-section">
              <JobRecommendations
                resumeId={selectedResumeId}
                resumeName={resumes.find(r => r._id === selectedResumeId)?.name || 'Your Resume'}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
