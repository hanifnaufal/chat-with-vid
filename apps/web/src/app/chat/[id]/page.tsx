"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { LoadingState } from "@/components/custom/LoadingState";
import { chatService } from "@/lib/services/chatService";

export default function ChatPage() {
  const params = useParams();
  const chatId = Array.isArray(params.id) ? params.id[0] : params.id;

  const { data, error, isLoading } = useQuery({
    queryKey: ["chat", chatId],
    queryFn: () => chatService.getChatById(chatId!),
    refetchInterval: (data) => {
      // Stop polling when status is complete or failed
      if (data?.status === "complete" || data?.status === "failed") {
        return false;
      }
      // Poll every 2 seconds as specified in requirements
      return 2000;
    },
    enabled: !!chatId,
  });

  if (!chatId) {
    return <div className="flex min-h-screen items-center justify-center p-4">Invalid chat ID</div>;
  }

  // If processing is completed, we would normally show the chat interface
  // For now, we'll just show a completion message
  if (data?.status === "complete") {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Processing Complete!</h1>
          <p className="mb-4">The video has been analyzed and is ready for chatting.</p>
          <p className="text-sm text-gray-500">In a full implementation, this would show the chat interface.</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <LoadingState status="pending" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <LoadingState 
          status="failed" 
          message="Failed to fetch chat status. Please try again." 
        />
      </div>
    );
  }

  // Calculate current step based on status
  let currentStep = 1;
  if (data?.status === "processing") {
    // Simple simulation - in reality, the backend would provide more detailed progress
    currentStep = 2;
  } else if (data?.status === "complete" || data?.status === "failed") {
    currentStep = 3;
  }

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <LoadingState 
        status={data?.status === "complete" ? "completed" : data?.status === "failed" ? "failed" : "processing"} 
        currentStep={currentStep} 
        totalSteps={3} 
        message={undefined}
      />
    </div>
  );
}