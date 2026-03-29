from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, donors, emergency

app = FastAPI(title="LFYHUB API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(donors.router, prefix="/api")
app.include_router(emergency.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to LFYHUB API", "status": "online"}

@app.get("/api/health")
async def api_health():
    return {"status": "api is working"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8081)
