import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:5000/detect", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    setResult(`Result: ${data.result} (${data.confidence}%)`);
  };

  return (
    <div style={{textAlign:"center"}}>
      <h1>Deepfake Detector</h1>
      <input type="file" onChange={(e)=>setFile(e.target.files[0])}/>
      <button onClick={upload}>Check</button>
      <p>{result}</p>
    </div>
  );
}

export default App;
