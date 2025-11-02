import './LoadingIndicator.css';

function LoadingIndicator() {
  return (
    <div className="loading-indicator">
      <div className="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <p>Assistant is thinking...</p>
    </div>
  );
}

export default LoadingIndicator;

