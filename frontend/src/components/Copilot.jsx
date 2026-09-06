import React, { useState } from 'react';
import axios from 'axios';

const Copilot = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!question) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/copilot/ask', { question });
      setResponse(res.data);
    } catch (e) {
      console.error(e);
      setResponse({ answer: "Failed to connect to Copilot API." });
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 flex flex-col h-[600px]">
      <h2 className="text-xl font-bold mb-4">AI Investigation Copilot</h2>
      <div className="flex-1 overflow-y-auto mb-4 border p-4 rounded bg-gray-50">
        {response ? (
          <div>
            <p className="font-medium text-gray-800 whitespace-pre-wrap">{response.answer}</p>
            {response.citations && response.citations.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <h4 className="text-sm font-bold text-gray-500 mb-2">Sources (Database Evidence):</h4>
                <ul className="text-xs text-gray-500 space-y-1">
                  {response.citations.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            )}
            {response.cypher_used && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <h4 className="text-sm font-bold text-gray-500 mb-2">Cypher Query:</h4>
                <code className="text-xs bg-gray-200 p-2 rounded block">{response.cypher_used}</code>
              </div>
            )}
          </div>
        ) : (
          <p className="text-gray-400 italic">Ask a question to begin querying the knowledge graph.</p>
        )}
        {loading && <p className="text-blue-500 mt-4">Generating response...</p>}
      </div>
      <div className="flex space-x-2">
        <input 
          type="text" 
          className="flex-1 border border-gray-300 rounded-md p-2"
          placeholder="e.g. Who connects John to the warehouse?"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && ask()}
        />
        <button onClick={ask} className="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">
          Ask
        </button>
      </div>
    </div>
  );
};

export default Copilot;
