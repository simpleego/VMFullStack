# LectureNote_Step01 - 강의 진행안 (Level 01: 상품 목록 조회)

대상: 웹 개발 입문자 / 강사: 코드 설명은 강사가 직접 진행하고, 이 문서는 **시간 배분과 진행 순서, HTTP 실습 자료**를 제공한다.
범위: Level 01 (0~3단계) + HTTP 요청/응답 헤더 실습 (개발자 도구, 터미널)
총 시간: **6시간 = 2시간 × 3회차** (코드 4시간 + HTTP 실습 약 1시간 + 복습·정리 1시간)

---

## 0. 한눈에 보기

| 회차 | 주제 | 코드 단계 | HTTP 실습 | 끝났을 때 상태 (Git 태그) |
|:--:|------|-----------|-----------|--------------------------|
| 1회차 | 환경 설정과 화면 | 0단계, 1단계 | - | `v0.1-step1` |
| 2회차 | 백엔드 연결과 CORS | 2단계 (2-1 ~ 2-7) | **개발자 도구 Network 탭** | `v0.1-step2` |
| 3회차 | DB 연결과 계층 분리 | 3단계 (3-1 ~ 3-8) | **터미널 도구 (curl, PowerShell, Python)** | `v0.1-step3` |

**수업 전체의 한 줄 목표**
> 화면(React)의 요청이 서버(FastAPI)를 거쳐 DB(MariaDB)까지 갔다 돌아오는 길을, 코드로도 만들고 HTTP 메시지로도 눈으로 확인한다.

### 학습 목표
1. React, FastAPI, MariaDB 세 가지가 각각 무엇을 맡는지 설명할 수 있다.
2. `useState`, `useEffect` + `fetch`로 서버 데이터를 화면에 그릴 수 있다.
3. CORS 오류가 왜 생기는지 알고 해결할 수 있다.
4. router / service / repository 계층이 하는 일을 구분할 수 있다.
5. **HTTP 요청과 응답의 구조(상태줄, 헤더, 본문)를 읽을 수 있고, 개발자 도구와 터미널로 직접 확인할 수 있다.**

### 준비물과 사전 점검 (강사)
| 항목 | 확인 |
|------|------|
| 완성본 실행: 백엔드 `:8000`, 프론트 `:5173`, MariaDB 서비스 | [ ] |
| 수강생 PC: Python 3.11+, Node LTS, Git, VS Code, Chrome 또는 Edge, MariaDB 설치 | [ ] |
| MariaDB `bin` 폴더 PATH 등록 (`C:\Program Files\MariaDB 11.8\bin`) 또는 전체 경로 사용 안내 | [ ] |
| 수강생 PC의 MariaDB root 비밀번호 (수업 3회차에 필요) | [ ] |
| 시연용 Git 태그 확인: `git tag` 에 `v0.1-step1`, `v0.1-step2`, `v0.1-step3` | [ ] |
| 참고 자료: `docs/level01.md`(단계별 코드), `docs/dbSQL.md`(DB 정리), 유스케이스 보드(시각화 페이지) | [ ] |

> 수업 전에 강사 PC에서 0단계부터 끝까지 한 번 리허설하길 권한다. 특히 3회차 Python `requests` 예제는 모듈 설치가 필요하다. (부록 C 참고)

---

## 1회차 (120분): 환경 설정과 화면 만들기

**목표**: 개발환경을 갖추고, 가짜 데이터로 상품 목록 화면을 만든다. (`v0.1-step1`)

| 시간 | 분 | 내용 | 진행 방식 |
|------|:--:|------|-----------|
| 0:00 ~ 0:10 | 10 | **오프닝** 프로젝트 소개, 완성본 시연(상품 카드 화면), 3회차 로드맵 | 강사 시연 |
| 0:10 ~ 0:25 | 15 | **전체 구조** 프론트 / 백엔드 / DB 역할, 요청이 흐르는 길(유스케이스 보드 활용) | 강의 + 그림 |
| 0:25 ~ 0:55 | 30 | **0단계 개발환경** 설치 확인, 폴더 구조, `.gitignore`, Python 가상환경, `pip install`, Vite 프로젝트 생성, 첫 커밋 | 강사 시연 + 따라하기 |
| 0:55 ~ 1:00 | 5 | 휴식 | |
| 1:00 ~ 1:40 | 40 | **1단계 가짜 데이터 화면** `ProductCard` 컴포넌트, props, `App`의 `useState`, `map`과 `key`, "목록 비우기/채우기" 버튼 | 강사가 코드 설명하며 함께 작성 |
| 1:40 ~ 1:55 | 15 | **실습** 가짜 데이터에 상품 추가, 가격 변경, 재고 0 만들어 "품절" 확인 | 개인 실습, 순회 지도 |
| 1:55 ~ 2:00 | 5 | **정리** 체크포인트 확인, 커밋, 다음 회차 예고 | |

**강의 포인트**
- 세 개의 실행 환경이 왜 필요한지 먼저 말로 설명하고 시작한다. (화면 / 서버 / 데이터 저장)
- `let` 변수를 바꿔도 화면이 안 바뀌지만 `useState`를 바꾸면 바뀌는 것을 실험으로 보여 준다.
- 가짜 데이터의 모양(`id, name, price, stock, image_url`)이 **나중에 API 응답과 같은 모양**임을 강조한다. 이것이 3단계에서 프론트를 안 고쳐도 되는 이유다.

**자주 막히는 곳**
| 증상 | 대응 |
|------|------|
| `python` 명령을 찾을 수 없음 | 설치 때 "Add to PATH" 누락. 재설치 또는 PATH 추가 |
| `.venv\Scripts\Activate.ps1` 실행 정책 오류 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `npm create vite` 질문이 다름 | React + JavaScript 선택 |
| 화면이 빈 하얀 화면 | 브라우저 F12 Console 오류 확인 (컴포넌트 import 경로, 파일 확장자 `.jsx`) |

**체크포인트**
- [ ] `http://localhost:5173`에 상품 카드가 보인다
- [ ] 재고 0 상품이 "품절"로 흐리게 표시된다
- [ ] 버튼으로 목록이 사라졌다 나타난다
- [ ] `git log`에 커밋이 있다

---

## 2회차 (120분): 백엔드 연결, CORS, 개발자 도구로 HTTP 보기

**목표**: FastAPI API를 만들어 React와 연결하고, 요청과 응답을 개발자 도구로 직접 관찰한다. (`v0.1-step2`)

| 시간 | 분 | 내용 | 진행 방식 |
|------|:--:|------|-----------|
| 0:00 ~ 0:10 | 10 | **복습** 지난 시간 퀴즈 (props? useState? 가짜 데이터 모양이 중요한 이유?) | 질문 |
| 0:10 ~ 0:30 | 20 | **2-1, 2-2 FastAPI** 서버 실행, `/docs`(Swagger), 라우터와 하드코딩 JSON, `GET /api/v1/products` | 강사 코드 설명 |
| 0:30 ~ 0:50 | 20 | **2-3, 2-4 프론트 연동** `fetchProducts`, `useEffect` + `fetch`, 로딩/오류 상태 | 강사 코드 설명 |
| 0:50 ~ 0:55 | 5 | 여유 시간 (밀린 수강생 따라잡기) | |
| 0:55 ~ 1:00 | 5 | 휴식 | |
| 1:00 ~ 1:20 | 20 | **2-5, 2-6 CORS** 일부러 오류 보기, 원인 설명, 미들웨어로 해결 | 체험 후 설명 |
| 1:20 ~ 1:35 | 15 | **2-7 이미지 연결** `StaticFiles`, 이미지 경로와 `<img>` | 강사 코드 설명 |
| 1:35 ~ 1:55 | 20 | **HTTP 실습 ①: 개발자 도구 Network 탭** (부록 B) | 함께 따라하기 |
| 1:55 ~ 2:00 | 5 | **정리** 체크포인트, 커밋, 다음 회차 예고 | |

**강의 포인트**
- 서버를 켠 채로 `http://localhost:8000/api/v1/products`를 **브라우저 주소창에 직접** 입력해 JSON이 보이는 것을 먼저 보여 준다. "주소창 입력 = GET 요청"을 몸으로 이해시킨다.
- CORS는 **서버가 막는 것이 아니라 브라우저가 응답을 못 읽게 막는 것**이다. 오류 상태에서도 Network 탭에는 요청이 도착한 기록이 남는다.
- 개발자 도구 실습은 CORS 해결 **직후**에 한다. 막 겪은 문제를 헤더로 설명할 수 있다. (`access-control-allow-origin`)

**수업용 Git 태그** (CORS를 처음부터 재현하고 싶을 때)
| 태그 | 상태 |
|------|------|
| `v0.1-step2-1` | API + fetch 연동, CORS 미적용 (오류 상태) |
| `v0.1-step2-2` | CORS 해결 |
| `v0.1-step2` | 서버 이미지 연결 (2단계 완료) |

**자주 막히는 곳**
| 증상 | 대응 |
|------|------|
| `ModuleNotFoundError: No module named 'app'` | `backend` 폴더에서 실행했는지, 가상환경 활성화 여부 |
| CORS 해결했는데 계속 오류 | 서버 재시작 확인 (`--reload`가 멈추는 경우가 있음), `localhost`와 `127.0.0.1` 혼용 여부 |
| 이미지가 안 보임 | 이미지 URL을 주소창에 직접 열어 보기 (`/products/images/cola.svg`), 404면 폴더 경로 확인 |
| 두 서버 중 하나만 켬 | 프론트와 백엔드는 **별도 프로세스**, 터미널 두 개 필요 |

**체크포인트**
- [ ] `/docs`에서 `GET /api/v1/products`가 6개 상품 반환
- [ ] CORS 오류를 직접 보고 해결했다
- [ ] 카드에 서버 이미지가 표시된다
- [ ] Network 탭에서 요청의 상태코드와 응답 헤더를 찾을 수 있다

---

## 3회차 (120분): DB 연결, 계층 분리, 터미널로 HTTP 호출하기

**목표**: 하드코딩 데이터를 DB 조회로 교체하고, 터미널 도구로 API를 직접 호출해 본다. (`v0.1-step3`)

| 시간 | 분 | 내용 | 진행 방식 |
|------|:--:|------|-----------|
| 0:00 ~ 0:10 | 10 | **복습** Network 탭으로 지난 요청 다시 확인 (상태코드, `content-type`, CORS 헤더) | 질문 + 시연 |
| 0:10 ~ 0:40 | 30 | **3-1, 3-2 DB 준비** DB/테이블 개념, `init.sql` → `schema.sql` → `seed.sql` 실행, `SELECT * FROM products` 직접 확인 | 강사 시연 + 따라하기 |
| 0:40 ~ 1:05 | 25 | **3-3 ~ 3-7 코드** `.env`, `database.py`, repository(SQL), service, router 교체 | 강사 코드 설명 |
| 1:05 ~ 1:10 | 5 | 휴식 | |
| 1:10 ~ 1:25 | 15 | **3-8 동작 확인** DB 값 변경 후 새로고침, 프론트 무수정 확인, 태그 비교 | 체험 |
| 1:25 ~ 1:50 | 25 | **HTTP 실습 ②: 터미널 도구** curl, PowerShell, Python (부록 C) | 함께 따라하기 |
| 1:50 ~ 2:00 | 10 | **마무리** 전체 흐름 정리, 확인 질문, 과제, Level 02 예고 | |

**강의 포인트**
- 3-8의 핵심 장면: `UPDATE products SET stock = 0 WHERE name = '콜라';` 실행 후 **새로고침만 했는데** 화면이 바뀐다. 프론트 코드는 한 줄도 안 바뀌었다는 점을 짚는다.
- 계층 비유: router = 주문 창구, service = 주방장, repository = 창고 담당. SQL은 repository에만 있다.
- 보안 한 마디: 비밀번호를 `.env`로 분리하는 이유, `.env`를 Git에 올리지 않는 이유, 오류 상세를 사용자에게 숨기는 이유.

**자주 막히는 곳**
| 증상 | 대응 |
|------|------|
| `mariadb` 명령을 찾을 수 없음 | PATH 추가 또는 전체 경로 (`& "C:\Program Files\MariaDB 11.8\bin\mariadb.exe" ...`), HeidiSQL/DBeaver도 가능 |
| `Access denied for user` | `.env`와 `init.sql`의 계정, 비밀번호 일치 확인 |
| `Unknown database 'vmShop'` | `init.sql`을 먼저 실행했는지 |
| `Can't connect to MySQL server` | MariaDB 서비스 실행 여부, 포트 3306 |
| 상품이 12개로 중복 | `seed.sql`을 반복 실행함. `schema.sql` → `seed.sql` 순서로 초기화 |

**체크포인트**
- [ ] `SELECT * FROM products;`에 6행이 있다
- [ ] API 응답이 DB 데이터와 일치한다
- [ ] DB 값을 바꾸면 화면이 따라 바뀐다
- [ ] 프론트 코드는 2단계와 동일하다
- [ ] curl 또는 Python으로 API 응답의 상태코드와 헤더를 직접 확인했다

**마무리 확인 질문**
1. 상품이 화면에 나타나기까지 거치는 단계를 순서대로 말해 보세요.
2. CORS 오류는 왜 생기고 어디를 고쳐서 해결했나요?
3. 가짜 데이터에서 DB로 바꿀 때 프론트를 고치지 않아도 된 이유는?
4. router, service, repository는 각각 무슨 일을 하나요?
5. 응답 헤더 `content-type: application/json`은 브라우저에게 무엇을 알려 주나요?
6. 상태코드 200, 404, 405, 500은 각각 어떤 상황인가요?

---

## 부록 A. HTTP 기초 (HTTP 실습 전 10분 설명용)

### A-1. 요청과 응답의 구조
```
[ 요청 Request ]
GET /api/v1/products HTTP/1.1          <- 시작줄: 방식(Method) + 주소(Path) + 버전
Host: localhost:8000                   <- 헤더들 (이름: 값)
Origin: http://localhost:5173
Accept: */*
                                       <- 빈 줄 (헤더 끝)
(본문 Body: GET 은 보통 없음)

[ 응답 Response ]
HTTP/1.1 200 OK                        <- 상태줄: 버전 + 상태코드 + 설명
content-type: application/json         <- 헤더들
access-control-allow-origin: http://localhost:5173
content-length: 554
                                       <- 빈 줄
[{"id":1,"name":"콜라", ...}]          <- 본문 Body: 실제 데이터
```
- **시작줄/상태줄**: 무엇을 요청했고 결과가 어땠는지
- **헤더**: 본문을 설명하는 부가 정보 (형식, 크기, 허용 여부, 캐시, 인증 등)
- **본문**: 실제 데이터 (JSON, HTML, 이미지 ...)

### A-2. 이번 프로젝트에서 실제로 보이는 헤더
아래는 이 프로젝트 서버에서 확인한 응답이다.

**`GET /api/v1/products` 응답**
| 헤더 | 값 (실제) | 의미 |
|------|-----------|------|
| `content-type` | `application/json` | 본문이 JSON이다. 브라우저/`fetch().json()`이 이를 보고 해석한다 |
| `content-length` | `554` | 본문 크기(바이트) |
| `server` | `uvicorn` | 응답한 서버 프로그램 |
| `date` | 응답 시각 | |
| `access-control-allow-origin` | `http://localhost:5173` | **CORS 허용 표시.** 이 헤더가 있어야 브라우저가 React에게 응답을 넘겨준다 |
| `vary` | `Origin` | 요청한 Origin에 따라 응답이 달라질 수 있다는 표시 (캐시용) |

**이미지 `GET /products/images/cola.svg` 응답**
| 헤더 | 값 (실제) | 의미 |
|------|-----------|------|
| `content-type` | `image/svg+xml` | 본문이 SVG 이미지다 (JSON과 다름!) |
| `etag` | `"c6bb6eba..."` | 파일 버전 표시. 같으면 브라우저가 다시 받지 않을 수 있다 |
| `last-modified` | 파일 수정 시각 | 캐시 판단용 |
| `accept-ranges` | `bytes` | 파일을 부분적으로 받을 수 있다 |

**자주 쓰는 요청 헤더**
| 헤더 | 의미 |
|------|------|
| `Origin` | 요청을 보낸 페이지의 출처. CORS 검사의 기준 (`http://localhost:5173`) |
| `Host` | 요청 대상 서버 (`localhost:8000`) |
| `Accept` | 받고 싶은 응답 형식 |
| `Content-Type` | (본문이 있을 때) 보내는 본문의 형식. 나중에 로그인/가입(POST)에서 `application/json` |
| `Authorization` | 로그인 토큰. **Level 02~03에서 사용 예정** |
| `User-Agent` | 브라우저/도구 종류 |

### A-3. 상태코드 (이번 수업에서 만나는 것)
| 코드 | 의미 | 이 프로젝트에서 보는 경우 |
|:--:|------|---------------------------|
| 200 OK | 성공 | 상품 목록, 이미지 정상 응답 |
| 304 Not Modified | 변경 없음 (캐시 사용) | 이미지를 다시 요청했을 때 (개발자 도구 확인) |
| 404 Not Found | 주소 없음 | 없는 주소 `/api/v1/nothing`, 없는 이미지 |
| 405 Method Not Allowed | 방식이 틀림 | `POST /api/v1/products` (응답에 `allow: GET` 헤더가 붙는다) |
| 422 | 입력값 검증 실패 | (이후 레벨) |
| 500 Internal Server Error | 서버 내부 오류 | DB 접속 실패 시 (서버 코드의 `HTTPException`) |

### A-4. 메서드(방식) 간단 표
| 메서드 | 의미 | 앞으로 쓰는 곳 |
|--------|------|----------------|
| GET | 조회 | 상품 목록 (이번 수업) |
| POST | 생성 | 회원가입, 주문 (Level 02~) |
| PUT / PATCH | 수정 | 재고 수정 (관리자) |
| DELETE | 삭제 | 장바구니/상품 삭제 |
| OPTIONS | "이 요청 보내도 되나요?" 사전 확인 (CORS preflight) | 브라우저가 자동으로 보냄 |

---

## 부록 B. 개발자 도구로 HTTP 요청/응답 확인하기 (2회차, 20분)

### B-1. 준비
1. 백엔드(`:8000`), 프론트(`:5173`)를 모두 실행한다.
2. Chrome 또는 Edge에서 `http://localhost:5173`을 연다.
3. **`F12`** (또는 우클릭 → 검사)로 개발자 도구를 열고 **Network(네트워크)** 탭을 선택한다.
4. 설정 확인
   - [x] **Disable cache** 체크 (실습 중 캐시 때문에 헷갈리지 않도록)
   - [x] **Preserve log** 체크 (페이지가 새로고침되어도 기록 유지)

> 개발자 도구를 **연 상태에서** 새로고침(`F5` 또는 `Ctrl + R`)해야 요청이 기록된다.

### B-2. 실습 순서

**실습 1. 요청 목록 읽기 (5분)**
1. 새로고침 후 Name 목록을 본다. 상품 API 요청(`products`)과 이미지 요청(`cola.svg` 등)이 보인다.
2. 열 머리글에서 확인할 것: **Name / Status / Type / Size / Time**
3. 필터에서 **Fetch/XHR**를 누르면 `fetch`로 보낸 API 요청만 보인다. **Img**를 누르면 이미지 요청만 보인다.
4. 질문: 이미지 요청은 몇 개인가? 왜 그 개수일까? (카드 수 = 6)

**실습 2. 요청 하나 자세히 보기 (8분)**
1. `products` 요청을 클릭한다.
2. **Headers 탭**의 구성
   | 영역 | 내용 |
   |------|------|
   | General | Request URL, Request Method(GET), Status Code(200), Remote Address(`[::1]:8000` 등) |
   | Response Headers | `content-type`, `access-control-allow-origin`, `content-length`, `server` ... |
   | Request Headers | `Host`, `Origin`, `Accept`, `User-Agent` ... |
3. 찾아 보기 과제
   - [ ] 요청 메서드는? (GET)
   - [ ] 상태코드는? (200)
   - [ ] 응답의 `content-type`은? (application/json)
   - [ ] 요청 헤더 `Origin`의 값은? (`http://localhost:5173`)
   - [ ] 응답 헤더 `access-control-allow-origin`의 값은? **두 값이 같다는 점**이 CORS 통과 조건
4. **Preview 탭**: JSON을 접고 펼쳐서 보여 준다. **Response 탭**: 서버가 보낸 원문 그대로.
5. **Timing 탭**: 요청이 걸린 시간(대기, 다운로드)을 본다.

**실습 3. 이미지 요청과 비교 (3분)**
1. `cola.svg` 요청을 클릭하고 Headers를 본다.
2. `content-type`이 `image/svg+xml`로 JSON과 다른 것을 확인한다. **같은 서버라도 응답의 종류가 다르다.**
3. `etag`, `last-modified`가 있는 것을 확인한다. (캐시 관련. "Disable cache"를 끄고 새로고침하면 Status가 `304` 또는 `(memory cache)`로 바뀔 수 있다)

**실습 4. 오류 요청 만들어 보기 (4분)**
1. 브라우저 새 탭에서 `http://localhost:8000/api/v1/nothing` 접속 → 404와 `{"detail":"Not Found"}`를 본다.
2. 백엔드 서버를 끄고 `localhost:5173`을 새로고침한다. Network 탭에서 상품 요청이 **(failed)**로 표시된다. 화면에는 "오류: Failed to fetch"가 나온다.
3. (선택) `v0.1-step2-1` 태그에서 CORS 오류를 보면, 요청은 서버에 도착해 `200`이지만 **응답 헤더에 `access-control-allow-origin`이 없다**는 점과 Console의 CORS 오류 메시지를 함께 보여 준다.

### B-3. 알아 두면 좋은 기능
| 기능 | 위치 | 용도 |
|------|------|------|
| Copy as cURL | 요청 우클릭 → Copy → Copy as cURL (bash) | 브라우저가 보낸 요청을 터미널에서 똑같이 재현. **3회차 터미널 실습과 연결** |
| Console 탭 | | CORS 오류 메시지, `console.log` 확인 |
| Throttling | Network 탭 상단 "No throttling" | 느린 네트워크 흉내 → "불러오는 중..." 화면 길게 보기 |
| 정렬/검색 | 필터 입력창 | 요청이 많을 때 `products`만 골라 보기 |

### B-4. 정리 질문
- 브라우저 주소창 입력은 어떤 메서드의 요청인가?
- 요청 헤더 `Origin`과 응답 헤더 `access-control-allow-origin`은 CORS에서 어떤 관계인가?
- `content-type`이 중요한 이유는?

---

## 부록 C. 터미널에서 HTTP 요청 보내기 (3회차, 25분)

프론트 없이 백엔드만 직접 호출해 보는 실습이다. **브라우저를 거치지 않으므로 CORS 검사는 적용되지 않는다.** 이 차이를 마지막에 확인한다.

### C-1. curl (Git Bash 또는 PowerShell)

> **Windows 주의**: PowerShell에서 `curl`은 `Invoke-WebRequest`의 별명이라 옵션이 다르게 동작한다. 진짜 curl은 **`curl.exe`**로 입력한다. (Git Bash에서는 `curl`)

| 목적 | 명령 | 확인할 것 |
|------|------|-----------|
| 본문만 보기 | `curl http://localhost:8000/api/v1/products` | JSON 6개 |
| **헤더 + 본문** | `curl -i http://localhost:8000/api/v1/products` | 상태줄, `content-type` |
| 헤더만 (HEAD) | `curl -I http://localhost:8000/products/images/cola.svg` | `image/svg+xml`, `etag` |
| 요청/응답 전체 과정 | `curl -v http://localhost:8000/api/v1/products` | `>` 요청 줄, `<` 응답 줄 |
| 헤더 추가 | `curl -i -H "Origin: http://localhost:5173" http://localhost:8000/api/v1/products` | `access-control-allow-origin` 생김 |
| 없는 주소 | `curl -i http://localhost:8000/api/v1/nothing` | 404 |
| 잘못된 메서드 | `curl -i -X POST http://localhost:8000/api/v1/products` | 405 + `allow: GET` |
| 사전 확인(OPTIONS) | `curl -i -X OPTIONS http://localhost:8000/api/v1/products -H "Origin: http://localhost:5173" -H "Access-Control-Request-Method: GET"` | `access-control-allow-methods`, `access-control-max-age` |

**`curl -v` 출력 읽는 법**
```
> GET /api/v1/products HTTP/1.1      <- ">" 로 시작: 내가 보낸 요청
> Host: localhost:8000
> Accept: */*
>
< HTTP/1.1 200 OK                    <- "<" 로 시작: 서버가 돌려준 응답
< content-type: application/json
<
[{"id":1,...}]                       <- 본문
```

**비교 실험 (CORS는 브라우저 규칙)**
1. `Origin` 헤더 없이 호출 → 응답에 `access-control-allow-origin`이 **없다** (그래도 데이터는 받는다)
2. `-H "Origin: http://localhost:5173"` 추가 → 헤더가 붙는다
3. `-H "Origin: http://localhost:9999"` → 허용되지 않은 출처이므로 헤더가 **붙지 않는다**
4. 결론: 서버는 `Origin`을 보고 헤더만 붙이거나 안 붙인다. **막는 주체는 브라우저**다.

### C-2. PowerShell
```powershell
# 상태코드와 헤더 보기
$res = Invoke-WebRequest http://localhost:8000/api/v1/products -UseBasicParsing
$res.StatusCode                 # 200
$res.Headers['Content-Type']    # application/json
$res.Headers                    # 모든 응답 헤더

# JSON 을 바로 객체로 받기
$items = Invoke-RestMethod http://localhost:8000/api/v1/products
$items.Count                    # 6
$items | Format-Table id, name, price, stock

# 헤더를 추가해서 호출
Invoke-WebRequest http://localhost:8000/api/v1/products -Headers @{ Origin = "http://localhost:5173" } -UseBasicParsing |
  Select-Object -ExpandProperty Headers
```
- 콘솔에서 한글이 깨져 보이면 출력 인코딩 문제일 수 있다. 데이터 자체는 정상이다.

### C-3. Python 표준 라이브러리 (설치 불필요)
`backend`의 가상환경에서 실행한다. 아래 코드는 서버를 켠 상태에서 실행 확인을 마쳤다.

`http.client` : HTTP 메시지를 가장 낮은 수준으로 보여 준다
```python
import http.client
import json

# 1) 서버에 연결
conn = http.client.HTTPConnection("localhost", 8000)

# 2) 요청 보내기 : 메서드, 주소, 헤더
conn.request("GET", "/api/v1/products", headers={"Origin": "http://localhost:5173"})

# 3) 응답 받기
res = conn.getresponse()
print(res.status, res.reason)            # 200 OK
for name, value in res.getheaders():     # 응답 헤더 전체
    print(f"{name}: {value}")

# 4) 본문(바이트)을 문자열로 바꾸고 JSON 으로 해석
products = json.loads(res.read().decode("utf-8"))
print(len(products), products[0]["name"])
conn.close()
```

`urllib.request` : 더 간단한 표준 도구
```python
import json
import urllib.request

with urllib.request.urlopen("http://localhost:8000/api/v1/products") as res:
    print(res.status, res.headers["Content-Type"])   # 200 application/json
    products = json.load(res)
    print(len(products))                             # 6
```

### C-4. Python `requests` 모듈 (설치 필요)
```powershell
cd D:\AX_WORK\VMFullStack\backend
.venv\Scripts\Activate.ps1
pip install requests
```
> `requests`는 수업 실습용 도구라서 프로젝트의 `requirements.txt`에는 넣지 않는 것을 권한다. (`pip freeze > requirements.txt`를 다시 실행하면 같이 들어가니 주의) 이 환경에서는 모듈이 설치되어 있지 않아 **아래 예제는 실행 검증을 하지 못했다.** 수업 전에 리허설한다.

```python
import requests

url = "http://localhost:8000/api/v1/products"

res = requests.get(url, headers={"Origin": "http://localhost:5173"})

print(res.status_code)                       # 200
print(res.headers["content-type"])           # application/json
print(res.headers.get("access-control-allow-origin"))

products = res.json()                        # JSON 을 파이썬 리스트로
for p in products:
    print(p["id"], p["name"], p["price"], p["stock"])

# 없는 주소 : 오류도 코드로 확인
bad = requests.get("http://localhost:8000/api/v1/nothing")
print(bad.status_code, bad.json())           # 404 {'detail': 'Not Found'}
```

