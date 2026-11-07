# =============================================================================
# services/product_service.py : "업무 규칙"을 담당하는 계층
#
# service 계층의 규칙
#   - router 와 repository 사이에서 "무엇을 할지"를 결정한다.
#   - SQL 은 쓰지 않는다. DB 가 필요하면 repository 에 부탁한다.
#
# 식당으로 비유하면 service 는 "주방장"이다.
#   창구(router)에서 주문이 오면, 창고(repository)에서 재료를 받아 규칙대로 처리한다.
#
# 지금은 업무 규칙이 없어서 repository 의 결과를 그대로 전달만 한다.
# 하지만 나중에 아래와 같은 규칙이 생기면 "이곳"에 추가한다. (router 나 repository 는 건드리지 않는다)
#   예) 품절 상품은 뒤로 정렬한다 / 할인 가격을 계산해서 붙인다
# =============================================================================

from app.repositories import product_repository


def get_products():
    """상품 목록을 돌려준다."""
    # DB 조회는 repository 에게 맡긴다.
    return product_repository.find_all()
