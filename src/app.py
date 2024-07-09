from fastapi import FastAPI
from src.index.router import router as index_router


app = FastAPI()

app.include_router(index_router)
