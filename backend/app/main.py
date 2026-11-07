from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import products

app = FastAPI(title="음료수 자판기 API")

# 허용할 프론트 주소 (포트까지 정확히 같아야 한다)
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

# backend/products/images 폴더를 /products/images 주소로 공개한다
# (main.py 기준으로 두 단계 위가 backend 폴더)
IMAGE_DIR = Path(__file__).resolve().parent.parent / "products" / "images"
app.mount("/products/images", StaticFiles(directory=IMAGE_DIR), name="product-images")


@app.get("/")
def root():
    return {"message": "서버가 실행 중입니다"}
