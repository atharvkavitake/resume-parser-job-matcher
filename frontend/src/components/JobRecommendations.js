import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { useTheme } from '../contexts/ThemeContext';
import api from '../services/api';
import './JobRecommendations.css';

function JobRecommendations({ resumeId, resumeName }) {
  const { isDarkMode } = useTheme();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedJob, setSelectedJob] = useState(null);
  const [showWhyMatch, setShowWhyMatch] = useState({});

  useEffect(() => {
    if (resumeId) {
      fetchRecommendations();
    }
  }, [resumeId]);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await api.getJobRecommendations(resumeId, 10);
      if (result.success) {
        setRecommendations(result.recommendations);
      } else {
        setError(result.error || 'Failed to fetch recommendations');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!resumeId) {
    return null;
  }

  if (loading) {
    return (
      <div className="job-recommendations loading">
        <div className="spinner"></div>
        <p>Analyzing your resume and finding matching jobs...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="job-recommendations error">
        <p>{error}</p>
        <button onClick={fetchRecommendations} className="retry-btn">Retry</button>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="job-recommendations empty">
        <p>No jobs found. Please upload some job descriptions first.</p>
      </div>
    );
  }

  // Prepare data for charts
  const barChartData = recommendations.slice(0, 5).map(rec => ({
    name: rec.job_title.length > 15 ? rec.job_title.substring(0, 15) + '...' : rec.job_title,
    'Match Score': rec.overall_match_score,
    'TF-IDF': rec.tfidf_score,
    'Skills': rec.skill_match.overall_score * 100
  }));

  const pieChartData = recommendations.slice(0, 5).map(rec => ({
    name: rec.job_title.length > 20 ? rec.job_title.substring(0, 20) + '...' : rec.job_title,
    value: rec.overall_match_score
  }));

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'];

  // Radar chart data for selected job
  const getRadarData = (job) => {
    if (!job) return [];
    return [
      { subject: 'TF-IDF', A: job.tfidf_score, fullMark: 100 },
      { subject: 'Skills', A: job.skill_match.overall_score * 100, fullMark: 100 },
      { subject: 'Experience', A: job.experience_match, fullMark: 100 },
      { subject: 'Education', A: job.education_match, fullMark: 100 }
    ];
  };

  const getMatchColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#17a2b8';
    if (score >= 40) return '#ffc107';
    return '#dc3545';
  };

  return (
    <div className="job-recommendations">
      <div className="recommendations-header">
        <h2>Job Recommendations for {resumeName || 'Your Resume'}</h2>
        <p className="subtitle">Based on keyword analysis and skill matching</p>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <h3>Top 5 Job Matches (Bar Chart)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? '#404040' : '#e9ecef'} />
              <XAxis 
                dataKey="name" 
                angle={-45} 
                textAnchor="end" 
                height={80}
                stroke={isDarkMode ? '#b0b0b0' : '#666'}
              />
              <YAxis stroke={isDarkMode ? '#b0b0b0' : '#666'} />
              <Tooltip 
                contentStyle={{
                  backgroundColor: isDarkMode ? '#2d2d2d' : '#fff',
                  border: `1px solid ${isDarkMode ? '#404040' : '#e9ecef'}`,
                  borderRadius: '8px',
                  color: isDarkMode ? '#fff' : '#333'
                }}
              />
              <Legend 
                wrapperStyle={{ color: isDarkMode ? '#b0b0b0' : '#666' }}
              />
              <Bar dataKey="Match Score" fill="#667eea" />
              <Bar dataKey="TF-IDF" fill="#764ba2" />
              <Bar dataKey="Skills" fill="#f093fb" />
            </BarChart>
          </ResponsiveContainer>
          <p className="chart-tooltip">TF-IDF: Text similarity score based on keyword matching</p>
        </div>

        <div className="chart-container">
          <h3>Match Distribution (Pie Chart)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{
                  backgroundColor: isDarkMode ? '#2d2d2d' : '#fff',
                  border: `1px solid ${isDarkMode ? '#404040' : '#e9ecef'}`,
                  borderRadius: '8px',
                  color: isDarkMode ? '#fff' : '#333'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <p className="chart-tooltip">Percentage distribution of match scores</p>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="recommendations-list">
        <h3>Recommended Jobs ({recommendations.length})</h3>
        {recommendations.map((job, index) => (
          <div
            key={job.job_id}
            className={`recommendation-card ${selectedJob?.job_id === job.job_id ? 'selected' : ''}`}
            onClick={() => setSelectedJob(job)}
          >
            <div className="card-header">
              <div className="job-title-section">
                <h4>{job.job_title}</h4>
                <span className="rank-badge">#{index + 1}</span>
              </div>
              <div className="match-score-large">
                <div className="score-value">{job.overall_match_score}%</div>
                <div className="score-label">Match</div>
              </div>
            </div>
            
            <div className="match-progress-bar">
              <div 
                className="progress-fill" 
                style={{ 
                  width: `${job.overall_match_score}%`,
                  backgroundColor: getMatchColor(job.overall_match_score)
                }}
              />
            </div>
            
            <div className="card-body">
              <div className="job-info">
                <span className="company">🏢 {job.company}</span>
                {job.location && <span className="location">📍 {job.location}</span>}
              </div>
              
              <div className="match-breakdown">
                <div className="breakdown-item">
                  <span className="label">TF-IDF:</span>
                  <span className="value">{job.tfidf_score}%</span>
                </div>
                <div className="breakdown-item">
                  <span className="label">Skills:</span>
                  <span className="value">{job.skill_match.overall_score * 100}%</span>
                </div>
                <div className="breakdown-item">
                  <span className="label">Experience:</span>
                  <span className="value">{job.experience_match}%</span>
                </div>
                <div className="breakdown-item">
                  <span className="label">Education:</span>
                  <span className="value">{job.education_match}%</span>
                </div>
              </div>

              <div className="skills-section">
                <div className="matching-skills">
                  <strong>Matching Skills ({job.skill_match.matching_skills.length}):</strong>
                  <div className="skill-tags">
                    {job.skill_match.matching_skills.slice(0, 5).map((skill, idx) => (
                      <span key={idx} className="skill-tag match">✓ {skill}</span>
                    ))}
                    {job.skill_match.matching_skills.length > 5 && (
                      <span className="skill-more">+{job.skill_match.matching_skills.length - 5} more</span>
                    )}
                  </div>
                </div>
                {job.skill_match.missing_skills.length > 0 && (
                  <div className="missing-skills">
                    <strong>Missing Skills ({job.skill_match.missing_skills.length}):</strong>
                    <div className="skill-tags">
                      {job.skill_match.missing_skills.slice(0, 3).map((skill, idx) => (
                        <span key={idx} className="skill-tag missing">✗ {skill}</span>
                      ))}
                      {job.skill_match.missing_skills.length > 3 && (
                        <span className="skill-more">+{job.skill_match.missing_skills.length - 3} more</span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {job.job_description && (
                <p className="job-description">{job.job_description}</p>
              )}

              <div className="card-actions">
                <button 
                  className="action-btn why-match-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowWhyMatch(prev => ({ ...prev, [job.job_id]: !prev[job.job_id] }));
                  }}
                >
                  {showWhyMatch[job.job_id] ? 'Hide Details' : 'Why This Match?'}
                </button>
                <button 
                  className="action-btn improve-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    const missingSkills = job.skill_match?.missing_skills?.slice(0, 3).join(', ') || 'None';
                    alert(`To improve your match score for this job, focus on:\n\nMissing Skills: ${missingSkills}\n\nConsider adding these skills to your resume!`);
                  }}
                >
                  Improve My Score
                </button>
              </div>

              {showWhyMatch[job.job_id] && (
                <div className="why-match-details">
                  <h5>Match Analysis</h5>
                  <div className="analysis-grid">
                    <div className="analysis-item">
                      <span className="analysis-label">TF-IDF Similarity</span>
                      <span className="analysis-value">{job.tfidf_score}%</span>
                      <p className="analysis-desc">Text-based keyword matching between your resume and job description</p>
                    </div>
                    <div className="analysis-item">
                      <span className="analysis-label">Skills Match</span>
                      <span className="analysis-value">{Math.round(job.skill_match.overall_score * 100)}%</span>
                      <p className="analysis-desc">{job.skill_match.matching_skills.length} skills matched out of {job.skill_match.total_required_count + job.skill_match.total_preferred_count} required</p>
                    </div>
                    <div className="analysis-item">
                      <span className="analysis-label">Experience</span>
                      <span className="analysis-value">{job.experience_match}%</span>
                      <p className="analysis-desc">Alignment with required years of experience</p>
                    </div>
                    <div className="analysis-item">
                      <span className="analysis-label">Education</span>
                      <span className="analysis-value">{job.education_match}%</span>
                      <p className="analysis-desc">Education level compatibility</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Detailed View for Selected Job */}
      {selectedJob && (
        <div className="detailed-view">
          <div className="detailed-header">
            <h3>Detailed Analysis: {selectedJob.job_title}</h3>
            <button className="close-btn" onClick={() => setSelectedJob(null)}>×</button>
          </div>
          
          <div className="radar-chart-container">
            <h4>Match Breakdown (Radar Chart)</h4>
            <ResponsiveContainer width="100%" height={400}>
              <RadarChart data={getRadarData(selectedJob)}>
                <PolarGrid stroke={isDarkMode ? '#404040' : '#e9ecef'} />
                <PolarAngleAxis 
                  dataKey="subject" 
                  tick={{ fill: isDarkMode ? '#b0b0b0' : '#666', fontSize: 12 }}
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]}
                  tick={{ fill: isDarkMode ? '#b0b0b0' : '#666', fontSize: 10 }}
                />
                <Radar
                  name="Match Score"
                  dataKey="A"
                  stroke="#667eea"
                  fill="#667eea"
                  fillOpacity={0.6}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: isDarkMode ? '#2d2d2d' : '#fff',
                    border: `1px solid ${isDarkMode ? '#404040' : '#e9ecef'}`,
                    borderRadius: '8px',
                    color: isDarkMode ? '#fff' : '#333'
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
            <p className="chart-tooltip">4-dimensional analysis: TF-IDF, Skills, Experience, Education</p>
          </div>

          <div className="detailed-stats">
            <div className="stat-card">
              <div className="stat-value">{selectedJob.overall_match_score}%</div>
              <div className="stat-label">Overall Match</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{selectedJob.skill_match.matching_required_count}/{selectedJob.skill_match.total_required_count}</div>
              <div className="stat-label">Required Skills Matched</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{selectedJob.skill_match.matching_preferred_count}/{selectedJob.skill_match.total_preferred_count}</div>
              <div className="stat-label">Preferred Skills Matched</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default JobRecommendations;

