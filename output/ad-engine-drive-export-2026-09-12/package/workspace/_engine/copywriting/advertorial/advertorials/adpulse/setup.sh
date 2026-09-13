#!/bin/bash
# AdPulse Setup Script
# Run this to install dependencies and set up the database

echo "=== AdPulse Setup ==="

# 1. Install dependencies
echo "Installing dependencies..."
npm install

# 2. Start Docker services (Postgres + Redis)
echo "Starting Docker services..."
docker-compose up -d

# Wait for Postgres to be ready
echo "Waiting for database..."
sleep 5

# 3. Generate Prisma client and push schema
echo "Setting up database..."
npx prisma generate
npx prisma db push

# 4. Seed the database with demo data
echo "Seeding database..."
npx tsx prisma/seed.ts

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To start the dev server:"
echo "  cd adpulse && npm run dev"
echo ""
echo "Login with: demo@adpulse.io / demo123"
echo ""
echo "Or click 'Try Demo Account' on the login page."
