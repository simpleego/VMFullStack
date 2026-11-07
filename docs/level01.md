# Level 01 - 상품 목록 조회 (프론트 → 백엔드 → DB)

첫 기능 **"상품 목록 조회"** 를 가짜 데이터에서 시작해 실제 DB까지 한 계층씩 연결한다.
수강 시간 기준: 12일 일정의 1~2일차 (약 4시간)

| 단계 | 주제 | 핵심 개념 | 예상 시간 |
|:--:|------|-----------|:--:|
| 0 | 개발환경 설정 | 폴더 구조, 가상환경, Vite, Git | 50분 |
| 1 | 가짜 데이터로 화면 | 컴포넌트, props, `useState` | 50분 |
| 2 | 백엔드 연결 | FastAPI, `useEffect`+`fetch`, CORS | 70분 |
| 3 | DB 연결 | MariaDB, SQL, `repositories` 계층 | 70분 |

> 이 문서의 코드는 **강의 진행용 정답 코드**다. 강사가 화면에서 직접 타이핑하며 설명하고, 수강생이 따라 입력한다.
> 코드는 작성만 했고 실제 실행 검증은 하지 않았다. 수업 전에 강사 PC에서 한 번 끝까지 따라 해 보길 권한다.

---

## 0단계: 개발환경 설정

### 학습 목표
- 풀스택 프로젝트의 폴더 구조를 이해한다.
- 프론트(Node), 백엔드(Python), DB(MariaDB) 세 가지 실행 환경을 준비한다.

### 0-1. 사전 설치 확인 (PowerShell)
```powershell
python --version      # 3.11 이상
node --version        # LTS (20 이상)
npm --version
git --version
mariadb --version     # 또는 mysql --version (설치된 클라이언트 이름)
```
- 설치되어 있지 않은 항목은 먼저 설치한다. (VS Code도 권장)
- MariaDB 서비스가 실행 중인지 확인: `Win + R` → `services.msc` → MariaDB 항목이 "실행 중"

### 0-2. 프로젝트 폴더 만들기
```powershell
cd D:\AX_WORK\VMFullStack
mkdir db
mkdir backend
git init
```

최종 구조(이번 레벨 완료 시):
```
VMFullStack/
├─ docs/
├─ db/
│  ├─ init.sql
│  ├─ schema.sql
│  └─ seed.sql
├─ backend/
│  ├─ .env / .env.example
│  ├─ requirements.txt
│  ├─ products/images/   (상품 이미지: cola.svg 등, 준비되어 있음)
│  └─ app/
│     ├─ main.py
│     ├─ database.py
│     ├─ routers/products.py
│     ├─ services/product_service.py
│     └─ repositories/product_repository.py
└─ frontend/        (Vite가 생성)
   └─ src/
      ├─ App.jsx
      ├─ api/products.js
      └─ components/ProductCard.jsx
```

### 0-3. .gitignore 만들기
프로젝트 루트에 `.gitignore`:
```gitignore
# Python
.venv/
__pycache__/
*.pyc

# Node
node_modules/
dist/

# 환경변수 (비밀번호가 들어 있으므로 커밋 금지)
.env
```

### 0-4. 백엔드 환경 (Python 가상환경)
```powershell
cd D:\AX_WORK\VMFullStack\backend
python -m venv .venv
.venv\Scripts\Activate.ps1
```
- 프롬프트 앞에 `(.venv)`가 보이면 성공.
- 실행 정책 오류가 나면 한 번만 실행: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

```powershell
pip install fastapi "uvicorn[standard]" pymysql python-dotenv
pip freeze > requirements.txt
```

| 패키지 | 역할 |
|--------|------|
| fastapi | 웹 API 프레임워크 |
| uvicorn | FastAPI를 실제로 실행하는 서버 |
| pymysql | Python에서 MariaDB에 접속하는 드라이버 (ORM 아님) |
| python-dotenv | `.env` 파일의 설정값 읽기 |

### 0-5. 프론트엔드 환경 (Vite + React)
```powershell
cd D:\AX_WORK\VMFullStack
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm run dev
```
- 브라우저에서 `http://localhost:5173`에 Vite + React 기본 화면이 보이면 성공. 확인 후 `Ctrl + C`로 종료한다.
- 질문이 나오면 기본 선택(JavaScript)을 사용한다. 템플릿 종류가 다르게 나오면 `React` + `JavaScript`를 고른다.

