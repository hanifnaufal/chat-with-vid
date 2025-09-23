// File: src/lib/services/chatService.ts
import api from "@/lib/api-client";

export interface ChatCreationResponse {
  chat_id: string;
}

export interface Chat {
  id: string;
  status: "processing" | "complete" | "failed";
  title?: string;
  channel_name?: string;
  publication_date?: string;
  view_count?: number;
  thumbnail_url?: string;
  generated_summary?: string;
  actionable_items?: string[];
  suggested_questions?: string[];
  messages?: ChatMessage[];
}

export interface ChatMessage {
  id: string;
  role: "user" | "ai";
  content: string;
  created_at: string;
}

export const chatService = {
  async createChat(youtubeUrl: string): Promise<ChatCreationResponse> {
    const response = await api("/api/v1/chats", {
      method: "POST",
      body: JSON.stringify({ source_url: youtubeUrl, source_type: "YOUTUBE" }),
    });
    return response.json();
  },

  async getChatById(chatId: string): Promise<Chat> {
    const response = await api(`/api/v1/chats/${chatId}`);
    return response.json();
  },

  async streamChatMessage(
    chatId: string,
    message: string
  ): Promise<Response> {
    const response = await api(`/api/v1/chats/${chatId}/messages`, {
      method: "POST",
      body: JSON.stringify({ message }),
    });
    return response; // Return the raw response for streaming
  },
};