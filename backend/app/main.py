from fastapi import FastAPI

from app.routers import products

app = FastAPI(title="음료수 자판기 API")

# 라우터를 앱에 등록한다
app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "서버가 실행 중입니다"}
