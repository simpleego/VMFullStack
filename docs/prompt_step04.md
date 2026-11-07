# prompt_step04 - 대화 기록

프로젝트: 웹용 음료수 자판기 (간단한 쇼핑몰) / 입문자용 풀스택 학습
이전 기록: `prompt_step01.md` ~ `prompt_step03.md`
이번 기록 범위: 작업 지시서 규칙 변경 확인 → 3단계(DB 연결) 구현

---

## 1. 3단계 구현 (DB 연결)

**사용자**
> 그럼 3단계 아래와 같이 진행해줘
>
> 3단계: DB 연결
> - MariaDB를 띄우고 products 테이블과 샘플 데이터를 넣습니다.
> - 백엔드의 하드코딩 JSON을 SELECT 쿼리로 교체합니다. (repositories/)
> - 프론트는 수정하지 않아도 그대로 동작합니다. 계층 분리의 효과를 직접 확인하게 됩니다.

**전제 (시스템 알림으로 확인된 변경)**
- `docs/CLAUDE.md`에 **코드 생성 규칙**이 추가됨
  - 입문 개발자를 고려하여 모든 코드에 상세한 주석을 단다.
  - 코드는 입문자 수준의 간단한 코드 위주로 작성한다.
- 3단계 코드는 이 규칙에 맞춰 모든 파일에 상세 주석을 달아 작성함

**요약 답변**
- 사전 정리: 3단계 브랜치를 만들기 전에 남아 있던 변경을 먼저 커밋
  - `Step2-4`: 서버 코드 주석 (태그 `v0.1-step2-4`)
  - docs 커밋: 코드 생성 규칙, `prompt_step03.md`
- 브랜치 `v0.1/step3-db` 생성 후 단계별 커밋·태그
- DB는 앞서 만들어 둔 `vmShop`/`products`(6건)를 그대로 사용, 접속 재확인

| 태그 | 내용 |
|------|------|
| `v0.1-step3-1` | `database.py` (`.env` 읽기, PyMySQL 접속, `DictCursor`) |
| `v0.1-step3` | repository / service / router 교체, DB 조회 완료 |

- 생성 코드

| 파일 | 역할 |
|------|------|
| `backend/app/database.py` | DB 접속 전담. 접속 정보는 `.env`에서 읽음 |
| `backend/app/repositories/product_repository.py` | `SELECT id, name, price, stock, image_url FROM products WHERE is_active = 1 ORDER BY id` 실행, `try/finally`로 연결 종료 |
| `backend/app/services/product_service.py` | 현재는 repository 결과를 전달만 하는 업무 계층(규칙이 생길 자리) |
| `backend/app/routers/products.py` | 하드코딩 제거, service 호출, 오류 시 500 + 일반 메시지(상세 오류는 서버 로그에만) |

- 검증 결과
  1. API가 DB의 상품 6건(이미지 경로 포함)을 반환
  2. DB에서 콜라 재고를 0으로 변경하면 API 응답도 0으로 변경
  3. 녹차를 `is_active = 0`으로 바꾸면 목록이 6건 → 5건
  4. 위 변경은 모두 원복 (6건, 콜라 재고 10)
  5. CORS 헤더 `http://localhost:5173` 정상
  6. 잘못된 DB 비밀번호로 띄우면 상태코드 500 응답 (본문 문구·서버 로그는 확인하지 못함)
  7. `frontend/` 변경 없음 (Git 비교로 확인) → 프론트 무수정 동작
- 브라우저 화면은 직접 확인하지 못함 (`http://localhost:5173`에서 확인 필요)
- 백엔드(8000), 프론트(5173) 서버 모두 실행 중

---

## Git 상태
- 브랜치: `master`(`v0.1-step1`), `v0.1/step2-backend`, `v0.1/step3-db`(현재)
- 태그 전체

| 태그 | 상태 |
|------|------|
| `v0.1-step1` | 가짜 데이터 화면 |
| `v0.1-step2-1` | 하드코딩 API + fetch, CORS 미적용 |
| `v0.1-step2-2` | CORS 해결 |
| `v0.1-step2` | 서버 이미지 연결 |
| `v0.1-step2-4` | 서버 코드 주석 |
| `v0.1-step3-1` | DB 연결 모듈 |
| `v0.1-step3` | DB 조회 완료 |

- 수업 시연 순서 예: `git checkout v0.1-step2`(하드코딩) → `git checkout v0.1-step3`(DB 조회) 비교, 복귀는 `git checkout v0.1/step3-db`

## 생성/변경된 파일
| 파일 | 내용 |
|------|------|
| `backend/app/database.py` | DB 접속 모듈 (신규) |
| `backend/app/repositories/product_repository.py` | SQL 실행 계층 (신규) |
| `backend/app/services/product_service.py` | 업무 계층 (신규) |
| `backend/app/routers/products.py` | 하드코딩 → service 호출로 교체 |
| `docs/prompt_step04.md` | 본 대화 기록 |

## 남은 작업 (제안)
- `docs/level01.md` 3단계 코드 블록을 주석 버전(실제 파일 기준)으로 갱신할지 결정
- 잘못된 비밀번호 시 500 응답 본문과 서버 로그 재확인
- 브라우저에서 5173 화면 확인
- `v0.1/step3-db`를 `master`에 합칠지 결정 (이전 브랜치도 함께 정리)
- MariaDB `bin` 폴더 PATH 추가 및 `level01.md` 0단계 안내 반영
- `docs/CLAUDE.md`의 "4. 프로젝트 기술적 요구사항" 채우기, `front.md`/`back.md` 작성
- Level 02(회원가입) 강의 자료 작성
