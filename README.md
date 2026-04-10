## 🎥 Project Demo

[![Watch the Demo](https://img.youtube.com/vi/0mtlrzyjk0A/maxresdefault.jpg)](https://youtu.be/0mtlrzyjk0A) 
# AuditAI - Enterprise Financial Fraud Detection & Risk Scoring Platform

A comprehensive SaaS platform for real-time fraud detection, risk assessment, and financial audit management using machine learning and advanced anomaly detection.

## 🎯 Features

- **Real-time Fraud Detection**: ML-powered fraud scoring for every transaction
- **Risk Assessment**: Comprehensive risk scoring with rule-based + ML hybrid approach
- **Document OCR**: Extract and process invoice/receipt data automatically
- **AI-Powered Insights**: LLM-powered explanations and audit summaries (via OpenRouter)
- **Multi-tenant Architecture**: Support for multiple organizations with role-based access
- **Comprehensive Reporting**: Generate fraud, risk, vendor, and compliance reports
- **Interactive Dashboard**: Real-time metrics, trends, and alerts
- **Alert Management**: Configurable alerts for high-risk and fraudulent transactions

## 📋 Tech Stack

### Backend
- **Framework**: FastAPI 0.115.2 with async support
- **Database**: PostgreSQL 15+ with SQLAlchemy ORM
- **Auth**: JWT with python-jose
- **ML Models**: scikit-learn (Random Forest)
- **Async**: AsyncPG for async database operations
- **Document Processing**: PyTesseract for OCR
- **Reports**: ReportLab for PDF generation
- **AI**: OpenRouter integration for LLM capabilities

### Frontend
- **Framework**: React 18 with TypeScript
- **UI**: Tailwind CSS for styling
- **Build Tool**: Vite for fast development
- **State Management**: Zustand (optional)
- **Charts**: Recharts for data visualization
- **HTTP**: Axios for API requests
- **Icons**: Lucide React for UI icons

### DevOps
- **Migrations**: Alembic for database schema management
- **Package Manager**: pip for Python, npm for Node

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- pip and npm

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configurations

# Create database
createdb auditai

# Run migrations
cd ..
alembic upgrade head

# Generate and train ML models
python train_models.py

# Start backend server
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**Default Credentials**:
- Email: `admin@auditai.com`
- Password: `demo123456`

## 📁 Project Structure

```
AuditAi/
├── backend/                      # FastAPI backend application
│   ├── app/
│   │   ├── main.py              # FastAPI app factory
│   │   ├── config.py            # Settings management
│   │   ├── db/                  # Database layer
│   │   │   ├── base.py          # SQLAlchemy setup
│   │   │   └── session.py       # Session management
│   │   ├── models/              # ORM models (User, Transaction, etc.)
│   │   ├── schemas/             # Pydantic schemas for validation
│   │   ├── api/                 # API route handlers
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── upload.py        # File upload endpoints
│   │   │   ├── audit.py         # Audit analysis endpoints
│   │   │   ├── chatbot.py       # Chatbot/AI endpoints
│   │   │   └── reports.py       # Report generation endpoints
│   │   ├── services/            # Business logic
│   │   │   ├── data_service.py         # CSV/Excel parsing
│   │   │   ├── fraud_service.py        # Fraud detection
│   │   │   ├── risk_service.py         # Risk scoring
│   │   │   ├── audit_service.py        # Audit orchestration
│   │   │   ├── ai_service.py           # LLM integration
│   │   │   ├── ocr_service.py          # Document OCR
│   │   │   └── report_service.py       # Report generation
│   │   └── ai/                  # ML models and artifacts
│   │       ├── fraud_model/     # Fraud detection model
│   │       └── risk_model/      # Risk scoring model
│   ├── alembic/                 # Database migrations
│   ├── .env                     # Environment configuration
│   ├── requirements.txt         # Python dependencies
│   └── alembic.ini             # Alembic configuration
├── frontend/                    # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx             # Main app component
│   │   ├── main.tsx            # Entry point
│   │   ├── index.css           # Global styles
│   │   ├── components/         # Reusable components
│   │   │   ├── Layout.tsx      # Main layout
│   │   │   ├── Sidebar.tsx     # Sidebar navigation
│   │   │   └── Navbar.tsx      # Top navigation
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.tsx   # Dashboard
│   │   │   ├── Upload.tsx      # File upload
│   │   │   ├── Audit.tsx       # Audit results
│   │   │   ├── Reports.tsx     # Report management
│   │   │   ├── Alerts.tsx      # Alert management
│   │   │   ├── Settings.tsx    # Settings
│   │   │   └── Login.tsx       # Login page
│   │   └── services/
│   │       └── api.ts          # API client
│   ├── package.json            # Node dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── tsconfig.json          # TypeScript configuration
│   └── index.html             # HTML entry point
├── notebooks/                 # Jupyter notebooks
│   ├── datagen.py            # Synthetic data generation
│   ├── train_models.py        # Model training notebook
│   └── model_experiments.ipynb # EDA and experiments
├── data/
│   ├── raw/                   # Original data
│   └── processed/             # Processed data
├── storage/                   # File storage
│   ├── uploads/               # Uploaded files
│   └── reports/               # Generated reports
├── logs/                      # Application logs
├── train_models.py            # Model training script
└── README.md                  # This file
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Upload
- `POST /api/upload/csv` - Upload CSV file
- `POST /api/upload/invoice` - Upload invoice document
- `GET /api/upload/status` - Get upload status

### Audit
- `POST /api/audit/run` - Start audit process
- `GET /api/audit/transactions` - List transactions with filters
- `GET /api/audit/transaction/{id}` - Get transaction details
- `GET /api/audit/summary` - Get audit summary
- `GET /api/audit/vendors` - Get vendor risk analysis

### Chatbot
- `POST /api/chatbot/message` - Send chat message
- `POST /api/chatbot/explain/{transaction_id}` - Explain transaction
- `POST /api/chatbot/summarize` - Summarize audit findings

### Reports
- `POST /api/reports/generate/{type}` - Generate report
- `GET /api/reports/list` - List reports
- `GET /api/reports/{id}` - Get report details
- `DELETE /api/reports/{id}` - Delete report

## 🤖 ML Models

### Fraud Detection Model
- **Type**: RandomForestClassifier
- **Features**: Amount, time-based, vendor risk, duplicate flags
- **Output**: Anomaly flag (0/1) + fraud score (0-1)
- **Training**: `train_models.py`

### Risk Scoring Model
- **Type**: RandomForestRegressor + Rule-based hybrid
- **Features**: Amount, time-based, vendor risk, flags
- **Output**: Risk score (0-100) + risk level (Low/Medium/High)
- **Training**: `train_models.py`

## 🔧 Environment Configuration

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/auditai
DATABASE_ASYNC_URL=postgresql+asyncpg://postgres:password@localhost:5432/auditai

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# LLM Services
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_DEFAULT_MODEL=nvidia/llama-3.1-nemotron-70b-instruct

# Storage
STORAGE_PATH=./storage
UPLOAD_DIR=./storage/uploads
REPORT_DIR=./storage/reports

# ML Models
FRAUD_MODEL_PATH=./app/ai/fraud_model/artifacts/fraud_classifier.joblib
RISK_MODEL_PATH=./app/ai/risk_model/artifacts/risk_regressor.joblib
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AuditAI
```

## 📊 Database Schema

### Key Tables
- **organizations**: Multi-tenant organizations
- **users**: User accounts with role-based access
- **vendors**: Vendor master data with risk scores
- **transactions**: Financial transactions with fraud/risk scores
- **documents**: Uploaded invoices/receipts with OCR
- **reports**: Generated audit reports
- **alerts**: High-risk/fraud alerts
- **audit_logs**: Compliance audit trail

## 🧪 Testing

### Run model training
```bash
python train_models.py
```

### Generate test data
```bash
python notebooks/datagen.py
```

### Run backend tests (when added)
```bash
pytest backend/tests/
```

## 📈 Performance

- **Transaction Processing**: ~100-1000 transactions/second (depends on features)
- **Model Inference**: <50ms per transaction
- **API Response Time**: <100ms (p95)
- **Database Queries**: Optimized with indexes on frequently accessed columns

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Audit logging for compliance
- CORS configured for frontend
- Environment-based secrets management

## 🚀 Deployment

### Docker
```bash
# Build and run with Docker Compose
docker-compose up
```

### Production Checklist
- [ ] Set `DEBUG=False` in backend
- [ ] Update `SECRET_KEY` to secure random value
- [ ] Configure PostgreSQL for production
- [ ] Set up HTTPS/TLS certificates
- [ ] Configure OpenRouter API key
- [ ] Set up monitoring and logging
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Train models: `python train_models.py`

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/

## 🐛 Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check port 8000 is available
- Run: `pip install -r requirements.txt`

### Frontend build fails
- Clear node_modules: `rm -rf node_modules`
- Reinstall: `npm install`
- Check Node version: `node --version` (should be 18+)

### Database migration errors
- Check PostgreSQL connection
- Drop and recreate database if needed
- Run: `alembic upgrade head`

### Model training fails
- Ensure training data in `data/processed/`
- Check file permissions
- Verify scikit-learn/joblib installed

## 📄 License

Proprietary - AuditAI Enterprise Platform

## 👥 Support

For issues and support, contact: syedalihasnat929@gmail.com
---

**Version**: 0.1.0  
**Last Updated**: March 2024
