"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { UrlInputForm } from "@/components/custom/UrlInputForm";
import { chatService } from "@/lib/services/chatService";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (url: string) => {
    setIsLoading(true);
    try {
      const response = await chatService.createChat(url);
      router.push(`/chat/${response.chat_id}`);
    } catch (error: any) {
      console.error("Failed to create chat:", error);
      // In a real implementation, we would show an error message to the user
      // For now, we'll just log it
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <UrlInputForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}
