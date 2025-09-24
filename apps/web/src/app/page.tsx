"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { UrlInputForm } from "@/components/custom/UrlInputForm";
import { chatService } from "@/lib/services/chatService";
import { HttpError } from "@/lib/api-client";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (url: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await chatService.createChat(url);
      router.push(`/chat/${response.chat_id}`);
    } catch (error) {
      console.error("Failed to create chat:", error);
      
      // Handle different types of errors
      if (error instanceof HttpError) {
        // API returned an error response
        if (error.response.status === 400) {
          setError("Invalid YouTube URL. Please check the URL and try again.");
        } else if (error.response.status === 500) {
          setError("Server error. Please try again later.");
        } else {
          // Try to get error message from response data
          let message = "Failed to process the video. Please try again.";
          if (error.data && typeof error.data === 'object' && 'message' in error.data) {
            message = error.data.message as string;
          }
          setError(`Error: ${message}`);
        }
      } else if (error instanceof Error) {
        // Network or other error
        setError("Network error. Please check your connection and try again.");
      } else {
        // Unknown error
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <UrlInputForm onSubmit={handleSubmit} isLoading={isLoading} error={error || undefined} />
    </div>
  );
}
