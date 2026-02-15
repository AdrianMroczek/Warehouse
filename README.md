# 📦 Warehouse Management System

A comprehensive warehouse inventory management application built with Python and DevOps technologies. This project demonstrates a journey from backend development through containerization to cloud orchestration.

## 🎯 Project Overview

The Warehouse Management System is a multi-phase learning project that implements a complete inventory management solution. It features a FastAPI backend with SQLite database, an interactive web interface, automation scripts, and Kubernetes deployments.

## ✨ Features

### Core Functionality
- **Product Management** - Create, update, and manage products and categories
- **Inventory Control** - Track stock quantities with real-time updates
- **Order Processing** - Handle customer orders with stock validation
- **Multi-role Support** - Separate endpoints for Admin, Client, and Employee roles

### Admin Features
- Database seeding with exemplary data
- Full CRUD operations on products and categories

### Client Features
- Browse available products
- Place orders with automatic stock deduction
- Real-time stock availability checking

### Employee Features
- Add and update product information
- Manage inventory quantities
- Create and manage product categories

## 🛠️ Technology Stack

### Backend
- **FastAPI** (0.128.0) - Modern Python web framework
- **Uvicorn** (0.40.0) - ASGI server
- **SQLModel** (0.0.31) - SQL database ORM with type validation
- **SQLAlchemy** (2.0.45) - SQL toolkit

### Frontend
- **Jinja2** (3.1.6) - Template engine
- **HTML5 & Bootstrap 5** - UI styling
- **JavaScript (Fetch API)** - Asynchronous frontend operations

### Database
- **SQLite** - Lightweight relational database

### Utilities
- **Pydantic** (2.12.5) - Data validation
- **Pydantic Settings** (2.12.0) - Configuration management
- **Python Multipart** (0.0.21) - Form data handling

### Deployment & Orchestration
- **Docker** - Application containerization
- **Kubernetes** - Container orchestration (YAML manifests included)

### Testing
- **Playwright** (1.58.0) - Browser automation
- **Pytest Playwright** (0.7.2) - Testing framework
- **Pytest HTML** (4.2.0) - Test reporting

## 📁 Project Structure

```
Warehouse/
├── app/
│   ├── main_warehouse.py    # FastAPI application & endpoints
│   ├── database.py          # SQLModel definitions & database setup
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JavaScript, assets
├── scripts/
│   ├── restock.sh           # CSV-based inventory restocking automation
│   ├── reset_env.sh         # Environment cleanup script
│   └── dostawa.csv          # Sample inventory data
├── k8s/
│   ├── app-deploy.yaml      # Kubernetes Deployment & Service
│   └── db-deploy.yaml       # Persistent Volume for database
├── Dockerfile               # Multi-stage Docker image
└── requirements.txt         # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Docker & Docker Compose (optional, for containerization)
- kubectl & Minikube/Kind (optional, for Kubernetes)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdrianMroczek/Warehouse.git
   cd Warehouse
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main_warehouse:app --reload
   ```
   The API will be available at `http://localhost:8000`

5. **Seed the database (Optional)**
   ```bash
   curl -X POST http://localhost:8000/api/seed
   ```

### Docker Setup

Build and run the application in Docker:

```bash
docker build -t warehouse-app .
docker run -p 8000:8000 warehouse-app
```

### Kubernetes Deployment

Deploy to a Kubernetes cluster:

```bash
kubectl apply -f k8s/db-deploy.yaml
kubectl apply -f k8s/app-deploy.yaml
```

## 🔌 API Endpoints

### Admin Endpoints
- `POST /api/seed` - Seed database with sample data

### Client Endpoints
- `POST /api/products/{product_id}/order` - Place an order for a product

### Employee Endpoints
- `POST /api/employee/products` - Add or update product information
- `GET /api/employee/products` - Retrieve all products

## 💾 Database Schema

### Category Model
- `id` (Primary Key)
- `name` (String, Unique, Indexed)
- `products` (Relationship to Product)

### Product Model
- `id` (Primary Key)
- `name` (String, Indexed)
- `price` (Float)
- `quantity` (Integer)
- `category_id` (Foreign Key)
- `category` (Relationship to Category)

## 🤖 Automation Scripts

### restock.sh
Automates inventory restocking from a CSV file:
```bash
./scripts/restock.sh [csv_file] [api_url]
```
- Reads product data from CSV
- Creates new items or updates existing ones
- Logs all operations to `restock_log.txt`

### reset_env.sh
Cleans up the environment:
```bash
./scripts/reset_env.sh [log_file] [database_file]
```
- Removes database file
- Clears log files
- Useful for development/testing

## 📝 Development

The project serves as a comprehensive learning resource, progressing from:
- Backend development fundamentals
- Database design and ORM usage
- Frontend integration
- Linux shell scripting and automation
- Container technology
- Cloud orchestration with Kubernetes

## 📄 License

This project is provided as-is for educational purposes.

## 👤 Author

Adrian Mroczek

---
