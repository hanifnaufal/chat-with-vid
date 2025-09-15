#!/bin/bash

# Start all services in development mode with hot reloading
echo "Starting all services in development mode..."
docker-compose -f docker-compose.dev.yml up -d

echo "Development services started successfully!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Database: postgresql://postgres:postgres@localhost:5432/chat_with_vid"
