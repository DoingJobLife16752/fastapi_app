import uvicorn
from fastapi import FastAPI
from app.routes import router as user_router

app = FastAPI(title="CRUD API на FastAPI")

app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/info")
def get_info():
    return {
        "app": "devops-test",
        "version": "1.0.0",
        "port": 8000
    }

@app.get("/test")
def test_route():
    return {"status": "success", "message": "Ветка успешно протестирована!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)