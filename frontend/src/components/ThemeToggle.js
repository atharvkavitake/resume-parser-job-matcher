import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './ThemeToggle.css';

function ThemeToggle() {
  const { isDarkMode, toggleTheme } = useTheme();

  return (
    <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle dark mode">
      <div className={`toggle-slider ${isDarkMode ? 'dark' : 'light'}`}>
        <span className="toggle-icon">
          {isDarkMode ? '🌙' : '☀️'}
        </span>
      </div>
      <span className="toggle-label">{isDarkMode ? 'Dark' : 'Light'}</span>
    </button>
  );
}

export default ThemeToggle;



