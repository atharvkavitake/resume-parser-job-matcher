import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './MatchResults.css';

function MatchResults({ resumeId, jobId, onClose }) {
  const [matchData, setMatchData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (resumeId && jobId) {
      fetchMatch();
    }
  }, [resumeId, jobId]);

  const fetchMatch = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await api.matchResumeToJob(resumeId, jobId);
      if (result.success) {
        setMatchData(result.match);
      } else {
        setError(result.error || 'Failed to fetch match results');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="match-results loading">Loading match results...</div>;
  }

  if (error) {
    return <div className="match-results error">{error}</div>;
  }

  if (!matchData) {
    return null;
  }

  const { overall_match_score, tfidf_score, skill_match, skill_gap } = matchData;

  return (
    <div className="match-results">
      <div className="match-header">
        <h2>Match Results</h2>
        {onClose && <button className="close-btn" onClick={onClose}>×</button>}
      </div>

      <div className="match-score">
        <div className="score-circle">
          <div className="score-value">{overall_match_score}%</div>
          <div className="score-label">Match Score</div>
        </div>
      </div>

      <div className="match-details">
        <div className="detail-section">
          <h3>Overall Score Breakdown</h3>
          <div className="score-breakdown">
            <div className="score-item">
              <span>TF-IDF Similarity:</span>
              <span className="score-value-small">{tfidf_score}%</span>
            </div>
            <div className="score-item">
              <span>Skill Match:</span>
              <span className="score-value-small">{skill_match.overall_skill_score}%</span>
            </div>
          </div>
        </div>

        <div className="detail-section">
          <h3>Skill Matching</h3>
          <div className="skills-list">
            <div className="skills-group">
              <h4>Matching Required Skills</h4>
              <div className="skill-tags">
                {skill_match.matching_required_skills.length > 0 ? (
                  skill_match.matching_required_skills.map((skill, idx) => (
                    <span key={idx} className="skill-tag match">✓ {skill}</span>
                  ))
                ) : (
                  <span className="no-skills">None</span>
                )}
              </div>
            </div>
            <div className="skills-group">
              <h4>Missing Required Skills</h4>
              <div className="skill-tags">
                {skill_gap.missing_required_skills.length > 0 ? (
                  skill_gap.missing_required_skills.map((skill, idx) => (
                    <span key={idx} className="skill-tag missing">✗ {skill}</span>
                  ))
                ) : (
                  <span className="no-skills">None - All required skills matched!</span>
                )}
              </div>
            </div>
            <div className="skills-group">
              <h4>Matching Preferred Skills</h4>
              <div className="skill-tags">
                {skill_match.matching_preferred_skills.length > 0 ? (
                  skill_match.matching_preferred_skills.map((skill, idx) => (
                    <span key={idx} className="skill-tag match">✓ {skill}</span>
                  ))
                ) : (
                  <span className="no-skills">None</span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="detail-section">
          <h3>Skill Gap Analysis</h3>
          <div className="gap-stats">
            <div className="stat-item">
              <span>Required Skills Match:</span>
              <span>{skill_gap.statistics.matched_required} / {skill_gap.statistics.total_required}</span>
            </div>
            <div className="stat-item">
              <span>Preferred Skills Match:</span>
              <span>{skill_gap.statistics.matched_preferred} / {skill_gap.statistics.total_preferred}</span>
            </div>
          </div>
          {skill_gap.recommendations.length > 0 && (
            <div className="recommendations">
              {skill_gap.recommendations.map((rec, idx) => (
                <div key={idx} className={`recommendation ${rec.priority}`}>
                  <strong>{rec.priority.toUpperCase()}:</strong> {rec.message}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MatchResults;
