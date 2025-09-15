# Chat with Video Frontend Architecture Document
## Section 1: Template and Framework Selection
#### Template and Framework Selection
Based on the PRD, the project will be a greenfield application built from scratch. No existing starter template is specified. The architecture will be based on the standard create-next-app scaffolding using the Next.js App Router, which is the current industry best practice.

The UI will be built using Shadcn/ui. It's important to note this is not a traditional component library but a collection of reusable, unstyled components built with Radix UI and styled with Tailwind CSS. This gives us full ownership and control over the codebase, aligning with the goal of creating a high-quality portfolio piece.

## Section 2: Frontend Tech Stack
This table defines the specific technologies and versions that are mandatory for the frontend application. These choices are derived from the PRD and UI/UX spec and are optimized for developer experience, performance, and maintainability.

| Category | Technology | Version | Purpose | Rationale |
| --- | --- | --- | --- | --- |
| Framework | Next.js | ^14.2.0 | The core React framework for the application. | Provides a robust, production-grade foundation with server-side rendering, routing, and optimizations. |
| UI Components | Shadcn/ui | ^0.8.0 | A collection of accessible and composable base components. | Aligns with the UI/UX spec. Provides maximum customizability and ownership of the code. |
| State Management | TanStack Query (React Query) | ^5.40.0 | Manages server state, including data fetching, caching, and polling. | The industry standard for handling asynchronous server state. Perfect for the polling required to check video processing status. |
| State Management | Zustand | ^4.5.0 | Manages simple, global client-side state. | A lightweight, simple solution for any minimal global state needed, avoiding the boilerplate of larger libraries. |
| Routing | Next.js App Router | Built-in | Handles all application routing. | Directory-based routing is intuitive and co-locates pages with their logic, improving maintainability. |
| Styling | Tailwind CSS | ^3.4.0 | A utility-first CSS framework for styling. | The required styling engine for Shadcn/ui. It enables rapid development and ensures a consistent design system. |
| Testing | Jest & React Testing Library | Latest | For unit and integration testing of components. | The standard testing stack for React/Next.js, focusing on user-centric testing practices. |
| Icons | Lucide Icons | ^0.390.0 | Provides a clean and modern icon set. | As specified in the UI/UX Specification, integrates perfectly with React. |

## Section 3: Project Structure
A well-organized project structure is critical for maintainability and developer velocity. Based on the monorepo requirement and the use of the Next.js App Router, the following directory structure will be used for the frontend (web) application.

```
apps/web/
├── src/
│   ├── app/                # Next.js App Router for routing and layouts
│   │   ├── layout.tsx        # Root layout (e.g., font setup, theme provider)
│   │   ├── page.tsx          # Home/Input Screen ('/')
│   │   ├── history/
│   │   │   └── page.tsx      # History Screen ('/history')
│   │   └── chat/[id]/
│   │       └── page.tsx      # Dynamic Chat/Analysis Screen ('/chat/{id}')
│   │
│   ├── components/         # All React components
│   │   ├── ui/               # Base components from Shadcn/ui (e.g., button, card)
│   │   └── custom/           # Project-specific components (e.g., ChatWindow, HistoryCard)
│   │
│   ├── lib/                # Non-component logic, services, and utilities
│   │   ├── api-client.ts     # Central API client configuration
│   │   ├── services/         # Service files for API interactions (e.g., chatService.ts)
│   │   ├── hooks.ts          # Custom React hooks
│   │   └── utils.ts          # Utility functions (e.g., date formatting)
│   │
│   ├── store/              # Global client state management (Zustand)
│   │   └── index.ts        # Zustand store definition
│   │
│   └── styles/             # Global CSS styles
│       └── globals.css     # Tailwind CSS base styles and theme variables
│
├── public/                 # Static assets (images, icons, etc.)
├── .env.local              # Local environment variables
├── next.config.js          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
```

## Section 4: Component Standards
To ensure consistency, all React components must adhere to the following standards.

#### Component Template
All new, custom components should follow this structural template. It includes TypeScript for type safety and `React.forwardRef` for composability.

```typescript
// File: src/components/custom/ExampleComponent.tsx
import * as React from "react";
import { cn } from "@/lib/utils"; // Utility for combining Tailwind classes

// 1. Define component-specific props using a TypeScript interface
export interface ExampleComponentProps
  extends React.HTMLAttributes<HTMLDivElement> {
  // Add custom props here
}

// 2. Create the component using React.forwardRef to pass down refs
const ExampleComponent = React.forwardRef<
  HTMLDivElement,
  ExampleComponentProps
>(({ className, children, ...props }, ref) => {
  return (
    // 3. Use the `cn` utility to merge default, variant, and incoming classes
    <div
      className={cn(
        "p-4 border rounded-md", // Base styles
        className // Allows overriding or extending styles from parent
      )}
      ref={ref}
      {...props}
    >
      {children}
    </div>
  );
});
ExampleComponent.displayName = "ExampleComponent";

// 4. Export the component for use in the application
export { ExampleComponent };
```

#### Naming Conventions
- **Component Files**: Must be PascalCase (e.g., ChatWindow.tsx).
- **Component Function Name**: Must match the file name and be PascalCase (e.g., const ChatWindow = ...).
- **Component Folders**: Should be kebab-case when a component requires multiple files.

## Section 5: State Management
Our strategy separates server state from client state.
- **TanStack Query**: Manages all server state (API data, polling, caching).
- **Zustand**: Manages minimal global client state (shared UI state).

#### Store Structure
All global client state logic will be centralized in the src/store/ directory.
```
src/
└── store/
    └── index.ts  # Main Zustand store definition
```

