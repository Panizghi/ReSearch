import React, { useState } from 'react';
import SearchBar from '../../components/SearchBar';
import ResultCard from '../../components/ResultCard';

function ResearchDashboard() {
  const [results, setResults] = useState([]);

  const handleSearch = async (query) => {
    // TODO: Implement search functionality
    // This will connect to your backend API
    console.log('Searching for:', query);
  };

  return (
    <div className="research-dashboard">
      <h1>Research Dashboard</h1>
      <SearchBar onSearch={handleSearch} />
      <div className="results-container">
        {results.map((result, index) => (
          <ResultCard key={index} result={result} />
        ))}
      </div>
    </div>
  );
}

export default ResearchDashboard; 