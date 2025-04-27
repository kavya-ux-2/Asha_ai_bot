import React, { useState } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [documents, setDocuments] = useState("");

  // Handle document insertion
  const handleInsert = async () => {
    try {
      const docs = documents.split("\n").map((text) => ({ text }));
      const response = await axios.post("http://localhost:5000/insert", { documents: docs });
      alert(response.data.message || "Documents inserted successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to insert documents.");
    }
  };

  // Handle user message submission
  const handleSendMessage = async () => {
    if (!input.trim()) return;
  
    // Add user message to chat
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
  
    try {
      const response = await axios.post("http://localhost:5000/chat", {
        message: input,
      });
  
      const botResponse = response.data.response || "No response received.";
      setMessages([...newMessages, { sender: "bot", text: botResponse }]);
    } catch (error) {
      console.error(error);
      setMessages([...newMessages, { sender: "bot", text: "Error fetching response." }]);
    }
  
    setInput(""); // Clear input
  };
  

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", maxWidth: "600px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center" }}>Asha AI Chatbot</h1>

      {/* Chat Window */}
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "8px",
          padding: "10px",
          height: "400px",
          overflowY: "auto",
          backgroundColor: "#f9f9f9",
          marginBottom: "20px",
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              textAlign: message.sender === "user" ? "right" : "left",
              margin: "10px 0",
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "10px",
                borderRadius: "8px",
                backgroundColor: message.sender === "user" ? "#007bff" : "#e9ecef",
                color: message.sender === "user" ? "#fff" : "#000",
                maxWidth: "70%",
              }}
            >
              {message.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input Field */}
      <div style={{ display: "flex", marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            marginRight: "10px",
          }}
        />
        <button
          onClick={handleSendMessage}
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#007bff",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>

      {/* Document Insertion */}
      <div>
        <h2>Insert Documents</h2>
        <textarea
          rows="5"
          cols="50"
          placeholder="Enter documents (one per line)..."
          value={documents}
          onChange={(e) => setDocuments(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            marginBottom: "10px",
          }}
        />
        <button
          onClick={handleInsert}
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#28a745",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Insert Documents
        </button>
      </div>
    </div>
  );
}

export default App;
