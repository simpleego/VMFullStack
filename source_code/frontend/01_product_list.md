# 1단계 — 사이트 방문 → 상품 목록

> **User Story** : 방문자는 사이트에 들어오면 상품 목록을 볼 수 있다.

---

## 1. 요청 / 응답

| 구분 | 내용 |
|------|------|
| 사용자 행동 | 브라우저에서 `http://localhost:5173` 접속 |
| 프론트 처리 | `ProductList` 화면이 처음 나타날 때 `useEffect` 에서 API 호출 |
| API 요청 | `GET /products` (Vite 프록시 → `http://localhost:8000/products`) |
| 백엔드 처리 | `SELECT id, name, price, stock, image_url FROM products WHERE is_active = 1 ORDER BY price` |
| API 응답 (성공) | `200` + 상품 배열 |
| API 응답 (실패) | `500` + `{"detail": "상품 목록 조회 에러"}` |
| 화면 결과 | 로딩 중 → 상품 카드 목록 (실패하면 에러 메시지) |

### 요청

```http
GET /products HTTP/1.1
Host: localhost:5173
```

### 응답 예시 (200 OK)

```json
[
  { "id": 12, "name": "생수 500ml", "price": 1000, "stock": 100, "image_url": "/products/images/water.svg" },
  { "id": 4,  "name": "사이다",     "price": 1400, "stock": 30,  "image_url": "/products/images/cider.svg" },
  { "id": 1,  "name": "콜라",       "price": 1500, "stock": 50,  "image_url": "/products/images/cola.svg" },
  { "id": 6,  "name": "오렌지주스", "price": 2000, "stock": 0,   "image_url": "/products/images/orange.svg" }
]
```

### 응답 예시 (500 에러)

```json
{ "detail": "상품 목록 조회 에러" }
```

---

## 2. 이번 단계에서 만드는 파일

| 파일 | 작업 |
|------|------|
| `vite.config.js` | 수정 — `/products` 프록시 추가 |
| `src/api/products.js` | **새로 만듦** — API 호출 함수 |
| `src/utils/image.js` | **새로 만듦** — 이미지 경로 변환 |
| `src/pages/ProductList.jsx` | **새로 만듦** — 상품 목록 화면 |
| `src/App.jsx` | 수정 — 하드코딩 배열 삭제, 헤더 + ProductList |
| `src/App.css` | 수정 — 스타일 추가 |

---

## 3. 코드

### 3-1. `vite.config.js` (server 부분)

```js
  server: {
    proxy: {
      // 상품 검색 테스트 화면(test.html)용
      '/search': process.env.API_TARGET || 'http://localhost:8001',

      // ✅ 추가 : 자판기 화면용 상품 API (목록, 상세)
      '/products': 'http://localhost:8000',
    },
  },
```

> 프록시를 바꾼 뒤에는 `npm run dev` 를 **다시 실행**해야 한다.

### 3-2. `src/api/products.js` (새 파일)

```js
// 백엔드 상품 API 기본 주소
//   Vite 프록시가 '/products' 로 시작하는 요청을 http://localhost:8000 으로 전달한다.
const API_BASE = '/products'

// 공통 요청 함수
//   fetch 는 404, 500 이어도 예외를 던지지 않는다 → res.ok 를 직접 확인한다.
//   백엔드 HTTPException 의 detail 메시지를 에러 메시지로 사용한다.
async function request(url, signal) {
  const res = await fetch(url, { signal })

  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `서버 오류 (${res.status})`)
  }

  return res.json()
}

// [1단계] 상품 목록 : GET /products
export function fetchProducts(signal) {
  return request(API_BASE, signal)
}
```

### 3-3. `src/utils/image.js` (새 파일)

```js
// DB 의 image_url("/products/images/cola.svg") 을
// 프론트 public 폴더 경로("/images/cola.svg") 로 바꾼다.
//   백엔드가 아직 이미지 파일을 내려주지 않기 때문에 public/images 의 같은 파일을 쓴다.
//   image_url 이 NULL 이면 기본 이미지를 보여준다.
export function toImagePath(imageUrl) {
  if (!imageUrl) return '/favicon.svg'
  const fileName = imageUrl.split('/').pop()   // "cola.svg"
  return `/images/${fileName}`
}
```

### 3-4. `src/pages/ProductList.jsx` (새 파일)