### 0-6. 첫 커밋
```powershell
cd D:\AX_WORK\VMFullStack
git add .
git commit -m "Level01 Step0: 개발환경 설정"
```

### ✅ 0단계 체크포인트
- [ ] `(.venv)` 가상환경이 활성화된다.
- [ ] `http://localhost:5173`에 Vite 기본 화면이 뜬다.
- [ ] MariaDB 서비스가 실행 중이다.
- [ ] `git log`에 커밋이 보인다.

### 강의 포인트 / 자주 나는 오류
- "왜 세 개의 환경이 필요한가?" 프론트(브라우저에서 실행), 백엔드(서버에서 실행), DB(데이터 저장)의 역할을 그림으로 먼저 설명한다.
- `python` 명령이 없다고 나오면 설치 시 "Add to PATH"를 놓친 경우가 많다.
- 이후 모든 백엔드 작업은 **가상환경이 활성화된 터미널**에서 한다.

---

## 1단계: 가짜 데이터로 화면 먼저 (프론트)

### 학습 목표
- 컴포넌트를 나누고 props로 데이터를 전달한다.
- `useState`로 화면 데이터를 관리한다.
- 아직 백엔드/DB 없이 **코드에 박아 둔 배열**로 목록을 그린다.

### 1-1. 기본 파일 정리
Vite가 만든 샘플 스타일을 제거한다.

`frontend/src/index.css` 전체를 다음으로 교체:
```css
body {
  margin: 0;
  font-family: "Malgun Gothic", sans-serif;
  background: #f5f5f5;
}
```

`frontend/src/App.css` 전체를 다음으로 교체:
```css
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 16px;
}

.title {
  text-align: center;
}

.toolbar {
  text-align: right;
  margin-bottom: 12px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.message {
  text-align: center;
  color: #666;
  padding: 40px 0;
}

.message.error {
  color: #d32f2f;
}
```

### 1-2. 상품 카드 컴포넌트
`frontend/src/components/ProductCard.jsx` (새 파일, `components` 폴더도 새로 만든다)
```jsx
import "./ProductCard.css";

// props: 부모(App)가 넘겨준 상품 정보 객체
function ProductCard({ product }) {
  const soldOut = product.stock === 0;

  return (
    <div className={soldOut ? "card sold-out" : "card"}>
      <div className="card-image">{product.image_url}</div>
      <h3 className="card-name">{product.name}</h3>
      <p className="card-price">{product.price.toLocaleString()}원</p>
      <p className="card-stock">
        {soldOut ? "품절" : `재고 ${product.stock}개`}
      </p>
    </div>
  );
}

export default ProductCard;
```

`frontend/src/components/ProductCard.css`
```css
.card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.card-image {
  font-size: 56px;
}

.card-name {
  margin: 8px 0 4px;
}

.card-price {
  font-weight: bold;
  margin: 4px 0;
}

.card-stock {
  color: #388e3c;
  margin: 4px 0;
}

.card.sold-out {
  opacity: 0.5;
}

.card.sold-out .card-stock {
  color: #d32f2f;
  font-weight: bold;
}
```
> 1단계에서는 학습 단순화를 위해 `image_url`에 이모지 문자를 넣어 사용한다. 2단계(2-7)에서 서버의 실제 이미지 파일(`products/images`)로 교체한다.

