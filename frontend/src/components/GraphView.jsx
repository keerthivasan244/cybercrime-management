import React, { useEffect, useState } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import axios from 'axios';

const GraphView = () => {
  const [elements, setElements] = useState([]);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/graph');
        setElements([...res.data.nodes, ...res.data.edges]);
      } catch (e) {
        console.error(e);
      }
    };
    fetchGraph();
  }, []);

  const layout = { name: 'cose' };
  
  const stylesheet = [
    {
      selector: 'node',
      style: {
        'label': 'data(label)',
        'background-color': '#4f46e5',
        'color': '#fff',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': '10px'
      }
    },
    {
      selector: 'edge',
      style: {
        'width': 2,
        'line-color': '#ccc',
        'target-arrow-color': '#ccc',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        'label': 'data(label)',
        'font-size': '8px'
      }
    }
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 h-[600px]">
      <h2 className="text-xl font-bold mb-4">Network Visualization</h2>
      <div className="h-full w-full border border-gray-100 bg-gray-50 rounded">
        <CytoscapeComponent 
            elements={elements} 
            style={{ width: '100%', height: '100%' }} 
            layout={layout}
            stylesheet={stylesheet}
        />
      </div>
    </div>
  );
};

export default GraphView;
