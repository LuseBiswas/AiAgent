import { useState } from 'react';
import './App.css';

function App() {
  const [command, setCommand] = useState("");

  const handleCommandSubmit = () => {
    // Send the command to the backend (Django) API here
    console.log("Command sent to backend:", command);
  };

  return (
    <div className="App">
      <h1>AI Web Automation</h1>
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Enter command"
      />
      <button onClick={handleCommandSubmit}>Submit</button>
    </div>
  );
}

export default App;