### 1-3. App 컴포넌트 (가짜 데이터 + useState)
`frontend/src/App.jsx` 전체를 다음으로 교체:
```jsx
import { useState } from "react";
import "./App.css";
import ProductCard from "./components/ProductCard";

// 가짜 데이터: 나중에 백엔드/DB에서 받아올 데이터와 같은 모양으로 만든다
const fakeProducts = [
  { id: 1, name: "콜라", price: 1500, stock: 10, image_url: "🥤" },
  { id: 2, name: "사이다", price: 1400, stock: 8, image_url: "🧃" },
  { id: 3, name: "오렌지주스", price: 2000, stock: 0, image_url: "🍊" },
  { id: 4, name: "생수", price: 1000, stock: 25, image_url: "💧" },
  { id: 5, name: "커피", price: 2500, stock: 5, image_url: "☕" },
  { id: 6, name: "녹차", price: 1800, stock: 12, image_url: "🍵" },
];

function App() {
  // products: 현재 값, setProducts: 값을 바꾸는 함수
  const [products, setProducts] = useState(fakeProducts);

  return (
    <div className="container">
      <h1 className="title">🥤 음료수 자판기</h1>

      {/* useState 체험용 버튼: 상태가 바뀌면 화면이 다시 그려진다 */}
      <div className="toolbar">
        <button onClick={() => setProducts([])}>목록 비우기</button>{" "}
        <button onClick={() => setProducts(fakeProducts)}>목록 채우기</button>
      </div>

      {products.length === 0 ? (
        <p className="message">상품이 없습니다.</p>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
```

### 실행 확인
```powershell
cd D:\AX_WORK\VMFullStack\frontend
npm run dev
```
- 상품 카드 6개가 보이고, "품절" 카드는 흐리게 표시된다.
- "목록 비우기" / "목록 채우기" 버튼으로 화면이 바뀐다.

```powershell
git add .
git commit -m "Level01 Step1: 가짜 데이터로 상품 목록 화면"
```

### ✅ 1단계 체크포인트
- [ ] 카드 6개가 표시되고 재고 0인 상품은 "품절"로 보인다.
- [ ] 버튼 클릭으로 목록이 사라졌다 나타난다.
- [ ] `ProductCard`가 별도 파일로 분리되어 있다.

### 강의 포인트
- **props**: 부모 → 자식으로 데이터가 흐른다. `ProductCard`는 받은 데이터를 그리기만 한다.
- **useState**: 일반 변수를 바꾸면 화면이 안 바뀌지만, state를 바꾸면 다시 그려진다. (`let products = []`로 바꿔 보는 실험을 추천)
- **key**: 목록 렌더링 시 `key`가 왜 필요한지 설명한다.
- 가짜 데이터의 모양(`id, name, price, stock, image_url`)은 **이후 API 응답과 같은 모양**이라는 점을 강조한다. 그래서 3단계에서 프론트를 고치지 않아도 된다.

---

## 2단계: 백엔드 연결

### 학습 목표
- FastAPI로 `GET /api/v1/products` API를 만든다. (우선 하드코딩 JSON)
- React에서 `useEffect` + `fetch`로 호출한다.
- **CORS 오류를 직접 겪고 해결한다.**

### 2-1. FastAPI 서버 최소 실행 확인
`backend/app/main.py` (새 파일, `app` 폴더도 새로 만든다)
```python
from fastapi import FastAPI

app = FastAPI(title="음료수 자판기 API")


@app.get("/")
def root():
    return {"message": "서버가 실행 중입니다"}
```

```powershell
cd D:\AX_WORK\VMFullStack\backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
- `http://localhost:8000` → `{"message":"서버가 실행 중입니다"}`
- `http://localhost:8000/docs` → Swagger 문서 화면 (자동 생성됨을 보여 준다)

### 2-2. 상품 목록 API (하드코딩)
`backend/app/routers/products.py` (새 파일, `routers` 폴더도 새로 만든다)
```python
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
```

`backend/app/main.py` 전체를 다음으로 교체:
```python
from fastapi import FastAPI

from app.routers import products

app = FastAPI(title="음료수 자판기 API")

# 라우터를 앱에 등록한다
app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "서버가 실행 중입니다"}
```
- Swagger(`/docs`)에서 `GET /api/v1/products`를 "Try it out"으로 실행해 JSON이 나오는지 확인한다.

### 2-3. 프론트에서 API 호출 함수 분리
`frontend/src/api/products.js` (새 파일, `api` 폴더도 새로 만든다)
```js
// 백엔드 주소. 나중에 환경에 따라 바꾸기 쉽도록 한 곳에 모아 둔다
const API_BASE = "http://localhost:8000";

export async function fetchProducts() {
  const response = await fetch(`${API_BASE}/api/v1/products`);

  if (!response.ok) {
    throw new Error(`서버 오류 (${response.status})`);
  }

  return response.json();
}
```

