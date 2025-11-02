import { useState, useRef, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🎵 Digital Music Store AI Agent</h1>
        <p>Ask me about music catalog and invoices!</p>
      </header>
      <ChatInterface />
    </div>
  );
}

export default App;

