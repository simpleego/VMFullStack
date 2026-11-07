# DictCursor를 사용하는 이유
> **SQL에서 필드명을 구체적으로 지정(`SELECT id, name FROM ...`)하더라도 `DictCursor`는 여전히 매우 유용하며 필수적일 수 있습니다.**
두 개념은 역할이 다르기 때문입니다. 그 이유를 명확하게 정리해 드릴게요.

---

### 1. SQL의 필드명 지정 vs `DictCursor`의 역할 차이

* **SQL의 필드명 지정 (`SELECT id, name ...`)**:
* 데이터베이스에서 "어떤 데이터 컬럼을 가져올 것인가"를 결정합니다. (불필요한 데이터 조회를 막고 성능을 최적화하는 용도)


* **`DictCursor`**:
* 가져온 데이터를 파이썬 코드에서 "어떤 자료구조(타입)로 받을 것인가"를 결정합니다.



즉, SQL에서 컬럼을 아무리 정확하게 지정해도, **기본 커서(`Cursor`)를 쓰면 그 결과는 여전히 순수한 `튜플(Tuple)`로 반환**됩니다.

---

### 2. 코드로 보는 비교 (필드명을 지정했을 때)

SQL에 필드명을 명시했더라도, 커서 종류에 따라 파이썬에서 데이터를 다루는 방식이 완전히 달라집니다.

#### ❌ 기본 커서 (`Cursor`) 사용 시

```python
cursor.execute("SELECT id, name, email FROM users WHERE id = 1;")
row = cursor.fetchone()

print(row)       # 출력: (1, "홍길동", "hong@example.com")
print(row[0])    # id (몇 번째 컬럼인지 숫자로 기억해야 함)
print(row[1])    # name

```

* **문제점**: SQL문에서 나중에 `SELECT id, email, name`처럼 순서를 바꾸거나 중간에 필드를 하나 추가하면, 기존의 `row[1]`, `row[2]` 인덱싱 코드가 전부 망가져서 **심각한 버그**로 이어집니다.

#### `DictCursor` 사용 시 (`cursorclass=DictCursor`)

```python
cursor.execute("SELECT id, name, email FROM users WHERE id = 1;")
row = cursor.fetchone()

print(row)       # 출력: {"id": 1, "name": "홍길동", "email": "hong@example.com"}
print(row["id"])    # 명확하게 키 값으로 접근
print(row["name"])  # 명확하게 키 값으로 접근

```

* **장점**: SQL문에서 컬럼 순서를 바꾸거나 새로운 컬럼을 추가해도, 파이썬 코드에서 키 이름(`"name"`)으로 접근하기 때문에 **코드가 안전하고 유지보수가 훨씬 쉬워집니다.**

---

### 3. 요약

SQL에서 필드명을 구체적으로 지정하는 것은 좋은 습관이지만, **데이터를 파이썬에서 인덱스(`row[0]`)가 아니라 직관적인 키(`row["컬럼명"]`)로 다루고 싶다면 `DictCursor`는 필드명 지정 여부와 상관없이 계속 필요**합니다.