### 2-4. App에서 useEffect로 호출
`frontend/src/App.jsx` 전체를 다음으로 교체:
```jsx
import { useEffect, useState } from "react";
import "./App.css";
import ProductCard from "./components/ProductCard";
import { fetchProducts } from "./api/products";

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 화면이 처음 나타날 때 한 번만 실행된다 ([] 의 의미)
  useEffect(() => {
    fetchProducts()
      .then((data) => setProducts(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="message">불러오는 중...</p>;
  if (error) return <p className="message error">오류: {error}</p>;

  return (
    <div className="container">
      <h1 className="title">🥤 음료수 자판기</h1>

      {products.length === 0 ? (
        <p className="message">상품이 없습니다.</p>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
```

### 2-5. CORS 오류 체험 (의도된 실패)
백엔드(8000)와 프론트(5173)를 **각각 다른 터미널**에서 실행한다.
```powershell
# 터미널 1 (backend, 가상환경 활성화 상태)
uvicorn app.main:app --reload

# 터미널 2 (frontend)
npm run dev
```
- 브라우저 `http://localhost:5173` → "오류: Failed to fetch" 표시
- `F12` → Console 탭에서 다음 메시지를 확인한다.
  `blocked by CORS policy: No 'Access-Control-Allow-Origin' header ...`
- Network 탭에서 요청이 실제로는 서버에 도착했음을 확인한다. (브라우저가 응답을 막은 것)

### 2-6. CORS 해결
`backend/app/main.py` 전체를 다음으로 교체:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def root():
    return {"message": "서버가 실행 중입니다"}
```
- `--reload`가 켜져 있으면 저장 시 서버가 자동 재시작된다. 브라우저를 새로고침하면 카드가 표시된다. (아직 1단계처럼 이모지로 표시된다.)

### 2-7. 상품 이미지 연결 (서버의 products/images 폴더)
이모지 대신 **서버에 저장된 실제 이미지 파일**을 보여 준다. 이미지는 미리 준비되어 있다.

```
backend/products/images/
├─ cola.svg
├─ cider.svg
├─ orange.svg
├─ water.svg
├─ coffee.svg
└─ greentea.svg
```
- 이미지 파일 자체는 DB에 넣지 않고, DB에는 **이미지 경로(문자열)만** 저장한다. 파일은 서버 폴더에 둔다.
- 브라우저가 이 폴더의 파일을 받으려면 백엔드가 폴더를 웹 주소로 열어 줘야 한다. (FastAPI `StaticFiles`)
  - 폴더 `backend/products/images` → 주소 `http://localhost:8000/products/images/cola.svg`
- 준비된 이미지는 직접 그린 단순한 SVG 아이콘이다. 다른 이미지(jpg, png)로 바꾸고 싶으면 같은 폴더에 넣고 경로만 바꾸면 된다.

**(1) 백엔드: 이미지 폴더 공개** — `backend/app/main.py` 전체를 다음으로 교체:
```python
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
```
- 확인: 브라우저에서 `http://localhost:8000/products/images/cola.svg` 를 열면 콜라 그림이 보인다.

**(2) 백엔드: 하드코딩 JSON의 image_url을 이미지 경로로 교체** — `backend/app/routers/products.py`
```python
        {"id": 1, "name": "콜라", "price": 1500, "stock": 10, "image_url": "/products/images/cola.svg"},
        {"id": 2, "name": "사이다", "price": 1400, "stock": 8, "image_url": "/products/images/cider.svg"},
        {"id": 3, "name": "오렌지주스", "price": 2000, "stock": 0, "image_url": "/products/images/orange.svg"},
        {"id": 4, "name": "생수", "price": 1000, "stock": 25, "image_url": "/products/images/water.svg"},
        {"id": 5, "name": "커피", "price": 2500, "stock": 5, "image_url": "/products/images/coffee.svg"},
        {"id": 6, "name": "녹차", "price": 1800, "stock": 12, "image_url": "/products/images/greentea.svg"},
```

**(3) 프론트: 주소 상수 공유** — `frontend/src/api/products.js` 첫 줄의 `const` 를 `export const` 로 바꾼다:
```js
export const API_BASE = "http://localhost:8000";
```

