"use client";

import * as React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface LoadingStateProps extends React.HTMLAttributes<HTMLDivElement> {
  status: "pending" | "processing" | "completed" | "failed";
  currentStep?: number;
  totalSteps?: number;
  message?: string;
}

const LoadingState = React.forwardRef<HTMLDivElement, LoadingStateProps>(
  ({ className, status, currentStep = 1, totalSteps = 3, message, ...props }, ref) => {
    const getStepMessage = () => {
      if (message) return message;
      
      switch (currentStep) {
        case 1:
          return "Fetching transcript...";
        case 2:
          return "Analyzing content...";
        case 3:
          return "Generating summary...";
        default:
          return "Processing...";
      }
    };

    const getStatusMessage = () => {
      switch (status) {
        case "pending":
          return "Starting processing...";
        case "processing":
          return `Step ${currentStep}/${totalSteps}: ${getStepMessage()}`;
        case "completed":
          return "Processing completed!";
        case "failed":
          return "Processing failed. Please try again.";
        default:
          return "Processing...";
      }
    };

    return (
      <Card className={cn("w-full max-w-2xl", className)} ref={ref} {...props}>
        <CardHeader>
          <CardTitle>Processing Video</CardTitle>
          <CardDescription>
            {getStatusMessage()}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col items-center justify-center space-y-4">
          <div className="flex space-x-2">
            {[...Array(totalSteps)].map((_, i) => (
              <div
                key={i}
                className={cn(
                  "h-3 w-3 rounded-full",
                  i < currentStep ? "bg-primary" : "bg-gray-200"
                )}
              />
            ))}
          </div>
          <div className="h-2 w-full max-w-xs overflow-hidden rounded-full bg-gray-200">
            <div
              className={cn(
                "h-full bg-primary transition-all duration-500",
                status === "failed" ? "bg-red-500" : "bg-primary"
              )}
              style={{ width: `${(currentStep / totalSteps) * 100}%` }}
            />
          </div>
          {status === "processing" && (
            <div className="flex items-center space-x-1">
              <div className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.3s]"></div>
              <div className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.15s]"></div>
              <div className="h-2 w-2 animate-bounce rounded-full bg-primary"></div>
            </div>
          )}
        </CardContent>
      </Card>
    );
  }
);

LoadingState.displayName = "LoadingState";

export { LoadingState };