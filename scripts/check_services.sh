#!/bin/bash

echo "Checking Docker containers..."
docker-compose ps

echo -e "\nChecking backend health..."
curl -f http://localhost:8000/health || echo "Backend health check failed"

echo -e "\nChecking backend root..."
curl -f http://localhost:8000/ || echo "Backend root check failed"

echo -e "\nChecking database connection..."
docker-compose exec db pg_isready -U user -d splitwise || echo "Database check failed"

echo -e "\nBackend logs (last 20 lines):"
docker-compose logs --tail=20 backend

echo -e "\nDatabase logs (last 10 lines):"
docker-compose logs --tail=10 db
