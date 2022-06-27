from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

apps = FastAPI()

origins=["*"]

apps.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@apps.get("/")
def root():
    return {"message": "Welcome!"}

apps.include_router(post.router)
apps.include_router(user.router)
apps.include_router(auth.router)
apps.include_router(vote.router)


