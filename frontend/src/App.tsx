import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import JobPreferences from './components/JobPreferences';
import ApplicationTracker from './components/ApplicationTracker';
import ReportsView from './components/ReportsView';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="bg-blue-600 text-white p-4">
          <h1 className="text-2xl font-bold">AutoAgentHire</h1>
          <p className="text-blue-100">AI-Powered LinkedIn Job Application Automation</p>
        </header>
        
        <nav className="bg-gray-100 p-4">
          <div className="flex space-x-4">
            <a href="/" className="text-blue-600 hover:text-blue-800">Dashboard</a>
            <a href="/preferences" className="text-blue-600 hover:text-blue-800">Job Preferences</a>
            <a href="/applications" className="text-blue-600 hover:text-blue-800">Applications</a>
            <a href="/reports" className="text-blue-600 hover:text-blue-800">Reports</a>
          </div>
        </nav>
        
        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/preferences" element={<JobPreferences />} />
            <Route path="/applications" element={<ApplicationTracker />} />
            <Route path="/reports" element={<ReportsView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;