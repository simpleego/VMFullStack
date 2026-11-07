# VMFullStack - 웹용 음료수 자판기

입문자가 풀스택 전체 구조(**React → FastAPI → MariaDB**)를 한 계층씩 직접 코딩하며 이해하는 학습용 프로젝트입니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| 프론트엔드 | React (Vite) |
| 백엔드 | FastAPI (Python 3.11+), Uvicorn |
| 데이터베이스 | MariaDB 11.x (ORM 없이 PyMySQL로 SQL 직접 작성) |

## 진행 현황

**Level 01 - 상품 목록 조회** 완료 (프론트 → 백엔드 → DB 연결)

| 태그 | 내용 |
|------|------|
| `v0.1-step1` | 가짜 데이터로 화면 구성 |
| `v0.1-step2-1` | 하드코딩 상품 API + fetch 연동 (CORS 미적용) |
| `v0.1-step2-2` | CORS 해결 |
| `v0.1-step2` | 서버 상품 이미지 연결 |
| `v0.1-step2-4` | 서버 코드 주석 |
| `v0.1-step3-1` | DB 연결 모듈 |
| `v0.1-step3` | DB 조회 완료 (현재) |

수업에서는 `git checkout <태그>`로 단계별 코드를 비교하고, `git checkout master`로 돌아옵니다.

다음 단계는 Level 02(회원가입, 로그인)입니다.

## 폴더 구조

```
VMFullStack/
├─ frontend/   React 화면
├─ backend/
│  └─ app/     main.py, database.py, routers/, services/, repositories/
├─ db/         init.sql, schema.sql, seed.sql
└─ docs/       요구사항, 강의 자료, 대화 기록
```

백엔드는 `router → service → repository` 3계층으로 나뉩니다.

## 실행 방법

사전 준비: Python 3.11+, Node.js 20+, MariaDB 실행 중.

**1. DB**: `db/init.sql`, `db/schema.sql`, `db/seed.sql`을 순서대로 실행합니다.

**2. 백엔드**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # .env 에 DB 비밀번호 입력
uvicorn app.main:app --reload
```
API 문서: http://localhost:8000/docs

**3. 프론트엔드**
```powershell
cd frontend
npm install
npm run dev
```
화면: http://localhost:5173

## 문서

- [요구사항 정의서](docs/requirement.md)
- [Level 01 강의 자료](docs/level01.md)
- [유스케이스 / 유저 스토리](docs/usecase_userstory.md)
