# =============================================================================
# routers/products.py : "상품" 관련 주소(API)를 모아 둔 파일
#
# router(라우터) 계층의 규칙
#   - 요청을 받고(어떤 주소로 왔는지), 응답을 돌려주는 "창구" 역할만 한다.
#   - 실제 일은 service 에게 맡긴다. (여기에는 SQL 도, 업무 규칙도 쓰지 않는다)
#
# 이번 단계(3단계)에서 바뀐 점
#   2단계 : 이 함수가 하드코딩한 데이터를 직접 들고 있었다.
#   3단계 : service -> repository -> DB 순서로 실제 데이터를 가져온다.
#   그런데도 응답의 "모양"은 같아서 프론트(React)는 한 줄도 수정하지 않았다.
#   -> 계층을 나누면 한 계층이 바뀌어도 다른 계층은 영향을 받지 않는다.
#
# 요청이 흐르는 순서
#   브라우저 -> router(이 파일) -> service -> repository -> MariaDB
#   응답은 반대 방향으로 돌아간다.
# =============================================================================

# HTTPException : 오류 상태코드(404, 500 등)를 응답으로 돌려주기 위한 도구
from fastapi import APIRouter, HTTPException

from app.services import product_service

# prefix 덕분에 아래 주소는 최종적으로 "/api/v1/products" 가 된다.
router = APIRouter(prefix="/api/v1/products", tags=["products"])


# 상품 목록 조회 API : GET /api/v1/products
@router.get("")
def get_products():
    # try ... except : 실행 중 오류가 나면 except 로 이동해서 처리한다.
    try:
        # 일은 service 에게 맡기고, 받은 결과를 그대로 응답한다.
        # (리스트/딕셔너리는 FastAPI 가 자동으로 JSON 으로 바꿔 준다)
        return product_service.get_products()
    except Exception as e:
        # 오류의 자세한 내용(DB 주소, SQL 등)은 보안상 사용자에게 보여 주면 안 된다.
        # -> 서버 터미널에만 출력하고,
        print(f"[ERROR] 상품 조회 실패: {e}")
        # -> 사용자에게는 일반적인 메시지와 500(서버 내부 오류) 상태코드만 돌려준다.
        raise HTTPException(status_code=500, detail="상품 목록을 불러오지 못했습니다.")