**(4) 프론트: 카드에서 `<img>` 로 표시** — `frontend/src/components/ProductCard.jsx` 수정
```jsx
import "./ProductCard.css";
import { API_BASE } from "../api/products";

function ProductCard({ product }) {
  const soldOut = product.stock === 0;

  return (
    <div className={soldOut ? "card sold-out" : "card"}>
      {/* image_url 은 "/products/images/cola.svg" 같은 경로이므로 서버 주소를 앞에 붙인다 */}
      <img
        className="card-image"
        src={`${API_BASE}${product.image_url}`}
        alt={product.name}
      />
      <h3 className="card-name">{product.name}</h3>
      <p className="card-price">{product.price.toLocaleString()}원</p>
      <p className="card-stock">
        {soldOut ? "품절" : `재고 ${product.stock}개`}
      </p>
    </div>
  );
}

export default ProductCard;
```

`frontend/src/components/ProductCard.css` 의 `.card-image` 를 다음으로 교체:
```css
.card-image {
  width: 120px;
  height: 120px;
  object-fit: contain;
}
```
- 브라우저를 새로고침하면 이모지 대신 그림이 보인다.
- 이 변경 이후 1단계의 `fakeProducts`(이모지)는 `App`에서 더 쓰지 않는다.

```powershell
git add .
git commit -m "Level01 Step2: FastAPI 상품 API와 프론트 연동, CORS, 상품 이미지"
```

### ✅ 2단계 체크포인트
- [ ] Swagger에서 `GET /api/v1/products`가 6개 상품을 반환한다.
- [ ] CORS 오류를 직접 보고, 미들웨어 추가로 해결했다.
- [ ] 화면의 상품이 이제 **백엔드가 준 데이터**로 그려진다.
- [ ] `http://localhost:8000/products/images/cola.svg` 가 브라우저에서 열리고, 카드에 이미지가 표시된다.
- [ ] 백엔드를 끄고 새로고침하면 "오류: Failed to fetch"가 표시된다.

### 강의 포인트 / 자주 나는 오류
- **CORS란?** 브라우저의 보안 정책이다. "출처(주소+포트)가 다른 서버의 응답을 마음대로 읽지 못하게" 막는다. 서버가 "이 출처는 허용"이라고 알려 줘야 한다.
- `useEffect`의 `[]`를 빼면 어떻게 되는지(무한 호출 위험)는 설명만 하고 직접 실험은 권하지 않는다.
- `ModuleNotFoundError: No module named 'app'`: `backend` 폴더에서 실행했는지, 가상환경이 활성화되었는지 확인한다.
- `localhost`와 `127.0.0.1`은 브라우저가 다른 출처로 취급한다. `origins`에 쓴 주소와 접속 주소를 맞춘다.
- 프론트와 백엔드가 **서로 다른 프로세스**라는 점, 둘 다 켜 두어야 한다는 점을 반복해서 알려 준다.

---

## 3단계: DB 연결

### 학습 목표
- MariaDB에 전용 DB·계정·테이블을 만들고 샘플 데이터를 넣는다.
- 하드코딩 JSON을 `SELECT` 쿼리 결과로 교체한다. (ORM 없이 SQL 직접 사용)
- **router → service → repository** 계층을 나누고, 프론트를 수정하지 않아도 동작함을 확인한다.

### 3-1. DB와 전용 계정 만들기
`db/init.sql`
```sql
-- 학습용 DB 생성 (한글/이모지를 위해 utf8mb4 사용)
CREATE DATABASE IF NOT EXISTS vmShop
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

-- 프로젝트 전용 계정 (root를 직접 쓰지 않기 위함)
-- 비밀번호는 학습용 예시이므로 실제 서비스에서는 사용하지 않는다
CREATE USER IF NOT EXISTS 'vmshop_user'@'localhost' IDENTIFIED BY 'vmshop1234';
GRANT ALL PRIVILEGES ON vmShop.* TO 'vmshop_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3-2. 테이블과 샘플 데이터
실제 `db/schema.sql`에는 요구사항 정의서의 4개 테이블(`users`, `products`, `orders`, `order_items`)이 모두 들어 있다.
이번 레벨에서 쓰는 것은 **`products` 하나뿐**이므로, 수업에서는 아래 `products` 부분만 먼저 보여 주고 나머지는 "이후 레벨에서 사용할 테이블"이라고 안내한다.

`db/schema.sql` (products 부분 발췌)
```sql
USE vmShop;

