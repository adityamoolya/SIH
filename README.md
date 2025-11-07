# Smart Waste Management System - Backend

A  waste management system developed for **SIH 2025 Internal Round** prototype. This backend handles authentication, waste tracking, reward management, and ML-based waste classification.

## 🎯 Project Overview

This system enables:
- **Households** to track waste disposal and earn reward points
- **Workers** to manage waste pickup schedules
- **Admins** to monitor system-wide analytics
- **IoT Devices** to automatically log waste data
- **ML Classification** to identify waste types and recommend appropriate disposal

## 🏗️ Architecture

The project consists of two main services:

### 1. FastAPI Backend (`/backend`)
- RESTful API for user management, waste logging, and rewards
- JWT-based authentication with role-based access control
- PostgreSQL database with async SQLAlchemy
- Deployed on Railway

### 2. ML Model Service (`/moodel_detection`)
- Flask-based microservice for waste image classification
- TensorFlow/Keras model trained on 6 waste categories
- Containerized with Docker
- Deployed separately on Railway

## 📋 Features

### Authentication & Authorization
- User registration and login (JWT tokens)
- Role-based access: `household`, `worker`, `admin`
- Secure password hashing with bcrypt

### Household Features
- View waste disposal logs
- Track reward points earned
- Automatic point calculation based on waste weight

### Worker Features
- View assigned pickup tasks
- Confirm waste collection
- Update pickup status

### Admin Features
- System-wide analytics dashboard
- Total waste collected metrics
- Active household monitoring
- Device management

### IoT Device Integration
- Automatic waste logging from IoT devices
- Real-time weight and waste type tracking
- Automatic reward point allocation
- Pickup request generation

### ML Waste Classification
- Image-based waste type detection
- 6 categories: cardboard, glass, metal, paper, plastic, trash
- Dustbin recommendation (Blue/Black bin system)
- Confidence score reporting

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM with async support
- **PostgreSQL** - Database (via asyncpg)
- **Passlib** - Password hashing
- **Python-JOSE** - JWT token handling
- **Uvicorn** - ASGI server

### ML Service
- **TensorFlow/Keras** - Deep learning model
- **Flask** - Lightweight web framework
- **Gunicorn** - Production WSGI server
- **PIL/Pillow** - Image processing

## 📁 Project Structure

```
.
├── backend/
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── household.py     # Household-specific endpoints
│   │   ├── worker.py        # Worker-specific endpoints
│   │   ├── admin.py         # Admin-specific endpoints
│   │   ├── device.py        # IoT device endpoints
│   │   └── ml.py            # ML classification proxy
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Database operations
│   ├── database.py          # Database connection setup
│   ├── auth_utils.py        # JWT & authentication helpers
│   ├── password_utils.py    # Password hashing utilities
│   ├── dependencies.py      # FastAPI dependency injection
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile             # Railway deployment config
│   └── runtime.txt          # Python version specification
│
└── moodel_detection/
    ├── app.py                     # Flask ML service
    ├── waste_classifier_model.h5  # Trained Keras model
    ├── requirements.txt           # ML service dependencies
    └── Dockerfile                 # Container configuration
```

## 🔧 Setup & Installation

### Prerequisites
- Python 3.12+
- PostgreSQL database
- Virtual environment (recommended)

### Backend Setup

1. **Clone and navigate to backend**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
MODEL_SERVICE_URL=http://your-ml-service-url/predict
```

5. **Run the server**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### ML Service Setup

1. **Navigate to model directory**
```bash
cd moodel_detection
```

2. **Option A: Local Setup**
```bash
pip install -r requirements.txt
python app.py
```

3. **Option B: Docker Setup**
```bash
docker build -t waste-classifier .
docker run -p 8080:8080 waste-classifier
```

The ML service will be available at `http://localhost:8080`

## 📡 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login and get JWT token

### Household
- `GET /api/household/waste-logs` - View waste disposal history
- `GET /api/household/rewards` - View reward points

### Worker
- `GET /api/worker/pickups` - View assigned pickups
- `POST /api/worker/pickups/confirm/{pickup_id}` - Confirm pickup completion

### Admin
- `GET /api/admin/analytics` - System-wide analytics
- `GET /api/admin/devices` - List all IoT devices

### IoT Device
- `POST /api/device/upload` - Log waste data from device

### ML Classification
- `POST /api/ml/classify-waste` - Classify waste image

## 📊 Database Schema

### Users
- Multi-role support (household, worker, admin)
- Secure password storage
- Contact information

### Devices
- IoT device registration
- Status tracking (online/offline)
- User association

### Waste Logs
- Waste type and weight tracking
- Point calculation
- Timestamp logging

### Pickups
- Worker assignment
- Status tracking (pending/collected)
- Household association

### Rewards
- Point accumulation
- Redemption tracking

## 🤖 ML Model Details

### Classification Categories
1. **Cardboard** → Blue Dustbin (Recyclable)
2. **Glass** → Blue Dustbin (Recyclable)
3. **Metal** → Blue Dustbin (Recyclable)
4. **Paper** → Blue Dustbin (Recyclable)
5. **Plastic** → Blue Dustbin (Recyclable)
6. **Trash** → Black Dustbin (Non-Recyclable)

### Model Architecture
- Base: MobileNetV2 (transfer learning)
- Input: 224x224 RGB images
- Output: 6-class classification with confidence scores

## 🚢 Deployment

### Backend (Railway)
1. Connect GitHub repository
2. Set environment variables in Railway dashboard
3. Railway auto-deploys using `Procfile`

### ML Service (Railway)
1. Create new service from Docker
2. Connect to model directory
3. Railway builds and deploys container

## 🔐 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- CORS middleware configured
- SQL injection prevention via SQLAlchemy ORM

## 🧪 Testing

Test password verification:
```bash
python backend/test_password.py
```

## 📝 Notes

- Frontend is in a separate repository
- This is a prototype for SIH 2025 internal evaluation
- Point system: 1kg waste = 20 points
- First available worker is auto-assigned to pickups

## 🔗 API Documentation

Once running, visit:
- FastAPI Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

**Status**: Prototype for SIH 2025 Internal Round ✅
