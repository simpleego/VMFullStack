# DB / SQL 작업 정리 (dbSQL)

프로젝트: 웹용 음료수 자판기 / DB: MariaDB 11.8 (수강생 PC에 설치된 DB 사용, ORM 없이 SQL 직접 사용)

---

## 1. 요약

| 항목 | 값 |
|------|----|
| DB 이름 | `vmShop` (utf8mb4 / utf8mb4_general_ci) |
| 전용 계정 | `vmshop_user` @ `localhost` (학습용 비밀번호 `vmshop1234`) |
| 권한 | `vmShop.*` 에 대한 ALL PRIVILEGES |
| 호스트 / 포트 | `localhost` / `3306` |
| 테이블 | `users`, `products`, `orders`, `order_items` (4개) |
| 샘플 데이터 | `products` 6건 |
| 스크립트 위치 | `db/init.sql`, `db/schema.sql`, `db/seed.sql` |
| 접속 설정 | `backend/.env` (Git 제외), `backend/.env.example` (견본) |

- Level 01(상품 목록)에서 사용하는 테이블은 `products` 하나다. 나머지는 이후 레벨에서 사용한다.
- 비밀번호는 학습용 예시이며 실제 서비스에서는 사용하지 않는다. root 비밀번호는 이 문서에 적지 않는다.

---

## 2. 스크립트 구성

| 파일 | 실행 계정 | 역할 |
|------|-----------|------|
| [db/init.sql](../db/init.sql) | root | DB 생성, 전용 계정 생성, 권한 부여 |
| [db/schema.sql](../db/schema.sql) | vmshop_user | 테이블 생성 (기존 테이블은 삭제 후 재생성) |
| [db/seed.sql](../db/seed.sql) | vmshop_user | 샘플 데이터 입력 |

실행 순서는 항상 **init → schema → seed** 다.

- `init.sql`은 `IF NOT EXISTS`를 사용하므로 여러 번 실행해도 안전하다.
- `schema.sql`은 `DROP TABLE IF EXISTS`로 시작한다. **실행하면 모든 테이블의 데이터가 사라진다.** 외래키 때문에 `order_items → orders → products → users` 순서로 삭제한다.
- `seed.sql`은 INSERT만 하므로 `schema.sql` 없이 반복 실행하면 상품이 중복 입력된다.

---

## 3. 테이블 설계

### 3.1 관계도 (ERD)
```
users 1 ───< orders 1 ───< order_items >─── 1 products
 (회원)        (주문)         (주문상세)          (상품)
```
- 회원 1명은 주문을 여러 건 할 수 있다.
- 주문 1건에는 상품이 여러 개 담길 수 있다. (`order_items`)
- 상품 1개는 여러 주문 상세에 나타날 수 있다.

### 3.2 users (회원) - Level 02 이후
| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 회원 번호 |
| email | VARCHAR(100) | NOT NULL, UNIQUE | 로그인 ID, 중복 불가 |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 해시 (평문 저장 금지) |
| name | VARCHAR(50) | NOT NULL | 이름 |
| role | VARCHAR(10) | NOT NULL, 기본 `USER`, CHECK | `USER` / `ADMIN` |
| status | VARCHAR(10) | NOT NULL, 기본 `ACTIVE`, CHECK | `ACTIVE` / `BLOCKED` |
| created_at | DATETIME | NOT NULL, 기본 현재시각 | 가입일시 |

### 3.3 products (상품) - **Level 01 사용**
| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 상품 번호 |
| name | VARCHAR(50) | NOT NULL | 상품명 |
| price | INT | NOT NULL, CHECK ≥ 0 | 가격(원) |
| stock | INT | NOT NULL, 기본 0, CHECK ≥ 0 | 재고 수량 (음수 불가) |
| image_url | VARCHAR(255) | NULL | 이미지 경로 (파일은 서버 `backend/products/images` 폴더, 백엔드가 `/products/images/...` 주소로 제공) |
| description | VARCHAR(255) | NULL | 설명 |
| is_active | TINYINT(1) | NOT NULL, 기본 1 | 판매 여부 (0이면 목록에서 제외) |
| created_at | DATETIME | NOT NULL, 기본 현재시각 | 등록일시 |

