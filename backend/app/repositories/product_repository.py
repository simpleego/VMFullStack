# =============================================================================
# repositories/product_repository.py : "SQL 을 실행하는 곳" (DB 와 직접 대화하는 계층)
#
# repository(저장소) 계층의 규칙
#   - SQL 은 오직 이 계층에서만 작성한다. (router, service 에는 SQL 이 없다)
#   - 하는 일은 "DB 에서 꺼내오기 / 저장하기" 뿐이다. 업무 규칙(할인 계산 등)은 넣지 않는다.
#
# 식당으로 비유하면 repository 는 "창고 담당자"이다.
#   주방(service)이 "콜라 목록 주세요"라고 하면 창고(DB)에서 꺼내서 건네주기만 한다.
# =============================================================================

from app.database import get_connection


def find_all():
    """판매 중인 상품 전체를 DB 에서 조회해서 리스트로 돌려준다."""

    # 1) DB 연결 만들기
    conn = get_connection()

    # try ... finally : 중간에 오류가 나더라도 finally 안의 코드는 "반드시" 실행된다.
    #                  -> 오류가 나도 DB 연결을 확실히 끊기 위해 사용한다.
    try:
        # 2) 커서(cursor) 만들기 : SQL 을 DB 에 보내고 결과를 받아오는 도구
        #    with 를 쓰면 블록이 끝날 때 커서가 자동으로 닫힌다.
        with conn.cursor() as cursor:
            # 3) 실행할 SQL 문 (ORM 없이 SQL 을 직접 작성한다)
            #    - SELECT 컬럼들 FROM 테이블 : 테이블에서 원하는 컬럼만 꺼낸다
            #    - WHERE is_active = 1       : 판매 중(1)인 상품만. 판매 중지(0)는 제외
            #    - ORDER BY id               : id 순서(등록 순서)로 정렬
            #    (비밀번호 같은 민감한 컬럼이 없는 products 테이블이라도, 필요한 컬럼만 고르는 습관을 들인다)
            sql = """
                SELECT id, name, price, stock, image_url
                FROM products
                WHERE is_active = 1
                ORDER BY id
            """

            # 4) SQL 실행
            cursor.execute(sql)

            # 5) 결과 가져오기 : 모든 행을 리스트로 받는다.
            #    DictCursor 를 썼기 때문에 [{"id": 1, "name": "콜라", ...}, ...] 모양이다.
            #    이 모양이 2단계에서 하드코딩했던 JSON 과 똑같아서 프론트는 바꿀 필요가 없다.
            return cursor.fetchall()
    finally:
        # 6) 연결 끊기 (성공하든 실패하든 항상 실행된다)
        conn.close()