```jsx
import { useEffect, useState } from 'react'
import ProductCard from '../components/ProductCard'
import { fetchProducts } from '../api/products'
import { toImagePath } from '../utils/image'

// 상품 목록 화면
function ProductList() {
  // 화면 상태 3가지 : 데이터, 로딩 중인지, 에러 메시지
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // 화면이 처음 나타날 때 한 번만 상품 목록을 불러온다. (의존성 배열 [])
  useEffect(() => {
    // 화면이 사라지면 진행 중인 요청을 취소하기 위한 컨트롤러
    const controller = new AbortController()

    fetchProducts(controller.signal)
      .then((data) => {
        // 이미지 경로만 프론트용으로 바꿔서 저장 (나머지 필드는 그대로)
        setProducts(data.map((p) => ({ ...p, image_url: toImagePath(p.image_url) })))
      })
      .catch((err) => {
        if (err.name === 'AbortError') return   // 취소된 요청은 에러가 아니다
        setError(err.message)
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })

    // 정리(cleanup) 함수 : 화면이 사라질 때 요청 취소
    return () => controller.abort()
  }, [])

  if (loading) return <p className="message">상품을 불러오는 중...</p>
  if (error) return <p className="message error">⚠️ {error}</p>
  if (products.length === 0) return <p className="message">판매 중인 상품이 없습니다.</p>

  return (
    <div className="product-grid">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

export default ProductList
```

### 3-5. `src/App.jsx`

```jsx
import './App.css'
import ProductList from './pages/ProductList'

function App() {
  return (
    <div className="container">
      <header className="header">
        <h1 className="title">🥤 음료수 자판기</h1>
      </header>

      <ProductList />
    </div>
  )
}

export default App
```

> 기존 `App.jsx` 의 `products` 하드코딩 배열과 사용하지 않는 import(heroImg, reactLogo, viteLogo)는 삭제한다.

### 3-6. `src/App.css` 에 추가

```css
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.message {
  text-align: center;
  color: #666;
  margin: 40px 0;
}

.message.error {
  color: #d32f2f;
}
```

> `ProductCard.jsx` 는 이번 단계에서 **수정하지 않는다.** 응답 필드 이름이 기존 배열과 같기 때문이다.

---

## 4. 설명

### 왜 `api/products.js` 로 분리하나?
2단계에서 상세 API(`GET /products/{id}`)도 호출한다. 에러 처리(`res.ok` 확인, `detail` 꺼내기)를
한 곳에 모아 두면 화면 컴포넌트는 "데이터를 받아서 그리기"에만 집중할 수 있다.

### 왜 `useEffect(..., [])` 인가?
컴포넌트 본문에서 바로 fetch 하면 렌더링 → fetch → setState → 다시 렌더링 → 또 fetch ... **무한 반복**이 된다.
의존성 배열을 `[]` 로 주면 **화면이 처음 나타날 때 한 번만** 실행된다.

### 왜 `ProductList` 가 데이터를 직접 가지나?
상품 목록 데이터는 목록 화면에서만 쓴다. 다른 화면과 공유할 필요가 없으므로 App 이 아니라 `ProductList` 안에 둔다.
(반대로 4단계의 장바구니는 여러 화면이 같이 쓰므로 App 에 둔다.)

### 4가지 화면 상태

| 상황 | 화면 |
|------|------|
| 응답 기다리는 중 | "상품을 불러오는 중..." |
| 에러 (백엔드 꺼짐, DB 오류) | "⚠️ 상품 목록 조회 에러" |
| 성공 + 0개 | "판매 중인 상품이 없습니다." |
| 성공 + 1개 이상 | 상품 카드 목록 (가격 낮은 순 — SQL `ORDER BY price`) |

---

## 5. 확인

- [ ] `http://localhost:8000/products` 에서 JSON 이 보인다
- [ ] `http://localhost:5173` 에서 DB 상품이 카드로 보인다
- [ ] 품절 상품(stock 0)은 흐리게 "품절" 로 보인다
- [ ] 백엔드를 끄고 새로고침하면 에러 메시지가 보인다

---

## 6. 참고 — `AbortController` 자세히 보기

`ProductList`(1단계)와 `ProductDetail`(2단계)의 `useEffect` 에서 사용하는
`const controller = new AbortController()` 에 대한 Q&A 정리.

### 6-1. AbortController 란?

> **진행 중인 `fetch` 요청을 중간에 취소할 수 있게 해 주는 브라우저 내장 객체**다.

```js
const controller = new AbortController()   // 리모컨 만들기
controller.signal                          // 수신기 (fetch 에 달아 줌)
controller.abort()                         // 취소 버튼 누르기
```