### 3.4 orders (주문) - 이후 레벨
| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 주문 번호 |
| user_id | INT | NOT NULL, FK → users.id | 주문한 회원 |
| total_price | INT | NOT NULL | 총 금액 |
| status | VARCHAR(10) | NOT NULL, 기본 `PAID` | 가상 결제이므로 바로 결제완료 |
| created_at | DATETIME | NOT NULL, 기본 현재시각 | 주문일시 |

인덱스: `idx_orders_user_id`(내 주문 조회), `idx_orders_created_at`(기간별 조회)

### 3.5 order_items (주문 상세) - 이후 레벨
| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 상세 번호 |
| order_id | INT | NOT NULL, FK → orders.id | 소속 주문 |
| product_id | INT | NOT NULL, FK → products.id | 주문한 상품 |
| quantity | INT | NOT NULL, CHECK > 0 | 수량 |
| unit_price | INT | NOT NULL | **주문 당시** 단가 (이후 상품 가격이 바뀌어도 유지) |

### 3.6 샘플 데이터 (products)
| id | 상품 | 가격 | 재고 | image_url |
|:--:|------|-----:|-----:|:---------:|
| 1 | 콜라 | 1,500 | 10 | /products/images/cola.svg |
| 2 | 사이다 | 1,400 | 8 | /products/images/cider.svg |
| 3 | 오렌지주스 | 2,000 | 0 (품절) | /products/images/orange.svg |
| 4 | 생수 | 1,000 | 25 | /products/images/water.svg |
| 5 | 커피 | 2,500 | 5 | /products/images/coffee.svg |
| 6 | 녹차 | 1,800 | 12 | /products/images/greentea.svg |

관리자 계정은 bcrypt 해시가 필요하므로 회원가입을 배우는 Level 02에서 추가한다.

---

## 4. 실행 방법 (Windows PowerShell)

MariaDB 클라이언트가 PATH에 없으면 전체 경로를 사용한다.
```powershell
$m = "C:\Program Files\MariaDB 11.8\bin\mariadb.exe"
```
PATH에 `C:\Program Files\MariaDB 11.8\bin`을 추가했다면 `mariadb` 만 입력해도 된다. (설치본에 따라 `mysql`일 수 있다.)

### 4.1 최초 생성
```powershell
cd D:\AX_WORK\VMFullStack

# 1) DB와 계정 생성 (root 비밀번호를 물어본다)
cmd /c "`"$m`" -u root -p --default-character-set=utf8mb4 < db\init.sql"

# 2) 테이블 생성 (vmshop_user 비밀번호를 물어본다)
cmd /c "`"$m`" -u vmshop_user -p --default-character-set=utf8mb4 < db\schema.sql"

# 3) 샘플 데이터 입력
cmd /c "`"$m`" -u vmshop_user -p --default-character-set=utf8mb4 < db\seed.sql"
```
- PowerShell에서는 `<` 리다이렉션이 지원되지 않아 `cmd /c`를 거친다.
- HeidiSQL, DBeaver 등 GUI 도구에서 `.sql` 파일을 열어 실행해도 결과는 같다.

### 4.2 확인
```powershell
& $m -u vmshop_user -p --default-character-set=utf8mb4 -e "USE vmShop; SHOW TABLES; SELECT * FROM products;"
```
기대 결과: 테이블 4개(`order_items`, `orders`, `products`, `users`)와 상품 6행.

### 4.3 처음 상태로 초기화
데이터만 초기화(테이블 구조 유지 후 재생성):
```powershell
cmd /c "`"$m`" -u vmshop_user -p --default-character-set=utf8mb4 < db\schema.sql"
cmd /c "`"$m`" -u vmshop_user -p --default-character-set=utf8mb4 < db\seed.sql"
```

DB와 계정까지 완전히 삭제 후 처음부터 (수업 시연용):
```sql
-- root 로 접속해서 실행
DROP DATABASE IF EXISTS vmShop;
DROP USER IF EXISTS 'vmshop_user'@'localhost';
```
이후 4.1의 1)~3)을 다시 실행한다.

### 4.4 백업 / 복원
```powershell
# 백업 (파일로 저장)
& "C:\Program Files\MariaDB 11.8\bin\mariadb-dump.exe" -u vmshop_user -p --default-character-set=utf8mb4 vmShop --result-file=backup_vmShop.sql

