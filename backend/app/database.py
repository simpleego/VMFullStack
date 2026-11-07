# =============================================================================
# database.py : MariaDB(DB)에 "접속"하는 일만 담당하는 파일
#
# DB 접속 정보(주소, 계정, 비밀번호)는 코드에 직접 쓰지 않고 .env 파일에 둔다.
#   - 이유 1) 비밀번호가 코드(Git)에 올라가면 유출 위험이 있다.
#   - 이유 2) 컴퓨터마다 DB 설정이 달라도 코드는 수정하지 않아도 된다.
# =============================================================================

# 파이썬 표준 라이브러리: 환경변수를 읽는 도구
import os

# pymysql : 파이썬에서 MariaDB/MySQL 에 접속하는 드라이버 (ORM 이 아니다. SQL 을 직접 보낸다)
import pymysql
# dotenv : .env 파일의 내용을 환경변수로 읽어 들이는 도구
from dotenv import load_dotenv
# DictCursor : 조회 결과를 {"컬럼명": 값} 딕셔너리로 받게 해 준다 (JSON 으로 바꾸기 쉽다)
from pymysql.cursors import DictCursor

# backend/.env 파일의 내용을 읽어서 환경변수로 등록한다.
# 이 파일(database.py)에서 위쪽 폴더로 올라가며 .env 를 찾기 때문에
# 서버를 어느 폴더에서 실행해도 backend/.env 를 찾을 수 있다.
load_dotenv()


def get_connection():
    """DB 연결(전화 연결 같은 것)을 새로 만들어서 돌려준다.

    사용하는 쪽에서 다 쓴 뒤에는 반드시 conn.close() 로 연결을 끊어야 한다.
    (연결을 끊지 않으면 DB 가 감당할 수 있는 연결 수를 다 써 버려 서버가 멈출 수 있다)
    """
    return pymysql.connect(
        # os.getenv("이름", "기본값") : 환경변수 값을 읽는다. 없으면 기본값을 쓴다.
        host=os.getenv("DB_HOST", "localhost"),        # DB 가 있는 컴퓨터 주소
        port=int(os.getenv("DB_PORT", "3306")),        # DB 포트 (MariaDB 기본값 3306), 환경변수는 문자열이라 int 로 변환
        user=os.getenv("DB_USER"),                     # DB 계정 (vmshop_user)
        password=os.getenv("DB_PASSWORD"),             # DB 비밀번호
        database=os.getenv("DB_NAME"),                 # 사용할 DB 이름 (vmShop)
        charset="utf8mb4",                             # 한글, 이모지가 깨지지 않게 하는 문자 인코딩
        cursorclass=DictCursor,                        # 결과를 딕셔너리로 받는다
    )
