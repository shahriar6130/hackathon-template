from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, authentication
import models, database  # Fixed line here

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Hackathon-Template-Backend")

# Handle CORS issues
origins = [
    "http://localhost:5173",      # Your Vite dev server
    "http://127.0.0.1:5173",      # Sometimes needed
    "http://localhost",           # Extra safety
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,       
    allow_methods=["*"],          
    allow_headers=["*"],          
)

# Routers
app.include_router(authentication.router)
app.include_router(user.router)