from fastapi import FastAPI

from api.middleware import TimingMiddleware
from api.users.router import router as user_router
from infra.task_iq.broker import broker


app = FastAPI()

app.include_router(user_router)
app.add_middleware(TimingMiddleware)


@app.on_event("startup")
async def app_startup():
    if not broker.is_worker_process:
        await broker.startup()


@app.on_event("shutdown")
async def app_shutdown():
    if not broker.is_worker_process:
        await broker.shutdown()
