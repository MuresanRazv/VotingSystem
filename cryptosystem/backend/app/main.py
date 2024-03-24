from fastapi import FastAPI
from routers import user_router, candidate_router, login_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

app.include_router(user_router,prefix="/api/users")
app.include_router(candidate_router,prefix="/api/candidates")
app.include_router(login_router,prefix="/api/login")