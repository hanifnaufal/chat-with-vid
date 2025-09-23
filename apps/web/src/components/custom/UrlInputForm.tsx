"use client";

import * as React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface UrlInputFormProps extends React.HTMLAttributes<HTMLDivElement> {
  onSubmit: (url: string) => void;
  isLoading?: boolean;
}

const UrlInputForm = React.forwardRef<HTMLDivElement, UrlInputFormProps>(
  ({ className, onSubmit, isLoading = false, ...props }, ref) => {
    const [url, setUrl] = React.useState("");
    const [error, setError] = React.useState("");

    const validateUrl = (input: string): boolean => {
      try {
        const urlObj = new URL(input);
        return urlObj.hostname.includes("youtube.com") || urlObj.hostname.includes("youtu.be");
      } catch {
        return false;
      }
    };

    const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      
      if (!url.trim()) {
        setError("Please enter a YouTube URL");
        return;
      }

      if (!validateUrl(url)) {
        setError("Please enter a valid YouTube URL");
        return;
      }

      setError("");
      onSubmit(url);
    };

    return (
      <Card className={cn("w-full max-w-md", className)} ref={ref} {...props}>
        <CardHeader>
          <CardTitle>Chat with YouTube Video</CardTitle>
          <CardDescription>
            Enter a YouTube URL to start analyzing its content
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Input
                type="url"
                placeholder="https://www.youtube.com/watch?v=..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={isLoading}
                className={error ? "border-red-500" : ""}
              />
              {error && (
                <p className="text-sm text-red-500">{error}</p>
              )}
            </div>
            <Button 
              type="submit" 
              className="w-full" 
              disabled={isLoading}
            >
              {isLoading ? "Processing..." : "Process Video"}
            </Button>
          </form>
        </CardContent>
      </Card>
    );
  }
);

UrlInputForm.displayName = "UrlInputForm";

export { UrlInputForm };