# FastAPI와 순수 JavaScript로 배우는 CORS

자판기 상품 API를 만들고, **같은 요청이 CORS 허용 전후에 어떻게 달라지는지** 브라우저에서 확인하는 실습입니다. MDN의 두 가지 요청 유형을 비교합니다. 별도 헤더 없는 `GET`은 바로 전송되고, `Content-Type: application/json`을 사용하는 교차 출처 `POST`는 브라우저가 `OPTIONS` 사전 요청을 먼저 보냅니다. [MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

| 구성 | 주소 | 역할 |
|---|---|---|
| 프론트엔드 | `http://127.0.0.1:5173` | HTML과 순수 JavaScript로 API 호출 |
| 백엔드 | `http://127.0.0.1:8000` | FastAPI로 상품 목록 조회와 등록 |

호스트는 같지만 **포트가 다르므로 서로 다른 출처**입니다. 실습용 상품은 파이썬 리스트에 저장하며, 서버를 재시작하면 초기 목록으로 돌아갑니다. [FastAPI](https://fastapi.tiangolo.com/tutorial/cors/?utm_source=chatgpt.com)

## 1. 백엔드 작성 — `main.py`

`CORS_ENABLED`를 `False`로 시작합니다. 실습 중에 `True`로 바꾸면, 미들웨어가 프론트엔드 출처를 허용합니다. `max_age=0`은 사전 요청 결과를 캐시하지 않도록 설정해, 버튼을 다시 눌렀을 때도 `OPTIONS`를 관찰할 수 있게 합니다. [FastAPI](https://fastapi.tiangolo.com/tutorial/cors/?utm_source=chatgpt.com)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

CORS_ENABLED = False
FRONTEND_ORIGIN = "http://127.0.0.1:5173"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN] if CORS_ENABLED else [],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    max_age=0,
)

products = [{"id": 1, "name": "콜라", "price": 1500}]


class ProductCreate(BaseModel):
    name: str
    price: int


@app.get("/api/v1/products")
async def get_products():
    return products


@app.post("/api/v1/products", status_code=201)
async def create_product(product: ProductCreate):
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price,
    }
    products.append(new_product)
    return new_product
```

`allow_origins`에는 **API 서버 주소가 아닌, HTML 페이지를 연 프론트엔드 주소**를 넣습니다. 사전 요청의 `OPTIONS`는 `CORSMiddleware`가 처리하므로 별도 라우트를 작성할 필요가 없습니다. [FastAPI](https://fastapi.tiangolo.com/tutorial/cors/?utm_source=chatgpt.com)

## 2. 프론트엔드 작성 — `frontend/index.html`

`frontend` 폴더를 만들고 아래 파일을 저장합니다. 두 버튼 모두 같은 API 주소로 요청하되, `POST` 버튼에만 JSON 요청 본문과 `Content-Type` 헤더를 넣습니다.

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>자판기 CORS 실습</title>
</head>
<body>
  <h1>자판기 CORS 실습</h1>
  <p>개발자 도구의 Network 탭을 열고 버튼을 눌러 보세요.</p>

  <button id="get-products">GET 상품 목록</button>
  <button id="add-product">POST 사이다 등록</button>

  <pre id="result" aria-live="polite">요청 대기 중</pre>

  <script>
    const apiUrl = "http://127.0.0.1:8000/api/v1/products";
    const result = document.querySelector("#result");

    async function requestProducts(options) {
      result.textContent = "요청 중...";

      try {
        const response = await fetch(apiUrl, options);

        if (!response.ok) {
          result.textContent = `HTTP 오류 ${response.status}`;
          return;
        }

        const data = await response.json();
        result.textContent =
          `HTTP ${response.status}\n${JSON.stringify(data, null, 2)}`;
      } catch (error) {
        result.textContent =
          `응답을 읽을 수 없습니다. Console과 Network를 확인하세요.\n${error}`;
      }
    }

    document.querySelector("#get-products").addEventListener("click", () => {
      requestProducts();
    });

    document.querySelector("#add-product").addEventListener("click", () => {
      requestProducts({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "사이다", price: 1300 }),
      });
    });
  </script>
</body>
</html>
```

## 3. 서버 실행

`main.py`가 있는 폴더에서 터미널 두 개를 엽니다.

**터미널 1 — FastAPI**

```bash
python -m pip install fastapi uvicorn
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**터미널 2 — 프론트엔드**

```bash
python -m http.server 5173 --bind 127.0.0.1 --directory frontend
```

브라우저에서 [http://127.0.0.1:5173](http://127.0.0.1:5173)을 열고 **F12 → Network**를 선택합니다. `localhost`로 접속하면 허용 목록의 `127.0.0.1`과 호스트가 달라지므로, 실습에서는 위 주소를 그대로 사용하세요. [FastAPI](https://fastapi.tiangolo.com/tutorial/cors/?utm_source=chatgpt.com)

## 4. CORS 허용 전후 비교

먼저 `CORS_ENABLED = False` 상태에서 두 버튼을 누릅니다. 다음으로 `main.py`에서 `CORS_ENABLED = True`로 바꾸고, Uvicorn이 재시작된 뒤 같은 버튼을 다시 누릅니다.

| 실습 | 서버에서 일어나는 일 | 브라우저 화면 |
|---|---|---|
| **허용 전 `GET`** | `GET`이 도착하고 서버는 `200 OK`를 반환 | 허용 헤더가 없어 JavaScript가 JSON을 읽지 못함 |
| **허용 전 `POST`** | 미들웨어가 `OPTIONS`에 `400`으로 응답. 실제 `POST`는 전송되지 않음 | 등록 실패. 상품도 추가되지 않음 |
| **허용 후 `GET`** | `GET`에 `200 OK`와 CORS 허용 헤더를 반환 | 상품 목록 JSON 표시 |
| **허용 후 `POST`** | `OPTIONS` 허용 후 실제 `POST`가 도착하고 `201 Created`를 반환 | 등록된 사이다 JSON 표시 |

위 결과는 MDN의 단순 요청과 사전 요청 흐름을 FastAPI의 `CORSMiddleware`로 재현한 것입니다. [MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

### Network 탭에서 볼 헤더

`POST` 버튼을 누른 뒤 **`OPTIONS` 요청**을 선택하면 브라우저가 어떤 출처에서 어떤 메서드와 헤더를 사용하려는지 확인할 수 있습니다. [MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

```http
Origin: http://127.0.0.1:5173
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
```

허용 상태에서는 서버의 **응답 헤더**에서 다음 값을 확인할 수 있습니다. [MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

```http
Access-Control-Allow-Origin: http://127.0.0.1:5173
```

실습에서 가장 눈여겨볼 부분은 **서버 로그와 브라우저 결과의 차이**입니다. 허용 전 `GET`은 서버 로그에 `200`이 찍혀도 JavaScript가 응답을 읽을 수 없습니다. 허용 전 `POST`는 `OPTIONS` 단계에서 거부되므로 서버 로그에 실제 `POST`가 찍히지 않습니다. [MDN](https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)
