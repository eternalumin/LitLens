# 📚 LitLens - AI-Powered Book Analysis Platform

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-24.0.0-blue.svg)](https://www.docker.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203-ff6b35.svg)](https://groq.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)

## 🚀 Overview

LitLens is an intelligent book analysis platform that transforms how readers engage with literature. By combining state-of-the-art AI with full-stack development best practices, LitLens provides comprehensive book analyses including summaries, character insights, thematic explorations, quotes, discussion questions, and interactive visualizations.

Perfect for students, book clubs, researchers, and literature enthusiasts who want deeper insights beyond surface-level summaries.

## ✨ Features

### 🔍 Intelligent Book Discovery
- Search books by title, author, or ISBN using Open Library API
- Fetch detailed book metadata, covers, and descriptions
- Integration with multiple data sources for comprehensive information

### 🤖 AI-Powered Analysis (Powered by Groq)
- **Comprehensive Summaries**: Detailed overviews and chapter breakdowns
- **Character Analysis**: In-depth profiles with relationships and motivations
- **Theme Extraction**: Identification of major themes and motifs
- **Quote Extraction**: Curated important passages with context
- **Key Terms & Definitions**: Vocabulary building from the text
- **Discussion Questions**: Thought-provoking questions for book clubs or study

### 📊 Interactive Visualizations
- Character relationship networks (NetworkX + Plotly)
- Timeline of story events
- Theme importance radar charts
- Sentiment analysis arcs throughout the narrative
- Geographic maps of story locations (Folium)

### 📄 Multiple Export Formats
- Generate beautifully formatted PDF reports
- Create editable DOCX documents
- Export analysis for sharing or academic use

### 💻 Full-Stack Architecture
- **Backend**: FastAPI (async Python framework) with automatic API documentation
- **Frontend**: Streamlit with custom CSS for professional UI/UX
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for performance optimization
- **NLP**: spaCy for entity extraction and text analysis
- **Deployment**: Docker Compose for easy setup and scaling

### 🔧 Developer-Friendly
- Comprehensive test suite
- GitHub Actions CI/CD pipeline
- Dockerized services for consistent environments
- Environment configuration with python-dotenv
- Modular, maintainable code structure

## 🏗️ Architecture

```plaintext
LitLens/
├── backend/                 # FastAPI backend
│   ├── api/                 # API routes and main app
│   ├── services/            # Business logic (scraping, NLP, Groq integration)
│   ├── models/              # Database models
│   └── utils/               # Helper functions
├── frontend/                # Streamlit frontend
│   ├── components/          # Reusable UI components
│   └── static/              # Custom CSS and assets
├── notebooks/               # Experimental Jupyter notebooks
├── tests/                   # Unit and integration tests
├── docker-compose.yml       # Multi-container deployment
└── .github/workflows/       # CI/CD pipelines
```

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Streamlit + Custom CSS | Interactive web interface |
| **Backend** | FastAPI | High-performance API framework |
| **AI/ML** | Groq API (Llama 3) | Ultra-fast LLM inference |
| **NLP** | spaCy | Named entity recognition, text processing |
| **Database** | PostgreSQL | Persistent data storage |
| **Caching** | Redis | Performance optimization |
| **Visualization** | Plotly, NetworkX, Folium | Interactive charts and graphs |
| **Export** | ReportLab, python-docx | PDF and DOCX generation |
| **DevOps** | Docker, Docker Compose | Containerization and orchestration |
| **CI/CD** | GitHub Actions | Automated testing and deployment |

## 📋 Resume-Worthy Highlights

This project demonstrates proficiency in:

### Backend Development
- Built RESTful APIs with FastAPI and automatic OpenAPI/Swagger documentation
- Implemented asynchronous programming for high concurrency
- Designed relational database schemas with SQLAlchemy ORM
- Integrated third-party APIs (Open Library, Google Books, Groq)
- Implemented caching strategies with Redis
- Applied SOLID principles and modular architecture

### Frontend Engineering
- Created responsive interfaces with Streamlit
- Designed custom CSS for professional appearance
- Implemented state management with Streamlit's session state
- Built reusable components for maintainability
- Added interactive data visualizations

### AI/ML Integration
- Leveraged cutting-edge LLMs via Groq API for text generation
- Implemented NLP pipelines for entity extraction and sentiment analysis
- Designed prompt engineering strategies for consistent outputs
- Combined LLMs with traditional NLP techniques for enhanced accuracy

### DevOps & Infrastructure
- Containerized applications with Docker
- Orchestrated multi-service deployments with Docker Compose
- Configured health checks and resource limits
- Implemented CI/CD pipelines with GitHub Actions
- Managed environment variables and secrets securely

### Data Engineering
- Built web scrapers for multiple data sources
- Implemented data validation and cleaning pipelines
- Designed efficient database queries and indexing strategies
- Applied caching strategies for performance optimization

### Software Engineering Practices
- Wrote comprehensive unit and integration tests
- Followed PEP 8 and Python best practices
- Implemented proper error handling and logging
- Used version control effectively with meaningful commits
- Created comprehensive documentation

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Groq API key (get one at [groq.com](https://groq.com))
- Optional: Python 3.11+ for local development

### Quick Start with Docker
```bash
# Clone the repository
git clone https://github.com/eternalumin/LitLens.git
cd LitLens

# Configure environment variables
cp .env.example .env
# Edit .env to add your Groq API key

# Start all services
docker-compose up --build

# Access the application:
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development
```bash
# Clone the repository
git clone https://github.com/eternalumin/LitLens.git
cd LitLens

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Set up environment
cp .env.example .env
# Edit .env to add your Groq API key

# Start backend
uvicorn backend.api.main:app --reload

# Start frontend (in another terminal)
streamlit run frontend/app.py
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
```
POST /api/v1/books/search     # Search for books
GET  /api/v1/books/{book_id}  # Get book details
POST /api/v1/summary/generate # Generate AI-powered analysis
POST /api/v1/export/pdf       # Export analysis as PDF
POST /api/v1/export/docx      # Export analysis as DOCX
```

## 🧪 Testing

Run the test suite:
```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests  
cd frontend
python -m pytest tests/ -v
```

## 📁 Project Structure

```
LitLens/
├── .github/
│   └── workflows/           # GitHub Actions CI/CD
├── backend/
│   ├── api/                 # FastAPI routes
│   │   ├── main.py          # App entry point
│   │   ├── routes
