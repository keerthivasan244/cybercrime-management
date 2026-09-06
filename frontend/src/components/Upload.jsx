import React, { useState } from 'react';
import axios from 'axios';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [caseId, setCaseId] = useState('');
  const [sourceType, setSourceType] = useState('pdf');
  const [status, setStatus] = useState('');

  const handleUpload = async () => {
    if (!file || !caseId) return;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('case_id', caseId);
    formData.append('source_type', sourceType);

    setStatus('Uploading...');
    try {
      const res = await axios.post('http://localhost:8000/api/upload', formData);
      setStatus(`Success: ${res.data.message}`);
    } catch (e) {
      setStatus(`Error: ${e.message}`);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-bold mb-4">Ingest Evidence</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Case ID</label>
          <input type="text" className="mt-1 block w-full border border-gray-300 rounded-md p-2" value={caseId} onChange={e => setCaseId(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Source Type</label>
          <select className="mt-1 block w-full border border-gray-300 rounded-md p-2" value={sourceType} onChange={e => setSourceType(e.target.value)}>
            <option value="pdf">PDF</option>
            <option value="csv">CSV</option>
            <option value="text">Text/DOCX</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">File</label>
          <input type="file" className="mt-1 block w-full" onChange={e => setFile(e.target.files[0])} />
        </div>
        <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">
          Upload & Process
        </button>
        {status && <p className="text-sm text-gray-600">{status}</p>}
      </div>
    </div>
  );
};

export default Upload;
