// draft/components/ResultCard.js
import React from 'react';
import '../styles/ResultCard.css';

function ResultCard({ result }) {
  return (
    <div className="result-card">
      <h3 className="result-title">{result.title}</h3>
      <p className="result-description">{result.description}</p>
      {result.url && (
        <a href={result.url} className="result-link" target="_blank" rel="noopener noreferrer">
          Read more
        </a>
      )}
    </div>
  );
}

export default ResultCard;