#### State Management Template
This template provides a type-safe structure for creating our Zustand store.
```typescript
// File: src/store/index.ts
import { create } from "zustand";

interface AppState {
  globalError: string | null;
}

interface AppActions {
  setGlobalError: (error: string | null) => void;
}

export const useAppStore = create<AppState & AppActions>((set) => ({
  // Initial state
  globalError: null,

  // Actions
  setGlobalError: (error) => set({ globalError: error }),
}));
```

## Section 6: API Integration
A dedicated service layer will abstract all HTTP requests away from UI components.

#### API Client Configuration
A centralized client handles base URLs, headers, and consistent error handling.
```typescript
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
```

#### Service Template
Services will export functions that correspond to specific backend endpoints.
```typescript
// File: src/lib/services/chatService.ts
import api from "@/lib/api-client";
import { Chat, ChatCreationResponse } from "@repo/shared-types";

export const chatService = {
  async createChat(youtubeUrl: string): Promise<ChatCreationResponse> {
    const response = await api("/api/chats", {
      method: "POST",
      body: JSON.stringify({ url: youtubeUrl }),
    });
    return response.json();
  },

  async getChatById(chatId: string): Promise<Chat> {
    const response = await api(`/api/chats/${chatId}`);
    return response.json();
  },

  async streamChatMessage(
    chatId: string,
    message: string
  ): Promise<Response> {
    const response = await api(`/api/chats/${chatId}/messages`, {
      method: "POST",
      body: JSON.stringify({ message }),
    });
    return response; // Return the raw response for streaming
  },
};
```

## Section 7: Routing
Routing is managed by the Next.js App Router based on the file system structure.

#### Route Configuration
The folder structure within src/app/ defines the application's routes.

#### Route Directory Structure:
```
src/app/
├── page.tsx          # Matches URL: /
├── history/
│   └── page.tsx      # Matches URL: /history
└── chat/[id]/
    └── page.tsx      # Matches URL: /chat/some-unique-id
```

#### Dynamic Route Example:
```typescript
// File: src/app/chat/[id]/page.tsx
type ChatPageProps = {
  params: {
    id: string; // `id` corresponds to the [id] folder name
  };
};

export default function ChatPage({ params }: ChatPageProps) {
  const { id: chatId } = params;

  // Use `chatId` to fetch data for this specific chat
  return (
    <div>
      <h1>Displaying Chat for ID: {chatId}</h1>
      {/* ... chat interface components go here ... */}
    </div>
  );
}
```

## Section 8: Styling Guidelines
#### Styling Approach
Styles will be applied directly within JSX using Tailwind CSS utility classes. The cn utility will be used to conditionally apply and merge classes.

#### Global Theme Variables
The color palette and theme (light/dark mode) are configured in src/styles/globals.css using CSS custom properties.
```css
/* File: src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 249 250 251;
    --foreground: 17 24 39;
    --card: 255 255 255;
    --card-foreground: 17 24 39;
    --primary: 59 130 246;
    --primary-foreground: 249 250 251;
    --destructive: 239 68 68;
    --border: 243 244 246;
    --ring: 59 130 246;
    --radius: 0.5rem;
  }

  .dark {
    --background: 17 24 39;
    --foreground: 249 250 251;
    --card: 31 41 55;
    --card-foreground: 249 250 251;
    --primary: 96 165 250;
    --primary-foreground: 17 24 39;
    --destructive: 248 113 113;
    --border: 55 65 81;
    --ring: 96 165 250;
  }
}
```

## Section 9: Testing Requirements
#### Component Test Template
Tests will be co-located with components and use Jest with React Testing Library.
```typescript
// File: src/components/custom/__tests__/HistoryCard.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { HistoryCard } from "../HistoryCard";

describe("HistoryCard", () => {
  it("should render the video title and channel correctly", () => {
    // Arrange
    const mockProps = {
      title: "Advanced React Patterns",
      channel: "React Conf",
    };
    render(<HistoryCard {...mockProps} />);

    // Assert
    expect(screen.getByText("Advanced React Patterns")).toBeInTheDocument();
    expect(screen.getByText("React Conf")).toBeInTheDocument();
  });
});
```

#### Testing Best Practices
- **MVP Focus on Unit & Integration Tests**: Ensure individual components and pages render and function correctly.
- **Plan for End-to-End (E2E) Tests**: The architecture will be conducive to adding E2E tests with tools like Playwright or Cypress post-MVP.
- **Test User Behavior, Not Implementation**: Tests should verify what the user sees and can do.
- **Follow Arrange-Act-Assert**: Structure tests clearly for readability.
- **Mock External Dependencies**: All frontend tests must run in isolation without making real API calls.

## Section 10: Environment Configuration
The frontend application requires the following environment variable in a .env.local file at the root of the apps/web/ directory.

```bash
# File: apps/web/.env.local

# The base URL for the backend FastAPI server
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**CRITICAL SECURITY NOTE**: The GEMINI_API_KEY is a backend-only secret and must NEVER be prefixed with NEXT_PUBLIC_.

## Section 11: Frontend Developer Standards
The following are critical rules that all development agents must follow:
- **Use the Service Layer for API Calls**: Never use fetch directly in components. All API interactions must go through the functions defined in the lib/services/ directory.
- **Separate Server and Client State**: Use TanStack Query for all server state. Use the Zustand store only for true global UI state.
- **Adhere to Component Standards**: All new components must follow the Component Template defined in Section 4.
- **Follow File Structure Conventions**: Place all files in their designated directories as outlined in the "Project Structure" section.
- **Keep Components Lean**: Components should primarily focus on UI. Extract complex business logic into custom hooks (src/lib/hooks.ts) or service functions.

