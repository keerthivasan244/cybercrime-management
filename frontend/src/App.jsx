import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Upload from './components/Upload';
import GraphView from './components/GraphView';
import Copilot from './components/Copilot';
import Alerts from './components/Alerts';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <header className="bg-white shadow-sm px-8 py-4 mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Investigation Platform</h1>
            <p className="text-sm text-gray-500">AI-Powered Network Discovery</p>
          </div>
          <nav className="space-x-6 text-sm font-medium">
            <Link to="/" className="text-gray-600 hover:text-indigo-600">Dashboard</Link>
            <Link to="/graph" className="text-gray-600 hover:text-indigo-600">Network Graph</Link>
            <Link to="/copilot" className="text-gray-600 hover:text-indigo-600">Copilot</Link>
          </nav>
        </header>
        
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Routes>
            <Route path="/" element={
              <>
                <div className="col-span-1"><Upload /></div>
                <div className="col-span-2"><Alerts /></div>
              </>
            } />
            <Route path="/graph" element={<div className="col-span-3"><GraphView /></div>} />
            <Route path="/copilot" element={<div className="col-span-3"><Copilot /></div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