| 구성 | 역할 |
|------|------|
| `controller` | 취소 버튼을 가진 **리모컨** |
| `controller.signal` | 요청에 붙이는 **수신기**. fetch 는 이걸 보고 취소 신호가 오는지 지켜본다 |
| `controller.abort()` | **취소 신호 보내기**. 수신기를 단 fetch 가 즉시 중단된다 |

```js
const controller = new AbortController()

fetch('/products', { signal: controller.signal })   // ① 수신기를 달아서 요청
  .then(res => res.json())
  .catch(err => console.log(err.name))              // ③ 'AbortError' 출력

controller.abort()                                  // ② 응답이 오기 전에 취소
```

취소되면 fetch 는 **`AbortError` 라는 이름의 에러**를 던진다.

### 6-2. useEffect 에서 쓰는 패턴

```jsx
useEffect(() => {
  const controller = new AbortController()          // ① 요청마다 리모컨 준비

  fetchProducts(controller.signal)                  // ② 수신기 달아서 요청
    .then((data) => setProducts(...))
    .catch((err) => {
      if (err.name === 'AbortError') return         // ④ 취소는 에러가 아님 → 무시
      setError(err.message)
    })
    .finally(() => {
      if (!controller.signal.aborted) setLoading(false)  // ⑤ 취소됐으면 상태 안 바꿈
    })

  return () => controller.abort()                   // ③ 화면이 사라지면 취소
}, [])
```

`return () => ...` 는 **정리(cleanup) 함수**다. React 는 컴포넌트가 화면에서 사라질 때,
또는 effect 가 다시 실행되기 직전에 이 함수를 호출한다.

| 코드 | 이유 |
|------|------|
| `if (err.name === 'AbortError') return` | 취소는 **일부러 한 것**이므로 화면에 "⚠️ 에러" 를 띄우면 안 된다 |
| `if (!controller.signal.aborted) setLoading(false)` | `signal.aborted` 는 취소됐으면 `true`. 이미 사라진 화면의 상태는 바꾸지 않는다 |

#### 필요한 상황 3가지

**상황 1 : 응답이 오기 전에 화면을 떠날 때**

```
상품 목록 화면 열림 → fetch 시작 ... (백엔드 응답 느림)
사용자가 바로 상품 클릭 → 목록 화면 사라짐
                     ... 응답 도착 → setProducts() ← 이미 없는 화면의 상태를 바꾸려 함
```

정리 함수에서 `abort()` 하면 필요 없어진 요청이 바로 중단된다.

**상황 2 : 응답 순서가 뒤바뀔 때**

```
콜라 상세 요청 ──────────────────────(느림)──────────▶ 콜라 응답 도착
      사이다 상세 요청 ──(빠름)──▶ 사이다 응답 도착
```

사이다를 보고 있는데 늦게 도착한 콜라 데이터가 화면을 덮어쓸 수 있다.
새 요청 전에 이전 요청을 `abort()` 하면 마지막으로 요청한 상품만 남는다.

**상황 3 : 개발 모드의 StrictMode**

개발 모드에서 React 는 버그를 찾으려고 **effect 를 일부러 두 번 실행**한다 (실행 → 정리 → 다시 실행).
첫 번째 요청은 정리 함수에서 취소되므로 Network 탭에 요청 하나가 `(canceled)` 로 보이는 것은 정상이다.

### 6-3. 브라우저가 제공하는 객체인가?

**그렇다. 브라우저가 제공하는 Web API** 다. JavaScript 언어 자체나 React 가 제공하는 것이 아니다.

| 구분 | 예시 | 정해진 곳 |
|------|------|-----------|
| **JavaScript 언어 자체** (ECMAScript) | `Array`, `Promise`, `JSON`, `Map` | ECMAScript 표준 |
| **브라우저 Web API** | `fetch`, `AbortController`, `localStorage`, `window.confirm`, `document` | WHATWG/W3C 웹 표준 |
| **React** | `useState`, `useEffect` | React 라이브러리 (import 필요) |

- 이번 자판기 코드의 `fetch`, `AbortController`, `localStorage`, `window.confirm`, `alert` 는 모두 Web API 라서 **import 없이** 쓴다.
- **Node.js 에도 있다.** v15 부터 브라우저와 같은 이름의 전역 객체로 들어갔다.
- 2019년쯤부터 모든 최신 브라우저가 지원한다. (Internet Explorer 는 미지원)
- fetch 외에도 쓸 수 있다.

