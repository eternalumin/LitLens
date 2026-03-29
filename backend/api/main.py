from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routes import books, summary, export

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting LitLens API...")
    yield
    # Shutdown
    print("Shutting down LitLens API...")

app = FastAPI(
    title="LitLens API",
    description="AI-Powered Book Analysis Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(summary.router, prefix="/api/v1/summary", tags=["summary"])
app.include_router(export.router, prefix="/api/v1/export", tags=["export"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to LitLens API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
