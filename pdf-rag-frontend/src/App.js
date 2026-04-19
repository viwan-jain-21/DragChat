import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isChatting, setIsChatting] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF to upload.");
      return;
    }
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://localhost:8000/upload', formData);
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("Error uploading file. Make sure the backend is running and Ollama is serving the models.");
    }
    setIsUploading(false);
  };

  const handleChat = async () => {
    if (!query) return;
    const currentQuery = query;
    const newMessages = [...messages, { role: 'user', text: currentQuery }];
    setMessages(newMessages);
    setQuery('');
    setIsChatting(true);

    try {
      const res = await axios.post('http://localhost:8000/chat', { query: currentQuery });
      setMessages([
        ...newMessages, 
        { role: 'bot', text: res.data.answer, citations: res.data.citations }
      ]);
    } catch (err) {
      console.error(err);
      setMessages([...newMessages, { role: 'bot', text: 'Error communicating with the chatbot.' }]);
    }
    setIsChatting(false);
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', fontFamily: 'sans-serif', padding: '20px' }}>
      <h2>RAG Chatbot</h2>
      
      <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={isUploading} style={{ padding: '5px 15px', cursor: 'pointer' }}>
          {isUploading ? 'Processing Document...' : 'Upload PDF'}
        </button>
      </div>

      <div style={{ border: '1px solid #ccc', height: '400px', overflowY: 'auto', padding: '15px', marginBottom: '10px', borderRadius: '5px' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.role === 'user' ? 'right' : 'left', margin: '15px 0' }}>
            <div style={{ 
                display: 'inline-block', 
                padding: '12px', 
                borderRadius: '12px', 
                maxWidth: '80%',
                backgroundColor: msg.role === 'user' ? '#007bff' : '#eaeaea', 
                color: msg.role === 'user' ? '#fff' : '#333' 
            }}>
              <div style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</div>
              
              {msg.role === 'bot' && msg.citations && msg.citations.length > 0 && (
                <div style={{ fontSize: '0.8em', marginTop: '10px', color: '#666', borderTop: '1px solid #ccc', paddingTop: '5px' }}>
                  <strong>Sources Used:</strong> Page(s) {msg.citations.join(', ')}
                </div>
              )}
            </div>
          </div>
        ))}
        {isChatting && <div style={{ color: '#888' }}>Bot is typing...</div>}
      </div>

      <div style={{ display: 'flex' }}>
        <input 
          style={{ flex: 1, padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }} 
          value={query} 
          onChange={e => setQuery(e.target.value)} 
          placeholder="Ask a question about the document..." 
          onKeyDown={e => e.key === 'Enter' && handleChat()}
          disabled={isChatting}
        />
        <button onClick={handleChat} disabled={isChatting} style={{ padding: '10px 20px', marginLeft: '10px', cursor: 'pointer' }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;