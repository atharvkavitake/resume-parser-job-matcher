import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useTheme } from '../contexts/ThemeContext';
import './ATSScore.css';
import { generateATSReportPDF } from '../utils/pdfGenerator';

function ATSScore({ resumeId, resumeName }) {
  const { isDarkMode } = useTheme();
  const [atsData, setAtsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    if (resumeId) {
      fetchATSScore();
    }
  }, [resumeId]);

  useEffect(() => {
    if (atsData) {
      // Animate score from 0 to actual score
      const targetScore = atsData.ats_score;
      const duration = 2000;
      const steps = 60;
      const increment = targetScore / steps;
      let current = 0;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= targetScore) {
          setAnimatedScore(targetScore);
          clearInterval(timer);
        } else {
          setAnimatedScore(current);
        }
      }, duration / steps);

      return () => clearInterval(timer);
    }
  }, [atsData]);

  const fetchATSScore = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await api.getATSScore(resumeId);
      if (result.success) {
        setAtsData(result.ats_score);
      } else {
        setError(result.error || 'Failed to fetch ATS score');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (atsData && resumeName) {
      generateATSReportPDF(atsData, resumeName);
    }
  };

  if (!resumeId) {
    return null;
  }

  if (loading) {
    return (
      <div className="ats-score-container loading">
        <div className="spinner"></div>
        <p>Calculating ATS Score...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ats-score-container error">
        <p>{error}</p>
        <button onClick={fetchATSScore} className="retry-btn">Retry</button>
      </div>
    );
  }

  if (!atsData) {
    return null;
  }

  const { ats_score, grade, rating, percentage, factors, recommendations } = atsData;
  const scoreColor = getScoreColor(ats_score);
  const verdict = getVerdict(ats_score);
  const circumference = 2 * Math.PI * 90; // radius = 90
  const offset = circumference - (animatedScore / 100) * circumference;

  return (
    <div className="ats-score-container hero-section">
      <div className="ats-header-section">
        <div className="header-content">
          <h2>ATS Score Analysis</h2>
          <p className="subtitle">Resume Optimization Report</p>
        </div>
        <button onClick={handleDownloadPDF} className="download-pdf-btn">
          📄 Download ATS Report (PDF)
        </button>
      </div>

      <div className="ats-main-display">
        <div className="score-visualization">
          <svg className="circular-progress" width="240" height="240">
            <circle
              className="progress-ring-background"
              cx="120"
              cy="120"
              r="90"
              fill="none"
              stroke="var(--border-color)"
              strokeWidth="12"
            />
            <circle
              className="progress-ring"
              cx="120"
              cy="120"
              r="90"
              fill="none"
              stroke={scoreColor}
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              transform="rotate(-90 120 120)"
              style={{ transition: 'stroke-dashoffset 0.1s ease-out' }}
            />
          </svg>
          <div className="score-content">
            <div className="score-value-large">{Math.round(animatedScore)}</div>
            <div className="score-grade">{grade}</div>
            <div className="score-rating">{rating}</div>
          </div>
        </div>

        <div className="verdict-section">
          <div className={`verdict-badge ${verdict.class}`}>
            <span className="verdict-icon">{verdict.icon}</span>
            <div>
              <div className="verdict-label">{verdict.label}</div>
              <div className="verdict-description">{verdict.description}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="ats-factors">
        <h3>Score Breakdown</h3>
        <div className="factors-grid">
          {Object.entries(factors).map(([key, factor]) => (
            <div key={key} className="factor-item">
              <div className="factor-header">
                <span className="factor-name">{formatFactorName(key)}</span>
                <span className="factor-score">
                  {factor.score.toFixed(1)}/{factor.max}
                </span>
              </div>
              <div className="factor-bar">
                <div
                  className="factor-bar-fill"
                  style={{
                    width: `${(factor.score / factor.max) * 100}%`,
                    backgroundColor: getFactorColor(factor.score, factor.max)
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {recommendations && recommendations.length > 0 && (
        <div className="ats-recommendations">
          <h3>AI Recommendations</h3>
          <div className="recommendations-list">
            {recommendations.map((rec, idx) => (
              <div key={idx} className={`recommendation-item ${rec.priority}`}>
                <div className="rec-priority-badge">{rec.priority}</div>
                <div className="rec-content">
                  <div className="rec-category">{rec.category}</div>
                  <div className="rec-message">{rec.message}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function getScoreColor(score) {
  if (score >= 85) return '#28a745';
  if (score >= 70) return '#17a2b8';
  if (score >= 50) return '#ffc107';
  return '#dc3545';
}

function getVerdict(score) {
  if (score >= 85) {
    return {
      class: 'excellent',
      icon: '⭐',
      label: 'Excellent',
      description: 'Your resume is highly optimized for ATS systems'
    };
  } else if (score >= 70) {
    return {
      class: 'good',
      icon: '✓',
      label: 'Good',
      description: 'Your resume is well-optimized with minor improvements needed'
    };
  } else if (score >= 50) {
    return {
      class: 'average',
      icon: '⚠',
      label: 'Average',
      description: 'Your resume needs optimization to improve ATS compatibility'
    };
  } else {
    return {
      class: 'poor',
      icon: '✗',
      label: 'Poor',
      description: 'Significant improvements needed for ATS compatibility'
    };
  }
}

function getFactorColor(score, max) {
  const percentage = (score / max) * 100;
  if (percentage >= 80) return '#28a745';
  if (percentage >= 60) return '#17a2b8';
  if (percentage >= 40) return '#ffc107';
  return '#dc3545';
}

function formatFactorName(name) {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export default ATSScore;
