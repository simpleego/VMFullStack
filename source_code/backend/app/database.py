from dotenv import load_dotenv
import os
import pymysql
from pymysql.cursors import DictCursor


# .env 파일에 설정된 환경변수를 메모리에 로드
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
