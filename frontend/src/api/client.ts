import axios from 'axios';
import type { ChatRequest, ChatResponse, ConversationHistory } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/api/chat', request);
    return response.data;
  },

  async getConversation(threadId: string): Promise<ConversationHistory> {
    const response = await apiClient.get<ConversationHistory>(
      `/api/conversation/${threadId}`
    );
    return response.data;
  },

  async deleteConversation(threadId: string): Promise<void> {
    await apiClient.delete(`/api/conversation/${threadId}`);
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