# 복원
cmd /c "`"$m`" -u vmshop_user -p --default-character-set=utf8mb4 vmShop < backup_vmShop.sql"
```
백업 파일에는 데이터가 들어 있으므로 Git에 올리지 않는다.

---

## 5. 백엔드 접속 설정

`backend/.env` (실제 사용, **Git 제외**)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=vmshop_user
DB_PASSWORD=vmshop1234
DB_NAME=vmShop
```
`backend/.env.example`은 같은 형식에 비밀번호만 비운 견본이며 Git에 포함한다.

Python 접속 방식은 [level01.md](level01.md) 3단계(`database.py`, PyMySQL)를 참고한다.

---

## 6. 자주 쓰는 SQL

```sql
USE vmShop;

-- 판매 중인 상품 목록 (Level 01 API 가 사용하는 쿼리)
SELECT id, name, price, stock, image_url
FROM products
WHERE is_active = 1
ORDER BY id;

-- 재고 변경 (화면이 따라 바뀌는지 실험용)
UPDATE products SET stock = 0 WHERE name = '콜라';
UPDATE products SET stock = 10 WHERE name = '콜라';   -- 원복

-- 상품 판매 중지 / 재개 (목록에서 사라지는지 확인)
UPDATE products SET is_active = 0 WHERE id = 6;
UPDATE products SET is_active = 1 WHERE id = 6;

-- 제약조건 확인: 재고를 음수로 바꾸면 거부된다
UPDATE products SET stock = -1 WHERE id = 1;   -- CHECK 제약 위반 오류

-- 테이블 구조 확인
DESCRIBE products;
SHOW CREATE TABLE products;
```

---

## 7. 문제 해결

| 증상 | 원인 / 조치 |
|------|-------------|
| `mariadb` 명령을 찾을 수 없음 | PATH에 `C:\Program Files\MariaDB 11.8\bin` 추가 또는 전체 경로 사용 |
| `Access denied for user` | 계정/비밀번호 확인. `.env`의 값이 `init.sql`과 같은지 확인 |
| `Can't connect to MySQL server` | MariaDB 서비스 실행 여부 확인 (`services.msc` → MariaDB), 포트 3306 확인 |
| `Unknown database 'vmShop'` | `init.sql`을 먼저 실행했는지 확인 |
| 한글/이모지가 `?`로 보임 | `--default-character-set=utf8mb4` 옵션 확인. 콘솔 출력 문제일 수 있으니 GUI 도구로 재확인 |
| 상품이 12건 등으로 중복됨 | `seed.sql`을 반복 실행한 경우. `schema.sql` → `seed.sql` 순서로 초기화 |
| `SHOW DATABASES`에 `vmshop`(소문자)으로 보임 | Windows의 MariaDB는 DB 이름을 소문자로 저장한다. SQL에서는 `vmShop`으로 써도 동작한다 |

---

## 8. 작업 이력

| 작업 | 상태 |
|------|------|
| MariaDB 11.8 서비스 실행 확인, root 접속 확인 | 완료 |
| `vmShop` DB, `vmshop_user` 계정 생성 (`init.sql`) | 완료 |
| 4개 테이블 생성 (`schema.sql`) | 완료 |
| 상품 샘플 6건 입력 (`seed.sql`) | 완료 |
| `vmshop_user`로 SELECT 조회 확인 | 완료 |
| 관리자 계정 seed | Level 02에서 진행 |
| 주문 관련 SQL(트랜잭션, 재고 차감) | 이후 레벨에서 진행 |
