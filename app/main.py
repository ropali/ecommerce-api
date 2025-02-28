from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.orders import router as order_router
from app.api.routes.products import router as product_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="REST API for Ecommerce Platform",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router, prefix=settings.API_V1_STR)
app.include_router(order_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to Ecommerce API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
