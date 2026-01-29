from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import MongoDatabase
from app.api.v1.pitch.route import router as pitch_v1_router
from app.api.v1.connect.route import router as connect_v1_router
from app.api.v1.mentorship.route import router as mentorship_v1_router
from app.api.v1.payment.route import router as payment_v1_router
from app.api.v1.admin.route import router as admin_v1_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    await MongoDatabase.connect()
    yield
    # 🔹 Shutdown
    await MongoDatabase.close()


app = FastAPI(
    title="Rohit Portfolio API",
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Rohit Portfolio API!"}

app.include_router(
    admin_v1_router,
    prefix="/api/v1/admin",
    tags=["Admin v1"]
)

app.include_router(
    pitch_v1_router,
    prefix="/api/v1/pitch",
    tags=["Pitch v1"]
)

app.include_router(
    connect_v1_router,
    prefix="/api/v1/connect",
    tags=["connect v1"]
)


app.include_router(
    mentorship_v1_router,
    prefix="/api/v1/mentorship",
    tags=["mentorship v1"]
)

app.include_router(
    payment_v1_router,
    prefix="/api/v1/payment",
    tags=["payment v1"]
)
