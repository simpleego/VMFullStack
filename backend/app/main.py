# =============================================================================
# main.py : 백엔드 서버의 "시작점"
#
# 이 파일이 하는 일
#   1) FastAPI 앱(서버 본체)을 만든다.
#   2) 공통 설정(CORS)을 붙인다.
#   3) 기능별 라우터(주소 목록)를 앱에 연결한다.
#   4) 상품 이미지 폴더를 웹 주소로 공개한다.
#
# 실행 방법 (backend 폴더에서, 가상환경 활성화 후)
#   uvicorn app.main:app --reload
#   -> "app 폴더의 main.py 안에 있는 app 객체를 실행하라"는 뜻이다.
#   -> --reload : 코드를 저장하면 서버가 자동으로 다시 시작된다 (개발할 때만 사용)
# =============================================================================

# 파이썬 표준 라이브러리: 파일/폴더 경로를 다루는 도구
from pathlib import Path

# FastAPI : 웹 API 서버를 만들어 주는 프레임워크
from fastapi import FastAPI
# CORSMiddleware : 다른 주소(출처)의 프론트가 우리 서버를 호출할 수 있게 허락해 주는 장치
from fastapi.middleware.cors import CORSMiddleware
# StaticFiles : 이미지, CSS 같은 "파일"을 그대로 내려주는 장치
from fastapi.staticfiles import StaticFiles

# 우리가 만든 상품 라우터 (app/routers/products.py 파일의 router 를 사용한다)
from app.routers import products

# -----------------------------------------------------------------------------
# 1) 앱(서버 본체) 만들기
#    title 은 API 문서 화면(http://localhost:8000/docs)의 제목으로 표시된다.
#    이 app 객체가 서버 그 자체이며, 아래에서 기능을 하나씩 붙여 나간다.
# -----------------------------------------------------------------------------
app = FastAPI(title="음료수 자판기 API")

# -----------------------------------------------------------------------------
# 2) CORS 설정
#
#    [문제 상황]
#    - 프론트(React)는 http://localhost:5173 에서 실행되고
#    - 백엔드(FastAPI)는 http://localhost:8000 에서 실행된다.
#    주소(출처 = 프로토콜 + 도메인 + 포트)가 다르면, 브라우저는 보안을 위해
#    "다른 출처 서버의 응답을 JavaScript 가 읽는 것"을 기본적으로 막는다.
#    이 규칙이 CORS(Cross-Origin Resource Sharing) 이다.
#
#    [해결 방법]
#    서버가 응답에 "이 출처는 허용한다"는 표시(Access-Control-Allow-Origin 헤더)를
#    붙여 주면 브라우저가 응답을 열어 준다. 그 표시를 붙여 주는 것이 아래 설정이다.
#
#    [주의]
#    - 요청이 서버에 도착하지 않는 것이 아니다. 서버는 정상 처리하지만
#      브라우저가 "응답을 읽지 못하게" 막는 것이다. (개발자도구 Network 탭에서 확인 가능)
#    - 이것은 "브라우저"의 규칙이라 Swagger(/docs)나 curl 로 호출할 때는 발생하지 않는다.
# -----------------------------------------------------------------------------

# 허용할 프론트 주소 (포트 번호까지 정확히 같아야 한다)
# 주의: localhost 와 127.0.0.1 은 브라우저가 서로 다른 출처로 취급한다.
origins = ["http://localhost:5173"]

# 미들웨어 : 모든 요청/응답이 지나가는 "검문소" 같은 것. 응답에 허용 헤더를 붙여 준다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 위에서 정한 프론트 주소만 허용
    allow_methods=["*"],    # 허용할 HTTP 방식 (GET, POST, PUT, DELETE ... 전부)
    allow_headers=["*"],    # 허용할 요청 헤더 (나중에 로그인 토큰 헤더 등을 위해 전부 허용)
)

# -----------------------------------------------------------------------------
# 3) 라우터 연결
#
#    라우터 = "어떤 주소로 요청이 오면 어떤 함수를 실행할지" 적어 둔 목록.
#    products.router 안에는 GET /api/v1/products 가 등록되어 있다.
#    include_router 로 앱에 연결해야 비로소 그 주소가 동작한다.
#    (연결하지 않으면 주소를 만들어 놓아도 404 Not Found 가 나온다)
#
#    기능이 늘어나면(회원, 주문 ...) 라우터 파일을 추가하고 여기에 한 줄씩 연결한다.
#    예) app.include_router(users.router)
# -----------------------------------------------------------------------------
app.include_router(products.router)

# -----------------------------------------------------------------------------
# 4) 상품 이미지 폴더 공개 (정적 파일 서비스)
#
#    이미지는 DB 에 파일 자체를 넣지 않고, 서버 폴더에 두고 "경로(문자열)"만 DB 에 저장한다.
#    브라우저가 이미지를 받으려면 서버가 그 폴더를 웹 주소로 열어 줘야 한다.
#
#      서버 폴더 : backend/products/images/cola.svg
#      웹 주소   : http://localhost:8000/products/images/cola.svg
#
#    폴더 경로 구하는 방법
#      __file__           : 현재 파일(main.py)의 위치      -> backend/app/main.py
#      .resolve()         : 전체 경로(절대경로)로 바꿈
#      .parent            : 한 단계 위 폴더                 -> backend/app
#      .parent.parent     : 두 단계 위 폴더                 -> backend
#      / "products" / ... : 그 아래 폴더로 이동             -> backend/products/images
#    이렇게 main.py 위치를 기준으로 계산하면, 서버를 어느 폴더에서 실행해도 이미지를 찾을 수 있다.
# -----------------------------------------------------------------------------
IMAGE_DIR = Path(__file__).resolve().parent.parent / "products" / "images"

# mount : 특정 주소 아래를 통째로 다른 처리기(여기서는 파일 제공기)에 맡긴다.
#   "/products/images" 로 시작하는 요청은 IMAGE_DIR 폴더에서 같은 이름의 파일을 찾아 돌려준다.
#   (DB 의 image_url 값이 "/products/images/cola.svg" 인 이유가 이것이다)
app.mount("/products/images", StaticFiles(directory=IMAGE_DIR), name="product-images")


# -----------------------------------------------------------------------------
# 서버가 살아 있는지 확인하는 가장 단순한 주소 : GET http://localhost:8000/
#
#   @app.get("/")  : 데코레이터. "GET 방식으로 / 주소가 오면 바로 아래 함수를 실행하라"고 등록한다.
#   return {...}   : 딕셔너리를 돌려주면 FastAPI 가 자동으로 JSON 으로 바꿔 응답한다.
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "서버가 실행 중입니다"}
