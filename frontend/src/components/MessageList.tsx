import type { ChatMessage } from '../types';
import Message from './Message';
import LoadingIndicator from './LoadingIndicator';
import './MessageList.css';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}

function MessageList({ messages, isLoading, error }: MessageListProps) {
  if (messages.length === 0 && !isLoading && !error) {
    return (
      <div className="message-list empty">
        <div className="empty-state">
          <h2>👋 Welcome to Digital Music Store!</h2>
          <p>Ask me anything about:</p>
          <ul>
            <li>🎵 Music catalog, artists, albums, and songs</li>
            <li>📄 Your invoices and purchase history</li>
            <li>💡 Music recommendations</li>
          </ul>
          <p className="example-text">
            Try: <em>"My customer ID is 1. What albums do you have by U2?"</em>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
      {isLoading && <LoadingIndicator />}
      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}

export default MessageList;

