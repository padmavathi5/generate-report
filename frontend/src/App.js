import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const App = () => {
  const [messages, setMessages] = useState([
    { text: "Hello there! Welcome to Aroma Beans Coffee! How can I help you today?", sender: "bot" }
  ]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
      setIsOpen(true); // Automatically open the chatbot after 2 seconds
    }, 5000); // Show loader for 2 seconds
  }, []);

  const handleSend = () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, sender: "user" }];
      setMessages(newMessages);
      setInput('');
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
        setTimeout(() => {
          const botResponse = `You uploaded a file named ${file.name}. ${response.data.message}`;
          setMessages([...newMessages, { text: botResponse, sender: "bot" }]);
        }, 10000);
      } catch (error) {
        console.error('Error uploading file:', error);
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

  return (
    <div className="app">
      <div className="background"></div>
      {loading ? (
        <div className="loader">
          <img src="https://www.ideagen.com/images/loading-gif.gif" alt="Awesome GIF" width="100" height="100"></img>
        </div>
      ) : (
        <>
          <button className="toggle-button" onClick={() => setIsOpen(!isOpen)}>
            <i className={`fas ${isOpen ? 'fa-times' : 'fa-comments'}`}></i>
          </button>
          {isOpen && (
            <div className="chatbot-container">
              <button className="close-button" onClick={() => setIsOpen(false)}>
                <i className="fa-solid fa-chevron-down"></i>
              </button>
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
                <button onClick={handleSend}>Send</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default App;