```js
// 이벤트 리스너를 한 번에 해제
const controller = new AbortController()
window.addEventListener('resize', onResize, { signal: controller.signal })
controller.abort()   // 리스너 제거

// 시간 제한 (5초 안에 응답이 없으면 자동 취소)
fetch('/products', { signal: AbortSignal.timeout(5000) })
```

개발자도구 **Console** 에서 직접 확인할 수 있다.

```js
typeof AbortController      // 'function' → 브라우저에 내장되어 있음
new AbortController()       // AbortController { signal: AbortSignal }
```

### 6-4. 이 코드를 넣지 않으면 어떤 일이 생기나?

> **지금 문서의 코드 구조에서는 빼도 눈에 보이는 버그는 거의 없다.**
> 대신 낭비가 생기고, 구조가 조금만 바뀌면 실제 버그가 된다.

#### 지금 구조에서 빼면

| 상황 | AbortController 없을 때 | 눈에 보이는 문제 |
|------|------------------------|-----------------|
| 응답 오기 전에 화면을 떠남 | 요청은 끝까지 진행되고, 응답이 오면 사라진 화면에 `setState` 호출 | **없음.** React 18 부터는 사라진 컴포넌트의 setState 를 조용히 무시한다 (경고도 없음) |
| 개발 모드 StrictMode | effect 두 번 실행 → **요청 2번 모두 끝까지 처리** | 백엔드 터미널에 `상품 목록 조회` 로그가 **2번**, DB 조회도 2번 |
| 상세 화면에서 상품이 바뀜 | 이전 요청이 계속 진행 | **없음.** `key={selectedId}` 로 상세 화면을 새로 만들기 때문에 이전 화면의 응답은 무시된다 |

→ **불필요한 요청이 끝까지 처리되는 낭비**(네트워크, 백엔드, DB) 정도다.

> React 17 이전에는 사라진 화면에 setState 를 하면 *"Can't perform a React state update on an unmounted component"* 경고가 떴다.
> 오래된 자료에서 "이 경고를 막으려고 AbortController 를 쓴다" 고 설명하는 경우가 많은데, React 18 부터는 이 경고가 없어졌다.

#### 실제 버그가 되는 경우 — 응답 순서 뒤바뀜 (Race Condition)

**같은 화면이 유지된 채로 요청 조건만 바뀔 때** 문제가 된다. 대표적인 예가 검색(`/search` API)이다.

```
사용자 입력:  "콜"  →  "콜라"

"콜"   요청 ─────────────────(느림)──────────────▶ 응답: 콜라, 콜라제로, 콜드브루 ...
   "콜라" 요청 ──(빠름)──▶ 응답: 콜라, 콜라제로
                              ↑ 화면 표시
                                                  ↑ 늦게 온 "콜" 결과가 덮어씀 ❌
```

검색창에는 **"콜라"** 인데 화면에는 **"콜" 검색 결과**가 남는다. 에러도 나지 않아서 찾기 어렵다.
2단계 상세 화면에서 `key={selectedId}` 를 빼도 같은 문제가 생길 수 있다.

AbortController 를 넣으면 "콜라" 요청 전에 정리 함수가 "콜" 요청을 취소하므로 **항상 마지막 요청의 결과만** 남는다.

#### 수업에서 직접 보여주는 방법

1. **StrictMode 중복 요청**
   - AbortController 를 빼고 새로고침 → 백엔드 로그 2번, Network 탭에 `/products` 2개 모두 `200`
   - 다시 넣으면 첫 번째 요청이 `(canceled)` 로 바뀐다
2. **느린 네트워크에서 화면 떠나기**
   - 개발자도구 → Network → Throttling 을 **Slow 4G** 또는 **3G** 로 변경
   - 목록이 뜨기 전에 다른 화면으로 이동 → 넣었을 때만 요청이 `(canceled)` 로 끊긴다

### 6-5. 정리

- `new AbortController()` 로 리모컨을 만들고, `signal` 을 fetch 에 달고, `abort()` 로 취소한다.
- useEffect 의 **정리 함수에서 `abort()`** 하는 것이 기본 패턴이다.
- 취소되면 `AbortError` 가 발생하므로 **에러 처리에서 제외**한다.
- 지금 구조에서는 빼도 화면은 정상이지만, 검색·필터처럼 **화면은 그대로이고 조건만 바뀌는 구조**에서는 버그가 된다.
  → "useEffect 에서 fetch 하면 정리 함수에서 취소한다" 를 습관으로 둔다.
