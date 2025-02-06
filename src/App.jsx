import { useState } from "react";
import "./App.css";

function App() {
  const [command, setCommand] = useState("");

  const handleCommandSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/command/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ command }),
      });
      const data = await response.json();
      console.log(data.message);
      alert(data.message);
    } catch (error) {
      console.error("Error sending command:", error);
    }
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
