// File: src/lib/api-client.ts
// Custom error for better error handling
export class HttpError extends Error {
  response: Response;
  data: any;
  constructor(response: Response, data: any) {
    super(`HTTP Error: ${response.status} ${response.statusText}`);
    this.response = response;
    this.data = data;
  }
}

const api = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  const defaultOptions: RequestInit = {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}${url}`,
    defaultOptions
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new HttpError(response, errorData);
  }

  return response;
};

export default api;