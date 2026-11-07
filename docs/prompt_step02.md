# prompt_step02 - 대화 기록

프로젝트: 웹용 음료수 자판기 (간단한 쇼핑몰) / 입문자용 풀스택 학습
이전 기록: `prompt_step01.md` (요구사항, 일정, 개발 흐름, Docker 미사용·로컬 MariaDB 전제 변경까지 포함)

---

## 1. 강의용 단계별 코드 생성 (level01.md)

**사용자**
> 그럼 지금부터 내가 주도적으로 강의를 진행할 수 있도록 코드를 생성해줘, 먼저 level01.md 파일에 너가 제시한 아래 내용을 단계별로 분리해서 코드를 생성해줘, 물론 개발환경 설정 작업부터 0단계: 개발환경 설정으로 해주고
>
> 1단계: 가짜 데이터로 화면 먼저 (프론트)
> - Vite로 React 프로젝트를 만들고 상품 카드 컴포넌트를 만듭니다.
> - 코드에 박아 둔 배열로 목록을 그립니다. (useState)
>
> 2단계: 백엔드 연결
> - FastAPI로 GET /api/v1/products를 만듭니다. 처음에는 코드에 박아 둔 JSON을 반환합니다.
> - React에서 useEffect + fetch로 호출해 화면에 표시합니다. (CORS를 이때 처음 만납니다.)
>
> 3단계: DB 연결
> - MariaDB를 띄우고 products 테이블과 샘플 데이터를 넣습니다.
> - 백엔드의 하드코딩 JSON을 SELECT 쿼리로 교체합니다. (repositories/)
> - 프론트는 수정하지 않아도 그대로 동작합니다. 계층 분리의 효과를 직접 확인하게 됩니다.

**요약 답변**
- `docs/level01.md` 생성. 강사가 직접 타이핑하며 진행하는 **강의용 정답 코드**이며, 실행 검증은 하지 않았음(수업 전 강사 PC에서 리허설 권장)
- 단계 구성(약 4시간, 12일 일정의 1~2일차)

| 단계 | 내용 |
|:--:|------|
| 0 | 설치 확인, 폴더 구조, `.gitignore`, Python 가상환경 + `pip install`, Vite 생성, 첫 커밋 |
| 1 | `ProductCard` 컴포넌트, 하드코딩 배열 + `useState`, "목록 비우기/채우기" 버튼 |
| 2 | FastAPI 하드코딩 API, `useEffect` + `fetch`, **CORS 오류를 일부러 겪은 뒤 미들웨어로 해결** |
| 3 | `init.sql`/`schema.sql`/`seed.sql`, `.env`, `database.py`, router → service → repository 계층, SELECT 쿼리 |

- 단계마다 학습 목표, 파일별 전체 코드, 실행 방법, 체크포인트, 강의 포인트, 자주 나는 오류 수록
- 문서 끝에 전체 요청 흐름도, 수강생 확인 질문 5개, 도전 과제, 다음 레벨(Level 02 회원가입) 예고 포함
- 설계 결정
  - 가짜 데이터의 필드(`id, name, price, stock, image_url`)를 API 응답과 동일하게 맞춰 3단계에서 프론트 수정이 필요 없도록 함
  - 학습 단순화를 위해 `image_url`에 이모지를 사용(실제 이미지 URL 교체는 이후 과제)
  - DB 계정 `vmshop_user` / 비밀번호 `vmshop1234`는 학습용 예시
  - DB 클라이언트 명령은 `mariadb`로 작성(설치본에 따라 `mysql`일 수 있음)
  - DB 연결은 요청마다 생성·종료(커넥션 풀은 이후 개선 과제)
- 실제 `frontend/`, `backend/` 프로젝트 파일은 생성하지 않음(시연용 완성본이 필요하면 별도 요청)

---

## 생성/변경된 파일
| 파일 | 내용 |
|------|------|
| `docs/level01.md` | Level 01 단계별 강의 가이드 및 코드 (0~3단계) |
| `docs/prompt_step02.md` | 본 대화 기록 |

## 남은 작업 (제안)
- 강사 PC에서 `level01.md` 0~3단계 리허설 및 오류 수정
- 시연용 완성본 프로젝트(`frontend/`, `backend/`, `db/`) 생성 여부 결정
- `docs/CLAUDE.md`의 "4. 프로젝트 기술적 요구사항" 채우기
- `docs/schedule.md` 작성, `docs/front.md`/`docs/back.md` 가이드 작성
- Level 02(회원가입) 강의 자료 작성
