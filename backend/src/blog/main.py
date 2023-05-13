from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base

from .routers import blog, user, authentication

app = FastAPI()

origins = [
    "https://nishithpshetty.gq"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)