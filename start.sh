#!/bin/bash

# Start all services with Docker Compose
echo "Starting all services..."
docker-compose up -d

echo "Services started successfully!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Database: postgresql://postgres:postgres@localhost:5432/chat_with_vid"
