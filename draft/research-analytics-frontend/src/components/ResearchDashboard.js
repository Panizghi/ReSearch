// draft/pages/ResearchDashboard.js
import React, { useState } from 'react';
import axios from 'axios';
import SearchBar from './SearchBar';
import ResultCard from './ResultCard';
import '../styles/ResearchDashboard.css';

function ResearchDashboard() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get('http://127.0.0.1:8000/search_with_scores', {
        params: { query, k: 10 }
      });
      setResults(response.data.results);
      setSuggestions(response.data.suggestions || []);
    } catch (err) {
      setError('An error occurred while searching. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Research Analytics 🧠</h1>
        <p>Search through academic papers and research documents</p>
      </header>

      <SearchBar 
        query={query} 
        setQuery={setQuery} 
        handleSearch={handleSearch} 
      />

      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Searching...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="results-container">
        {results.length > 0 && (
          <div className="results-section">
            <h2>Search Results</h2>
            <div className="results-grid">
              {results.map((result, index) => (
                <ResultCard key={index} result={result} />
              ))}
            </div>
          </div>
        )}

        {suggestions.length > 0 && (
          <div className="suggestions-section">
            <h2>Related Papers</h2>
            <div className="results-grid">
              {suggestions.map((suggestion, index) => (
                <ResultCard key={index} result={suggestion} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResearchDashboard;