# prompt_step03 - 대화 기록

프로젝트: 웹용 음료수 자판기 (간단한 쇼핑몰) / 입문자용 풀스택 학습
이전 기록: `prompt_step01.md`(요구사항·일정·개발 흐름·로컬 환경 전제), `prompt_step02.md`(level01.md 생성)
이번 기록 범위: 개발환경 준비 → DB 생성 → 1단계 코드 → 2단계 코드(Git 버전 관리) → 코드 주석

---

## 1. 개발환경 준비

**사용자**
> 그럼 내가 수업준비해야 하니 개발환경 준비를 진행해줘

**요약 답변**
- 설치 확인: Python 3.12.0, Node v24.19.0, npm 11.17.0, Git 2.55.0, MariaDB 11.8 서비스 실행 중
- 수행: `git init`, `.gitignore`, `db/`·`backend/` 폴더, `backend/.venv` 생성 + 패키지 설치(fastapi, uvicorn, pymysql, python-dotenv) + `requirements.txt`, Vite + React로 `frontend/` 생성 및 `npm install`, 개발서버 응답(200) 확인
- 문제: `mariadb`/`mysql` 명령이 PATH에 없음 (실제 위치 `C:\Program Files\MariaDB 11.8\bin`). PATH 추가 또는 전체 경로 사용 필요

**사용자** > db root 비번은 pjc0129

- root 접속과 버전(11.8.9) 확인. 비밀번호는 환경변수로 한 번만 사용하고 어떤 파일에도 저장하지 않음
- 기존 DB(`counsel_survey`, `todo_course`, `test`)가 있으나 이번 프로젝트와 충돌 없음

---

## 2. DB 생성 (vmShop)

**사용자**
> vmShop으로 DB를 생성하고 테이블은 적당한 이름으로 생성해줘

**요약 답변**
- `db/init.sql`, `db/schema.sql`, `db/seed.sql` 작성 후 실행
- DB `vmShop`(utf8mb4), 전용 계정 `vmshop_user`(비밀번호 `vmshop1234`, 학습용)
- 테이블 4개: `users`, `products`, `orders`, `order_items` (외래키, UNIQUE, CHECK, 인덱스 포함), 상품 샘플 6건
- `backend/.env`(Git 제외), `backend/.env.example` 작성
- `level01.md`, `prompt_step02.md`의 `vending` 이름을 `vmShop` 계열로 수정, 3-2에 "4개 테이블 중 이번 레벨은 products만 사용" 안내 추가
- 관리자 계정 seed는 bcrypt 해시가 필요하므로 Level 02로 이월
- Windows는 DB 이름을 소문자(`vmshop`)로 저장하지만 SQL에서는 `vmShop`으로 써도 동작

---

## 3. DB 작업 문서화

**사용자** > DB 관련 작업은 dbSQL.md로 정리해줘

**요약 답변**
- `docs/dbSQL.md` 생성: 요약, 스크립트 구성(init → schema → seed), 테이블 설계(ERD·컬럼), 실행/확인/초기화/백업·복원 방법, `.env` 설정, 자주 쓰는 SQL, 문제 해결, 작업 이력
- `schema.sql` 실행 시 데이터가 모두 지워진다는 경고, `seed.sql` 반복 실행 시 중복된다는 주의 명시

---

## 4. 상품 이미지를 서버 폴더 방식으로 변경

**사용자**
> (seed.sql의 INSERT 문을 붙여 넣고) imgurl을 실제 상품이미지가 있는 사이트를 참고하도록 해줘, 상품이미지 사이트는 현재 서버의 products/images 폴더에 이미지가 있다고 가정하고 연결해줘, 가능하면 현재 insert 명령어에 있는 상품이미지를 준비해 주면 좋겠고

**요약 답변**
- `backend/products/images/`에 직접 그린 SVG 6개 생성: `cola`, `cider`, `orange`, `water`, `coffee`, `greentea` (저작권 문제 없음, XML 검증 완료)
- `seed.sql`의 `image_url`을 `/products/images/cola.svg` 같은 경로로 변경, DB 재적재 후 6건 확인
- DB에는 파일이 아니라 **경로 문자열만** 저장, 파일은 서버 폴더에 두고 FastAPI `StaticFiles`로 `/products/images` 주소로 공개
- `level01.md`에 **2-7 "상품 이미지 연결"** 추가, 3단계 seed·폴더 구조 수정, `dbSQL.md` 반영

---

## 5. 1단계 코드 생성 및 실행

**사용자**
> 그럼 아래 작업 코드를 생성해줘 — 1단계: 가짜 데이터로 화면 먼저 (프론트)

- 생성: `ProductCard.jsx/.css`, `App.jsx`(가짜 데이터 + `useState` + 목록 비우기/채우기 버튼), `App.css`, `index.css`, `index.html`(lang ko, 제목 "음료수 자판기"). 빌드 통과
- 참고: `src/assets/`의 Vite 샘플 이미지는 미사용 상태로 남음

**사용자** > 그럼 프론트엔드 실행해줘

- `npm run dev` 백그라운드 실행, `http://localhost:5173` 응답(200) 확인

---

## 6. Vite 빌드 체험 방법

**사용자**
> 혹시 배포전에 빌드 기능을 체험해 보고 싶은데 vite로 빌드하는 방법을 알려줘

**요약 답변**
- `npm run build` → `frontend/dist/`(index.html + 해시가 붙은 js/css), `npm run preview`(:4173)로 미리보기
- 개발 모드 vs 빌드 비교 표(용도, 파일, 압축, HMR, Node 필요 여부)
- 체험 실험: 압축된 JS 확인, 코드 수정 후 해시 변경 확인, `file://`로 열면 빈 화면이 될 수 있음
- 이 `dist`는 이후 배포 단계에서 FastAPI `StaticFiles`로 제공할 결과물

---

## 7. 2단계 구현 + Git 버전/브랜치 관리 (v0.1)

**사용자**
> 아래 단계를 수행하는데 반드시 단계를 구분해서 진행할 수 있도록 버전을 0.1로 생성해서 진행해줘 물론 git 브랜치로 생성해서 관리해줘 — 2단계: 백엔드 연결 (GET /api/v1/products 하드코딩 JSON, React에서 useEffect + fetch, CORS)

**요약 답변**
- Git 구성
  - 기본 브랜치는 `master`. 커밋이 없어서 0~1단계를 먼저 커밋(`9ca261a`)하고 태그 `v0.1-step1` 부여
  - 2단계는 `v0.1/step2-backend` 브랜치에서 진행 (`master`에 합치지 않음)
  - CORS 오류 장면을 수업에서 재현할 수 있도록 커밋·태그를 분리

| 태그 | 상태 | 용도 |
|------|------|------|
| `v0.1-step1` | 가짜 데이터 화면 | 1단계 완료 지점 |
| `v0.1-step2-1` | 하드코딩 API + fetch 연동, CORS 미적용 | 오류 화면 체험용 |
| `v0.1-step2-2` | CORS 미들웨어 추가 | 해결 후 |
| `v0.1-step2` | 서버 이미지 연결 | 2단계 완료 지점 |

- 생성 코드
  - 백엔드: `app/main.py`(라우터 등록, CORS, 이미지 폴더 공개), `app/routers/products.py`
  - 프론트: `api/products.js`(`fetchProducts`, `API_BASE`), `App.jsx`(`useEffect` + `fetch` + 로딩/오류 상태), `ProductCard.jsx`(`<img>`로 서버 이미지 표시)
- 확인: 2-1 시점에는 `access-control-allow-origin` 헤더 없음, CORS 적용 후 `http://localhost:5173` 출처에만 헤더 부여, 이미지 200(`image/svg+xml`), 프론트 빌드 통과. 브라우저 화면은 직접 확인하지 못함
- 문제: Windows에서 백그라운드 `--reload`가 재시작을 끝내지 못해 옛 코드가 응답함 → 서버를 완전히 껐다 켜서 해결 (수업에서는 보이는 터미널에서 실행 권장)
- 실행 중: 프론트 `:5173`, 백엔드 `:8000`

---

## 8. 라우터 동작 원리 설명

**사용자** > 백엔드 라우터 기능을 사용했는데 어떤 원리로 가능한지 설명해줘

**요약 답변**
- 라우터 = "주소 + 방식 → 함수" 안내 표(식당의 주문 창구 비유)
- `@router.get("")` 데코레이터는 서버 시작 시 등록 정보를 저장함, `prefix`와 경로가 합쳐져 최종 주소가 됨
- `include_router`로 앱에 연결해야 동작(빼면 404), 파일을 나누는 이유
- 요청 흐름: 브라우저 → Uvicorn(통신, ASGI) → FastAPI(미들웨어 → 라우팅 → 함수 호출) → JSON 변환 → 응답
- FastAPI가 자동으로 해 주는 일(JSON 변환, 200/404/405, Swagger 문서)과 확인용 실험 4가지
- 3단계 연결 예고: router(창구) → service(업무) → repository(SQL)

---

## 9. 서버 코드에 입문자용 주석 추가

**사용자** > 서버코드에 주석으로 입문자가 이해할 수 있도록 충분한 설명을 달아줘

**요약 답변**
- `backend/app/main.py`, `backend/app/routers/products.py`에 설명 주석 추가 (동작 변경 없음, 문법 검사 통과, 재시작 후 API·이미지 정상 응답)
- 주요 내용: CORS의 원리와 주의점, `include_router`, `StaticFiles`/`mount`, `Path(__file__).parent.parent` 경로 계산, 라우터 prefix·데코레이터, 하드코딩 → DB 전환 예고, 응답 필드 의미
- **아직 커밋하지 않음** (`v0.1/step2-backend`에 수정 상태). `v0.1-step2` 태그의 코드에는 주석이 없음. `level01.md` 코드 블록은 주석 없는 간결한 버전 그대로

---

## 생성/변경된 파일
| 파일 | 내용 |
|------|------|
| `db/init.sql`, `db/schema.sql`, `db/seed.sql` | DB·계정 생성, 4개 테이블, 상품 샘플 6건(이미지 경로) |
| `backend/.env`, `backend/.env.example` | DB 접속 설정 (`.env`는 Git 제외) |
| `backend/products/images/*.svg` | 상품 이미지 6개 |
| `backend/app/main.py`, `backend/app/routers/products.py` | 2단계 서버 코드 (주석 포함, 미커밋) |
| `frontend/src/**` | 1~2단계 프론트 코드 (`App.jsx`, `ProductCard`, `api/products.js` 등) |
| `docs/dbSQL.md` | DB/SQL 작업 정리 |
| `docs/level01.md` | DB 이름 변경, 2-7 이미지 연결 추가 |
| `docs/prompt_step03.md` | 본 대화 기록 |

## Git 상태
- 브랜치: `master`(`v0.1-step1`), `v0.1/step2-backend`(현재)
- 태그: `v0.1-step1`, `v0.1-step2-1`, `v0.1-step2-2`, `v0.1-step2`
- 미커밋: 서버 코드 주석, `docs/prompt_step03.md` 등 문서 변경

## 남은 작업 (제안)
- 서버 코드 주석 커밋 (`Step2-4`로 분리, `v0.1-step2` 태그는 유지)
- 3단계(DB 연결)를 `v0.1/step3-db` 브랜치에서 진행
- `level01.md`에 주석 버전 코드·라우터 원리 설명 반영 여부 결정
- 2단계를 `master`에 합칠지 결정
- MariaDB `bin` 폴더 PATH 추가 및 `level01.md` 0단계 안내 반영
- `docs/CLAUDE.md`의 "4. 프로젝트 기술적 요구사항" 채우기, `front.md`/`back.md` 작성
