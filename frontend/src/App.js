import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [centerMessage, setCenterMessage] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
      setIsOpen(true);
    }, 2000);
  }, []);

  const handleSend = () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, sender: "user" }];
      setMessages(newMessages);
      setInput('');
      setCenterMessage(false); // Hide the center message when user sends a message
      setTimeout(() => {
        const botResponse = getBotResponse(input);
        setMessages([...newMessages, { text: botResponse, sender: "bot" }]);
      }, 1000);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const newMessages = [...messages, { text: `File uploaded: ${file.name}`, sender: "user" }];
        setMessages(newMessages);
        setCenterMessage(false); // Hide the center message when user uploads a file
        setTimeout(() => {
          const botResponse = `You uploaded a file named ${file.name}. ${response.data.message}`;
          setMessages([...newMessages, { text: botResponse, sender: "bot" }]);
        }, 1000);
      } catch (error) {
        console.error('Error uploading file:', error);
        alert(`Error uploading file: ${error.message}`);
      }
    }
  };

  const getBotResponse = (userInput) => {
    // Simple bot response logic
    if (userInput.toLowerCase().includes("introduce")) {
      return "Hello! I'm the Aroma Beans Coffee chatbot, here to assist you with anything you need regarding our coffee shop. I can answer questions about our menu, location, hours, brewing tips, or anything else you might need to know about Aroma Beans Coffee. Just ask!";
    } else if (userInput.toLowerCase().includes("location")) {
      return "Aroma Beans Coffee is located at 123 Coffee Street, Brewtown.";
    } else {
      return "I'm not sure how to respond to that. Can you please ask something else?";
    }
  };

  const handleClose = () => {
    setMessages([]);
    setIsOpen(false);
  };

  const handleToggle = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setCenterMessage(true); // Show the center message when the chatbot is opened
    }
  };

  return (
    <div className="app">
      <div className="background"></div>
      {loading ? (
        <div className="loader">Loading...</div>
      ) : (
        <>
          <button className="toggle-button" onClick={handleToggle}>
            <i className={`fas ${isOpen ? 'fa-times' : 'fa-comments'}`}></i>
          </button>
          {isOpen && (
            <div className="chatbot-container">
              <div className="chatbot-header">
                <h2>Chatbot</h2>
                <button className="close-button" onClick={handleClose}>
                  <i className="fas fa-times"></i>
                </button>
              </div>
              {centerMessage && (
                <div className="center-message" style={{ color:'#908f8e', padding: '10px', fontStyle: 'italic', textAlign: 'center', position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
                  You can upload any file to summarize your data
                </div>
              )}
              <div className="chatbot">
                {messages.map((message, index) => (
                  <div key={index} className={`message ${message.sender}`}>
                    <p>{message.text}</p>
                  </div>
                ))}
              </div>
              <div className="input-container">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type a message..."
                />
                <label className="upload-icon">
                  <i className="fa-solid fa-paperclip"></i>
                  <input type="file" onChange={handleFileUpload} style={{ display: 'none' }} />
                </label>
                <button onClick={handleSend}>Summarize</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default App;