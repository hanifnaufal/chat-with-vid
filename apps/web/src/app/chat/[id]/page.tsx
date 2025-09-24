"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { LoadingState } from "@/components/custom/LoadingState";
import { chatService, type Chat } from "@/lib/services/chatService";

export default function ChatPage() {
  const params = useParams();
  const chatId = Array.isArray(params.id) ? params.id[0] : params.id;

  const { data, error, isLoading } = useQuery<Chat, Error>({
    queryKey: ["chat", chatId],
    queryFn: () => chatService.getChatById(chatId!),
    // Configure polling interval to 2 seconds as specified in requirements
    refetchInterval: (query) => {
      // Stop polling when status is complete or failed
      if (query.state.data?.status === "complete" || query.state.data?.status === "failed") {
        return false;
      }
      // Poll every 2 seconds to provide timely updates without overwhelming the server
      return 2000;
    },
    // Configure automatic retries for polling
    retry: 3,
    retryDelay: 1000,
    // Only enable polling when we have a valid chatId
    enabled: !!chatId && typeof chatId === 'string',
  });

  if (!chatId || typeof chatId !== 'string') {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-500">Invalid chat ID</h1>
          <p className="mt-2 text-gray-600">The chat ID provided is invalid. Please go back and try again.</p>
        </div>
      </div>
    );
  }

  // If processing is completed, we would normally show the chat interface
  // For now, we'll just show a completion message
  if (data?.status === "complete") {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Processing Complete!</h1>
          <p className="mb-4">The video has been analyzed and is ready for chatting.</p>
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative max-w-md" role="alert">
            <strong className="font-bold">Success! </strong>
            <span className="block sm:inline">The video processing has finished successfully.</span>
          </div>
        </div>
      </div>
    );
  }

  // Show loading state while fetching initial data
  if (isLoading && !data) {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <LoadingState status="pending" />
      </div>
    );
  }

  // Show error state if we have an error and no data
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

  // Determine current step based on actual status from backend
  let currentStep = 1;
  let statusMessage = "";
  
  switch (data?.status) {
    case "processing":
      // In a real implementation, the backend would provide more detailed progress
      // For now, we'll use a default message
      currentStep = 2;
      statusMessage = "Processing your video...";
      break;
    case "failed":
      currentStep = 3;
      break;
    default:
      currentStep = 1;
  }

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <LoadingState 
        status={data?.status || "pending"} 
        currentStep={currentStep} 
        totalSteps={3} 
        message={statusMessage}
      />
    </div>
  );
}