-- 여러 번 실행해도 되도록 기존 테이블을 먼저 지운다
-- (전체 파일에서는 외래키 때문에 자식 테이블 order_items, orders 부터 지운다)
DROP TABLE IF EXISTS products;

CREATE TABLE products (
  id          INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50)  NOT NULL,
  price       INT          NOT NULL,
  stock       INT          NOT NULL DEFAULT 0,
  image_url   VARCHAR(255) NULL,
  description VARCHAR(255) NULL,
  is_active   TINYINT(1)   NOT NULL DEFAULT 1,
  created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_products_price CHECK (price >= 0),
  CONSTRAINT chk_products_stock CHECK (stock >= 0)
);
```

`db/seed.sql`
```sql
USE vmShop;

-- image_url 에는 2-7 에서 공개한 이미지 경로를 저장한다 (파일은 backend/products/images 에 있다)
INSERT INTO products (name, price, stock, image_url) VALUES
  ('콜라',       1500, 10, '/products/images/cola.svg'),
  ('사이다',     1400,  8, '/products/images/cider.svg'),
  ('오렌지주스', 2000,  0, '/products/images/orange.svg'),
  ('생수',       1000, 25, '/products/images/water.svg'),
  ('커피',       2500,  5, '/products/images/coffee.svg'),
  ('녹차',       1800, 12, '/products/images/greentea.svg');
```

실행 (프로젝트 루트에서, root 비밀번호 입력 필요):
```powershell
cd D:\AX_WORK\VMFullStack
mariadb -u root -p --default-character-set=utf8mb4 < db\init.sql
mariadb -u vmshop_user -p --default-character-set=utf8mb4 < db\schema.sql
mariadb -u vmshop_user -p --default-character-set=utf8mb4 < db\seed.sql
```
- 클라이언트 명령이 `mariadb`가 아니라 `mysql`인 설치본도 있다. 안 되면 `mysql`로 바꿔 입력한다.
- PowerShell에서 `<` 리다이렉션이 막히면 `cmd /c "mariadb -u root -p < db\init.sql"` 형태로 실행하거나, HeidiSQL/DBeaver에서 파일을 열어 실행해도 된다.
- 한글·이모지가 `?`로 깨져 보이면 콘솔 출력 문제일 수 있다. HeidiSQL 등에서 확인한다.

확인:
```sql
USE vmShop;
SELECT * FROM products;
```

### 3-3. 접속 설정(.env)
`backend/.env.example` (커밋용 견본)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=vmshop_user
DB_PASSWORD=여기에_비밀번호
DB_NAME=vmShop
```

`backend/.env` (실제 사용, Git에 올리지 않음)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=vmshop_user
DB_PASSWORD=vmshop1234
DB_NAME=vmShop
```

### 3-4. DB 연결 모듈
`backend/app/database.py`
```python
import os

import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

# .env 파일의 값을 환경변수로 읽어 온다
load_dotenv()


