import type { ChatMessage } from '../types';
import './Message.css';

interface MessageProps {
  message: ChatMessage;
}

function Message({ message }: MessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        <div className="message-role">
          {isUser ? '👤 You' : '🤖 Assistant'}
        </div>
        <div className="message-text">
          {message.content.split('\n').map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
        {message.timestamp && (
          <div className="message-timestamp">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;

