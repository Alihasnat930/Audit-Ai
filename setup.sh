#!/bin/bash
# Complete AuditAI Startup Script

set -e  # Exit on error

echo "=========================================="
echo "🚀 AuditAI Complete Startup Guide"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ Node.js/npm is required"; exit 1; }
command -v psql >/dev/null 2>&1 || { echo "⚠️  PostgreSQL client not found (required for database setup)"; }

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Step 1: Backend Setup
echo -e "\n${BLUE}Step 1: Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Setup environment variables
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "# Backend environment variables" > .env
    echo "⚠️  Please configure .env with your database credentials"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Step 2: Frontend Setup
echo -e "\n${BLUE}Step 2: Setting up frontend...${NC}"
cd ../frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Setup environment variables
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cat > .env.local << EOF
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AuditAI
EOF
    echo "✓ Frontend environment configured"
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Step 3: Database Setup
echo -e "\n${BLUE}Step 3: Database configuration...${NC}"
echo "To setup the database, run:"
echo "  1. Ensure PostgreSQL is running"
echo "  2. Update DATABASE_URL in backend/.env"
echo "  3. Run: cd backend && alembic upgrade head"

# Step 4: Train Models
echo -e "\n${BLUE}Step 4: ML Model Training...${NC}"
echo "To train the fraud and risk models, run:"
echo "  python train_models.py"

# Step 5: Start Services
echo -e "\n${BLUE}Step 5: Starting services...${NC}"
echo ""
echo "To start all services, run in separate terminals:"
echo ""
echo -e "${YELLOW}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo -e "${YELLOW}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo -e "${YELLOW}Or use Docker Compose:${NC}"
echo "  docker-compose up"
echo ""

# Final Information
echo -e "${GREEN}=========================================="
echo "✅ Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Setup Database:"
echo "   • Create PostgreSQL database: createdb auditai"
echo "   • Run migrations: alembic upgrade head"
echo ""
echo "2️⃣  Train ML Models:"
echo "   • Generate synthetic data and train: python train_models.py"
echo ""
echo "3️⃣  Start Services:"
echo "   • Backend: python -m uvicorn app.main:app --reload"
echo "   • Frontend: npm run dev"
echo ""
echo "4️⃣  Access Application:"
echo "   • Frontend: http://localhost:5173"
echo "   • API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo "5️⃣  Login with demo credentials:"
echo "   • Email: admin@auditai.com"
echo "   • Password: demo123456"
echo ""
echo -e "${YELLOW}For more information, see README_COMPLETE.md${NC}"
