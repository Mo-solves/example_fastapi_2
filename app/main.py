from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .middleware.cors import cors_middleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

cors_middleware(app)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
