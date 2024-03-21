from typing import Union

from fastapi import FastAPI

from routers import user_router, candidate_router

app = FastAPI()
app.include_router(user_router,prefix="/api/users")
app.include_router(candidate_router,prefix="/api/candidates")