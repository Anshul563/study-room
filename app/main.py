from fastapi import FastAPI
from app.database import Base, engine
from app.auth.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "AI Study Room Backend Running"
    }