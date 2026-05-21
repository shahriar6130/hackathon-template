import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, authentication
import models, database

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(
    title="Hackathon-Template-Backend",
    description="Backend API with Supabase PostgreSQL",
    version="1.0.0"
)

# Handle CORS - get allowed origins from environment or use defaults
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(authentication.router)
app.include_router(user.router)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "ok",
        "service": "Hackathon-Template-Backend",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Hackathon Template Backend is running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=(environment == "development"),
        log_level="info"
    )