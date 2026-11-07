from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("")
def get_products():
    # 아직 DB가 없으므로 코드에 박아 둔 데이터를 그대로 돌려준다
    return [
        {"id": 1, "name": "콜라", "price": 1500, "stock": 10, "image_url": "🥤"},
        {"id": 2, "name": "사이다", "price": 1400, "stock": 8, "image_url": "🧃"},
        {"id": 3, "name": "오렌지주스", "price": 2000, "stock": 0, "image_url": "🍊"},
        {"id": 4, "name": "생수", "price": 1000, "stock": 25, "image_url": "💧"},
        {"id": 5, "name": "커피", "price": 2500, "stock": 5, "image_url": "☕"},
        {"id": 6, "name": "녹차", "price": 1800, "stock": 12, "image_url": "🍵"},
    ]
