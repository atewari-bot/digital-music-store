export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  thread_id?: string;
  customer_id?: string;
}

export interface ChatResponse {
  message: string;
  thread_id: string;
  customer_id?: string;
  agent_name?: string;
}

export interface ConversationHistory {
  thread_id: string;
  messages: ChatMessage[];
  customer_id?: string;
}