### C-5. 도구별 비교
| 도구 | 설치 | 특징 | 쓰는 때 |
|------|------|------|---------|
| 브라우저 개발자 도구 | 없음 | 화면이 보낸 **실제 요청**을 그대로 관찰 | 프론트-백엔드 연동 문제 추적 |
| `curl` / `curl.exe` | 거의 기본 | 가장 빠르게 요청/헤더 확인 | API 단독 점검, 문서에 예시로 넣기 |
| PowerShell `Invoke-*` | 없음 | 결과를 객체로 다룸 | Windows에서 간단한 점검 |
| Python `http.client` / `urllib` | 없음 | 표준 라이브러리, 원리 학습 | 외부 설치 없이 스크립트 |
| Python `requests` | `pip install` | 가장 읽기 쉬움 | 자동화 스크립트, 테스트 |
| Swagger `/docs` | 없음 | 클릭으로 호출 | 수업 시연, 팀 공유 |

### C-6. 실습 과제 (선택)
1. `curl -i`로 상품 API를 호출하고 헤더 5개의 의미를 노트에 적는다.
2. Python 스크립트로 상품 6개의 **총 재고 수량**을 계산해 출력한다.
3. DB에서 콜라 재고를 0으로 바꾼 뒤, 같은 스크립트를 다시 실행해 결과가 바뀌는 것을 확인한다.
4. 개발자 도구의 **Copy as cURL**로 복사한 명령을 터미널에서 실행해 같은 응답이 나오는지 비교한다.

---

## 부록 D. 진행 팁과 운영

### D-1. 전체 시간표 요약
| 회차 | 0~10 | 10~55 | 55~60 | 60~110 | 110~120 |
|:--:|------|-------|-------|--------|---------|
| 1 | 오프닝 | 구조 + 0단계 | 휴식 | 1단계 + 실습 | 정리 |
| 2 | 복습 | 2-1~2-4 | 휴식 | CORS, 이미지, **개발자 도구** | 정리 |
| 3 | 복습 | DB 준비, 3-3~3-7 | 휴식 | 확인, **터미널 도구**, 마무리 | 질문/예고 |

### D-2. Git 태그로 수업 진행하기
| 상황 | 명령 |
|------|------|
| 현재 상태 저장 | `git add .` → `git commit -m "메시지"` |
| 정답 코드 확인 | `git checkout v0.1-step1` / `v0.1-step2` / `v0.1-step3` |
| 작업 브랜치로 복귀 | `git checkout v0.1/step3-db` |
| CORS 오류 재현 | `git checkout v0.1-step2-1` |
- 태그를 옮기면 백엔드 서버를 **재시작**해야 코드가 반영될 수 있다.
- 수강생이 따라가지 못하면 해당 단계의 태그로 맞춰 주면 다음 단계에서 같은 출발선에 설 수 있다.

### D-3. 수업 운영 팁
- 코드를 칠 때마다 **결과를 눈으로 확인**하는 단계를 꼭 넣는다. (Swagger, 브라우저, DB 조회)
- 오류가 나면 지우지 말고 **오류 메시지를 읽는 연습**을 시킨다. (Console, 서버 터미널, Network 탭의 3곳을 순서대로 보기)
- 백엔드와 프론트를 모두 켜야 한다는 점을 반복해서 상기시킨다.
- 속도가 느린 수강생은 "정답 태그로 맞추고 다음으로" 원칙으로 수업 흐름을 지킨다.

### D-4. 과제 (선택)
| 난이도 | 과제 |
|:--:|------|
| 하 | 상품을 이름으로 검색하는 입력창 만들기 (프론트 `useState` 필터링) |
| 하 | 재고 5개 이하 상품에 "품절 임박" 표시 |
| 중 | `GET /api/v1/products/{id}` 상세 API 추가 (router, service, repository) |
| 중 | 새 상품을 `seed.sql`에 추가하고 이미지 SVG 한 개 직접 그려서 연결 |
| 상 | 터미널 스크립트로 상품 목록을 표 형태로 출력하는 도구 만들기 |

### D-5. 다음 수업 예고
**Level 02: 회원가입**: 폼 입력, `POST` 요청과 `Content-Type: application/json` 헤더, 요청 본문, INSERT, 비밀번호 해시(bcrypt), 이메일 중복 처리(409), 입력 검증 오류(422).
이번 수업에서 배운 개발자 도구와 curl로 **POST 요청의 본문과 헤더**를 확인하는 것이 연결 고리가 된다.
