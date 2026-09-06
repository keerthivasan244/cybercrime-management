import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await axios.post('http://localhost:8000/api/anomalies/detect');
        setAlerts(res.data.anomalies);
      } catch (e) {
        console.error(e);
      }
    };
    fetchAlerts();
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-bold mb-4">Investigative Leads & Flags</h2>
      <div className="space-y-4">
        {alerts.length === 0 ? <p className="text-gray-500">No anomalies detected.</p> : null}
        {alerts.map(a => (
          <div key={a.id} className="p-4 border-l-4 border-yellow-400 bg-yellow-50 rounded">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-yellow-800">{a.pattern_type}</h3>
                <p className="text-sm text-yellow-700 mt-1">{a.description}</p>
              </div>
              <span className="text-xs font-semibold px-2 py-1 bg-yellow-200 text-yellow-800 rounded">
                {a.severity}
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-2 font-mono">Evidence ID: {a.id} (Human review required)</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Alerts;
