# =============================================================================
# routers/products.py : "상품" 관련 주소(API)를 모아 둔 파일
#
# 라우터(Router)란?
#   "어떤 주소 + 어떤 방식(GET, POST ...)의 요청이 오면, 어떤 함수를 실행할지"를
#   적어 두는 안내 목록이다. 식당으로 비유하면 주문을 받아 주방에 전달하는 "창구"이다.
#
# 기능별로 파일을 나누는 이유
#   products.py(상품), users.py(회원), orders.py(주문) ... 처럼 나누면
#   코드가 길어져도 찾기 쉽고, main.py 가 복잡해지지 않는다.
# =============================================================================

# APIRouter : 주소 목록을 만들기 위한 도구
from fastapi import APIRouter

# -----------------------------------------------------------------------------
# 라우터 만들기
#   prefix : 이 파일의 모든 주소 앞에 자동으로 붙는 공통 접두사
#            -> 아래에서 @router.get("") 이면 최종 주소는 "/api/v1/products" 가 된다.
#   tags   : API 문서(/docs)에서 묶음 이름으로만 쓰인다. 동작에는 영향이 없다.
#
#   주소를 "/api/v1/..." 로 짓는 이유
#     - /api : 화면(HTML)이 아니라 데이터(JSON)를 주고받는 주소라는 표시
#     - /v1  : 버전. 나중에 API 모양이 크게 바뀌면 /v2 를 만들어 옛 버전도 함께 유지할 수 있다.
#     - /products : 다루는 대상(상품)을 "복수 명사"로 쓰는 것이 REST API 의 관례
#
#   이 router 는 main.py 의 app.include_router(products.router) 로 앱에 연결된다.
# -----------------------------------------------------------------------------
router = APIRouter(prefix="/api/v1/products", tags=["products"])


# -----------------------------------------------------------------------------
# 상품 목록 조회 API : GET /api/v1/products
#
#   @router.get("")
#     - 데코레이터. 바로 아래 함수를 "GET 방식, prefix 뒤에 아무것도 없는 주소" 요청의 처리 함수로 등록한다.
#     - 등록은 서버가 시작될 때(파일을 불러올 때) 한 번 끝난다. 요청이 올 때마다 만드는 것이 아니다.
#     - GET 은 "데이터를 조회한다"는 뜻의 HTTP 방식이다. (브라우저 주소창 입력도 GET 이다)
#
#   요청이 처리되는 흐름
#     브라우저 fetch("/api/v1/products")
#       -> Uvicorn 이 요청을 받음
#       -> FastAPI 가 등록된 목록에서 이 주소를 찾아 get_products() 를 호출
#       -> 함수가 돌려준 값을 FastAPI 가 JSON 으로 바꿔 응답(상태코드 200)
#
#   함수 이름(get_products)은 아무거나 지어도 되지만, 무엇을 하는지 알 수 있게 짓는다.
# -----------------------------------------------------------------------------
@router.get("")
def get_products():
    # [현재 단계] 아직 DB 가 없으므로 코드에 박아 둔(하드코딩) 데이터를 그대로 돌려준다.
    # [다음 단계] 3단계에서 이 부분을 DB 조회(SELECT)로 교체한다.
    #             그래도 아래와 "같은 모양"의 데이터를 돌려주기 때문에 프론트는 수정할 필요가 없다.
    #             (API 의 응답 모양 = 프론트와 백엔드 사이의 약속)
    #
    # 파이썬의 리스트([])와 딕셔너리({})를 돌려주면 FastAPI 가 알아서 JSON 으로 변환한다.
    # 각 항목의 의미
    #   id        : 상품 번호
    #   name      : 상품 이름
    #   price     : 가격(원)
    #   stock     : 재고 수량 (0 이면 프론트에서 "품절"로 표시)
    #   image_url : 이미지 경로. main.py 에서 공개한 /products/images 폴더의 파일을 가리킨다.
    return [
        {"id": 1, "name": "콜라", "price": 1500, "stock": 10, "image_url": "/products/images/cola.svg"},
        {"id": 2, "name": "사이다", "price": 1400, "stock": 8, "image_url": "/products/images/cider.svg"},
        {"id": 3, "name": "오렌지주스", "price": 2000, "stock": 0, "image_url": "/products/images/orange.svg"},
        {"id": 4, "name": "생수", "price": 1000, "stock": 25, "image_url": "/products/images/water.svg"},
        {"id": 5, "name": "커피", "price": 2500, "stock": 5, "image_url": "/products/images/coffee.svg"},
        {"id": 6, "name": "녹차", "price": 1800, "stock": 12, "image_url": "/products/images/greentea.svg"},
    ]
