import { useState, useRef, useEffect } from 'react';
import { chatApi } from '../api/client';
import type { ChatMessage } from '../types';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import './ChatInterface.css';

function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage({
        message: content.trim(),
        thread_id: threadId || undefined,
      });

      if (response.thread_id && !threadId) {
        setThreadId(response.thread_id);
      }

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      const errorResponse: ChatMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
    setThreadId(null);
    setError(null);
  };

  return (
    <div className="chat-interface">
      <div className="chat-container">
        <MessageList
          messages={messages}
          isLoading={isLoading}
          error={error}
        />
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-footer">
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={isLoading}
        />
        <button
          className="clear-button"
          onClick={handleClear}
          disabled={isLoading || messages.length === 0}
        >
          Clear
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;

