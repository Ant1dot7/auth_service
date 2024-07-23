from fastapi import FastAPI

from api.middleware import TimingMiddleware
from api.users.router import router as user_router


app = FastAPI()

app.include_router(user_router)
app.add_middleware(TimingMiddleware)
