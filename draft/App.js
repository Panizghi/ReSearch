import React from 'react';
import logo from './logo.svg';
import './App.css';
import ResearchDashboard from './pages/ResearchDashboard';
import './styles/global.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header>
      <main>
        <ResearchDashboard />
      </main>
    </div>
  );
}

export default App;