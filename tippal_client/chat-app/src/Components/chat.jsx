import React, { useState } from "react";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [mode, setMode] = useState("ask"); // 'ask' or 'add'

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { text: inputValue, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue("");

    try {
      let endpoint, body;
      if (mode === "ask") {
        endpoint = "http://localhost:5000/query";
        body = JSON.stringify({ query: inputValue });
      } else if (mode === "add") {
        endpoint = "http://localhost:5000/insert";
        body = JSON.stringify({ data: inputValue });
      }

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
      });

      const data = await response.json();
      const botMessage = { text: data.result, sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const toggleMode = () => {
    setMode((prevMode) => (prevMode === "ask" ? "add" : "ask"));
  };

  return (
    <div style={styles.chatContainer}>
      <div style={styles.chatWindow}>
        <div style={styles.messagesContainer}>
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                ...styles.messageBubble,
                alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                backgroundColor: msg.sender === "user" ? "#009BC0" : "#f1f1f1",
                color: msg.sender === "user" ? "#fff" : "#000",
              }}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div style={styles.inputContainer}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            style={styles.input}
            placeholder={mode === "ask" ? "Ask a question..." : "Add tips or feedback..."}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          />
          <button onClick={handleSendMessage} style={styles.sendButton}>
            Send
          </button>
        </div>
        <button onClick={toggleMode} style={styles.modeButton}>
          Switch to {mode === "ask" ? "Add tips or feedback" : "Ask Question"}
        </button>
      </div>
    </div>
  );
};

const styles = {
  chatContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f8f9fa",
  },
  chatWindow: {
    display: "flex",
    flexDirection: "column",
    width: "400px",
    height: "600px",
    backgroundColor: "#fff",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    overflow: "hidden",
  },
  messagesContainer: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    backgroundImage: "url('/logo.png')", 
    backgroundSize: "cover", 
    backgroundPosition: "center", 
    backgroundRepeat: "no-repeat", 
    opacity: 0.3, // Lower opacity for the background
    position: "relative", // Ensure messages are positioned correctly
  },

messageBubble: {
  padding: "10px 15px",
  borderRadius: "15px",
  maxWidth: "70%",
  wordWrap: "break-word",
  backgroundColor: "rgba(255, 255, 255, 0.8)", // Semi-transparent white background
  opacity:0.9,
},
  inputContainer: {
    display: "flex",
    padding: "10px",
    borderTop: "1px solid #ddd",
    backgroundColor: "##009BC0",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ddd",
    outline: "none",
  },
  sendButton: {
    padding: "10px 20px",
    marginLeft: "10px",
    borderRadius: "5px",
    border: "none",
    backgroundColor: "#009BC0",
    color: "#fff",
    cursor: "pointer",
    outline: "none",
  },
  modeButton: {
    padding: "10px",
    border: "none",
    backgroundColor: "#CFCFCF",
    color: "#009BC0",
    cursor: "pointer",
    outline: "none",
    textAlign: "center",
  },
};

export default Chat;