def get_connection():
    """요청마다 새 DB 연결을 만든다. 사용 후에는 반드시 close() 해야 한다."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=DictCursor,  # 결과를 {"컬럼명": 값} 딕셔너리로 받는다
    )
```
> 연결을 매번 새로 만드는 방식은 단순하지만 비효율적이다. 커넥션 풀은 이후 레벨에서 개선 과제로 다룬다.

### 3-5. Repository 계층 (SQL을 실행하는 곳)
`backend/app/repositories/product_repository.py` (새 파일, `repositories` 폴더도 새로 만든다)
```python
from app.database import get_connection


def find_all():
    """판매 중인 상품 전체를 조회한다."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # ORM 없이 SQL을 직접 작성한다
            sql = """
                SELECT id, name, price, stock, image_url
                FROM products
                WHERE is_active = 1
                ORDER BY id
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()  # 오류가 나도 연결은 반드시 닫는다
```

### 3-6. Service 계층 (업무 규칙이 들어갈 자리)
`backend/app/services/product_service.py` (새 파일, `services` 폴더도 새로 만든다)
```python
from app.repositories import product_repository


def get_products():
    # 지금은 단순 전달이지만, 나중에 업무 규칙(할인, 필터 등)이 이곳에 들어간다
    return product_repository.find_all()
```

### 3-7. Router를 service 호출로 교체
`backend/app/routers/products.py` 전체를 다음으로 교체:
```python
from fastapi import APIRouter, HTTPException

from app.services import product_service

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("")
def get_products():
    try:
        return product_service.get_products()
    except Exception as e:
        # 내부 오류 상세는 서버 터미널에만 남기고, 사용자에게는 일반 메시지만 준다
        print(f"[ERROR] 상품 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="상품 목록을 불러오지 못했습니다.")
```

### 3-8. 동작 확인
```powershell
cd D:\AX_WORK\VMFullStack\backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
1. Swagger(`/docs`)에서 `GET /api/v1/products` 실행 → DB의 6개 상품이 반환된다.
2. 프론트(`npm run dev`) 새로고침 → **프론트 코드를 한 줄도 바꾸지 않았는데** DB 데이터가 표시된다.
3. DB에서 데이터를 바꾼 뒤 새로고침하면 화면이 따라 바뀐다.
   ```sql
   USE vmShop;
   UPDATE products SET stock = 0 WHERE name = '콜라';
   ```
   → 콜라 카드가 "품절"로 바뀐다.
4. (실험) `.env`의 비밀번호를 일부러 틀리게 바꾸면 화면에 오류 메시지가 표시된다. 확인 후 원복한다.

```powershell
cd D:\AX_WORK\VMFullStack
git add .
git commit -m "Level01 Step3: MariaDB 연결, repository/service 계층"
```

### ✅ 3단계 체크포인트
- [ ] `SELECT * FROM products;`에 6행이 있다.
- [ ] API 응답이 DB 데이터와 일치한다.
- [ ] DB 값을 수정하면 화면이 따라 바뀐다.
- [ ] 프론트 코드는 2단계와 동일하다.
- [ ] `.env`가 Git에 포함되지 않았다. (`git status`로 확인)

### 강의 포인트
- **계층의 역할**: router는 요청/응답, service는 업무 규칙, repository는 SQL. 각자 한 가지만 한다.
- **계층 분리의 효과**: 2단계에서 3단계로 넘어올 때 바뀐 것은 백엔드 내부뿐이고 프론트는 그대로다. "API 응답의 모양이 약속(계약)이다"라는 점을 강조한다.
- **SQL 직접 사용**: 쿼리 결과가 어떻게 JSON이 되는지(DictCursor → dict → JSON) 흐름을 짚는다.
- **보안 한 마디**: 비밀번호를 코드에 쓰지 않고 `.env`로 분리하는 이유, `.env`를 커밋하지 않는 이유를 설명한다.
- 자주 나는 오류
  - `Access denied for user`: `.env`의 계정/비밀번호가 `init.sql`과 같은지 확인한다.
  - `Can't connect to MySQL server`: MariaDB 서비스가 꺼져 있거나 포트(3306)가 다르다.
  - `Unknown database 'vmShop'`: `init.sql`을 먼저 실행했는지 확인한다.

---

## Level 01 최종 점검

**전체 요청 흐름**
```
브라우저(React)
  └─ fetch GET /api/v1/products
       └─ router (products.py)          요청 받기 / 오류 응답
            └─ service                  업무 규칙
                 └─ repository          SELECT 쿼리 실행
                      └─ MariaDB        products 테이블
```

**수강생 확인 질문**
1. 상품 데이터가 화면에 나타나기까지 거치는 단계를 순서대로 말해 보세요.
2. `useState`와 `useEffect`는 각각 무엇을 위해 쓰였나요?
3. CORS 오류는 왜 생기고, 어디(프론트/백엔드)를 고쳐서 해결했나요?
4. 가짜 데이터에서 DB로 바꿀 때 프론트를 고치지 않아도 된 이유는 무엇인가요?
5. repository, service, router는 각각 어떤 일을 하나요?

**도전 과제 (시간 여유 시)**
- 상품을 이름으로 검색하는 입력창 만들기 (프론트 `useState` 필터링)
- 재고가 5개 이하인 상품에 "품절 임박" 표시하기
- `GET /api/v1/products/{id}` 상세 API 추가하기

**다음 레벨 예고**: Level 02 - 회원가입 (폼 입력, POST, INSERT, 비밀번호 해시)
