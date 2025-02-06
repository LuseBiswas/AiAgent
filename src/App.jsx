import { useState } from "react";
import "./App.css";

function App() {
  const [command, setCommand] = useState('');
  const [results, setResults] = useState([]);

  const handleCommandSubmit = async () => {
    try {
        console.log('Sending command:', command);
        
        const response = await fetch('http://127.0.0.1:8000/api/command/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Unknown error occurred');
        }
        
        if (data.results) {
            setResults(data.results);
        } else {
            throw new Error('No results returned');
        }
    } catch (error) {
        console.error('Error details:', error);
        alert(`Error: ${error.message}`);
    }
};

  return (
    <div>
      <h1>AI Web Automation</h1>
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Enter command"
      />
      <button onClick={handleCommandSubmit}>Submit Command</button>
      
      {results.length > 0 && (
        <div>
          <h3>Top 10 Results:</h3>
          <ul>
            {results.map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
