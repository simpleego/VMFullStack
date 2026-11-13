
from fastapi import FastAPI, HTTPException

import logging

from pydantic import BaseModel, Field

from .database import get_connection
from .product01 import router as search_router

app = FastAPI(title="음료수 자판기 ")
app.include_router(search_router)   # 상품 검색 API (/search/...)


# products = [
#         {"id": 1, "name": "콜라", "price": 1500, "stock": 10, "image_url": "/products/images/cola.svg"},
#         {"id": 2, "name": "사이다", "price": 1400, "stock": 8, "image_url": "/products/images/cider.svg"},
#         {"id": 3, "name": "오렌지주스", "price": 2000, "stock": 0, "image_url": "/products/images/orange.svg"},
#         {"id": 4, "name": "생수", "price": 1000, "stock": 25, "image_url": "/products/images/water.svg"},
#         {"id": 5, "name": "커피", "price": 2500, "stock": 5, "image_url": "/products/images/coffee.svg"},
#         {"id": 6, "name": "녹차", "price": 1800, "stock": 12, "image_url": "/products/images/greentea.svg"},
#     ]

# -----------------------------------------------------------------------------
# 로그 설정
#   level=logging.INFO : INFO 이상(INFO, WARNING, ERROR ...)의 로그를 출력한다. (DEBUG 는 숨김)
#   format             : 한 줄의 모양 -> "시간 [레벨] 로거이름: 메시지"
#   getLogger(__name__): 이 파일 전용 로거. __name__ 은 "app.main" 이 되어 어느 파일의 로그인지 알 수 있다.
# print 와 달리 레벨(중요도)로 걸러 볼 수 있고, 시간 등 정보가 자동으로 붙는다.
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# 요청 본문(JSON) 모양 정의
#   프론트가 보내는 JSON 이 이 모양과 다르면(필드 누락, 타입 틀림, 조건 위반)
#   FastAPI 가 함수 실행 전에 422 오류로 자동 거부한다.
#   id 는 서버가 정하므로 요청에서 받지 않는다.
# -----------------------------------------------------------------------------
class ProductIn(BaseModel):
    name: str = Field(min_length=1)    # 상품 이름 (빈 문자열 금지)
    price: int = Field(ge=0)           # 가격 (ge=0 : 0 이상)
    stock: int = Field(ge=0)           # 재고 (0 이상)
    image_url: str | None = None       # 이미지 경로 (없어도 된다)


def find_all_products():
    # db 작업 준비-> db 연결
    conn = get_connection()
    # SQL 명령어 전송
    try:
        with conn.cursor() as cursor:
            sql = """ SELECT 
                id, NAME, price, stock, image_url 
                FROM products
                WHERE is_active = 1
                ORDER BY price;
            """
            cursor.execute(sql)
            
            return cursor.fetchall()
    finally:
        conn.close()
        
    # SQL 명령어 결과 처리  

# -----------------------------------------------------------------------------
# 상품 1개 조회 함수 (SQL 실행)
#   id 로 상품 1개를 꺼내 딕셔너리로 돌려준다. 없으면 None 을 돌려준다.
# -----------------------------------------------------------------------------
def find_product_by_id(product_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # %s : 값이 들어갈 "빈칸". 값은 execute 의 두 번째 인자로 따로 넘긴다. (파라미터 바인딩)
            #   -> SQL 인젝션 공격을 막아 준다. f-string 으로 SQL 에 직접 이어 붙이지 않는다.
            # 목록과 달리 상세 화면에서는 description(설명)도 함께 꺼낸다.
            sql = """
                SELECT id, name, price, stock, image_url, description
                FROM products
                WHERE id = %s AND is_active = 1
            """
            # (product_id,) : 값이 하나여도 튜플로 넘긴다. 끝의 쉼표를 빼먹지 않는다.
            cursor.execute(sql, (product_id,))

            # ❌ 절대 이렇게 쓰지 않는다
            # sql = f"SELECT ... WHERE id = {product_id}"
            # cursor.execute(sql)
            # SQL Injection 보안 위험이 있음
            # /api/v1/products/1 OR 1=1          → 422 (정수 아님)
            # /api/v1/products/1; DROP TABLE...  → 422


            # fetchone : 한 행만 꺼낸다. 결과가 없으면 None 이다.
            return cursor.fetchone()
    finally:
        conn.close()

@app.get("/")
def root():
    return {"message" : "서버가 실행중입니다"}

@app.get("/products", tags=["product"])
def list_products():
    try:
        logger.info("상품 목록 조회 ")
        # db로부터 상품 목록을 가져오기 SQL
        return find_all_products()
    except Exception as e:
        print(f"[ERROR] 상품 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="상품 목록 조회 에러")


@app.get("/products/{product_id}", tags=["product"])
def get_product(product_id: int):
    # select * from products where product_id = id
    # for product in products:
    #     if product["id"] == product_id:
    #         logger.info("상품 상세 조회 결과 (id=%s) : %s", product_id, product)
    #         return product
    try:
        product = find_product_by_id(product_id)
        
        # 상품이 없는 경우
        logger.info("상품 상세 조회 결과 (id=%s) : 없음", product_id)
    except Exception as e:
        print(f"[ERROR] 상품 상세 조회 실패 id={product_id}: {e}")
        raise HTTPException(status_code=500, detail="상품 상세 조회 에러")
    if product is None:
            raise HTTPException(status_code=500, detail="상품을 찾을 수 없습니다.")
    
    return product

# 상품 등록 1. POST, PUT(모든 필드 수정)
# -----------------------------------------------------------------------------
# 상품 추가 API : POST http://localhost:8000/products
#   status_code=201 : "새로 만들어졌다(Created)"는 뜻의 상태코드
# -----------------------------------------------------------------------------
@app.post("/products", status_code=201, tags=["products"])
def create_product(item: ProductIn):
    # 새 id = 지금 있는 id 중 가장 큰 값 + 1 (상품이 하나도 없으면 1)
    

    # logger.info("상품 추가: %s", new_product)
    return None


# 상품 수정
# -----------------------------------------------------------------------------
# 상품 수정 API : PUT http://localhost:8000/products/1
#   PUT 은 "통째로 교체"한다. 그래서 name, price, stock 을 모두 보내야 한다.
#   id 는 주소에 있는 값을 그대로 유지한다.
# -----------------------------------------------------------------------------
@app.put("/products/{product_id}", tags=["products"])
def update_product(product_id: int, item: ProductIn):
   

    # logger.info("상품 수정 (id=%s): %s", product_id, updated)
    # return updated
    return None


# -----------------------------------------------------------------------------
# 상품 삭제 API : DELETE http://localhost:8000/products/1
#   삭제한 상품을 돌려줘서 무엇이 지워졌는지 확인할 수 있게 한다.
# -----------------------------------------------------------------------------
@app.delete("/products/{product_id}", tags=["products"])
def delete_product(product_id: int):
    
    # logger.info("상품 삭제 (id=%s): %s", product_id, deleted)
    return None

    