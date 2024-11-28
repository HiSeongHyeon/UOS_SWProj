import sqlite3
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = "Database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.current_user: Optional[Tuple[str, str]] = None  # 로그인된 사용자 정보 저장 (ID, PW)

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Database_data(
            ID TEXT,
            PW TEXT,
            Name TEXT,
            PRIMARY KEY (ID, PW)
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS HPE(
            ID TEXT,
            PW TEXT,
            angle_shoulder REAL,
            center_shoulder_dist REAL,
            center_mouth_dist REAL,
            left_hand_distance REAL,
            right_hand_distance REAL,
            FOREIGN KEY (ID, PW) REFERENCES Database_data(ID, PW)
        )
        """)
        self.conn.commit()

    # 
import re

def sign_up(self, ID: str, PW: str, name: str) -> bool:
    """
    회원가입 메소드 - Database_data 테이블에 ID, PW, 이름 추가.
    입력 조건을 만족하지 않으면 False를 반환.
    :param ID: 사용자 ID (영문, 숫자 조합, 1~12자)
    :param PW: 사용자 PW (영문, 숫자, 특수문자 조합, 1~12자)
    :param name: 사용자 이름 (한글, 영문, 숫자 조합, 1~6자)
    :return: 성공 여부
    """
    try:
        # 조건 검증
        if not re.fullmatch(r"[A-Za-z0-9]{1,12}", ID):
            raise ValueError("ID는 영문, 숫자의 조합으로 1~12자 이내여야 합니다.")
        
        if not re.fullmatch(r"[A-Za-z0-9!@#$%^&*()_+=-]{1,12}", PW):
            raise ValueError("PW는 영문, 숫자, 특수문자의 조합으로 1~12자 이내여야 합니다.")
        
        if not re.fullmatch(r"[가-힣A-Za-z0-9]{1,6}", name):
            raise ValueError("이름은 한글, 영문, 숫자의 조합으로 1~6자 이내여야 합니다.")

        # 조건을 만족하면 데이터베이스에 삽입
        self.cur.execute(
            "INSERT INTO Database_data (ID, PW, Name) VALUES (?, ?, ?)",
            (ID, PW, name)
        )
        self.conn.commit()
        return True

    except (sqlite3.IntegrityError, ValueError) as e:
        return False


    def log_in(self, ID: str, PW: str) -> bool:
        self.cur.execute(
            "SELECT * FROM Database_data WHERE ID=? AND PW=?",
            (ID, PW)
        )
        user = self.cur.fetchone()
        if user:
            self.current_user = (ID, PW)
            return True
        else:
            self.current_user = None
            return False

    def insert_hpe_data(self, 
                        angle_shoulder: float, 
                        center_shoulder_dist: float, 
                        center_mouth_dist: float) -> bool:
        """
        left_hand_distance와 right_hand_distance를 제외한 데이터를 삽입
        """
        if not self.current_user:
            print("HPE 데이터를 삽입하려면 먼저 로그인해야 합니다.")
            return False

        ID, PW = self.current_user
        try:
            self.cur.execute(
                """INSERT INTO HPE (ID, PW, angle_shoulder, center_shoulder_dist, center_mouth_dist) 
                VALUES (?, ?, ?, ?, ?)""",
                (ID, PW, angle_shoulder, center_shoulder_dist, center_mouth_dist)
            )
            self.conn.commit()
            print(f"HPE 데이터 삽입 성공: ID={ID}")
            return True
        except sqlite3.Error as e:
            print(f"HPE 데이터 삽입 중 오류 발생: {e}")
            return False

    def insert_hpe_hands_data(self, 
                              left_hand_distance: float, 
                              right_hand_distance: float) -> bool:
        """
        left_hand_distance와 right_hand_distance 데이터를 삽입
        """
        if not self.current_user:
            print("HPE 데이터를 삽입하려면 먼저 로그인해야 합니다.")
            return False

        ID, PW = self.current_user
        try:
            self.cur.execute(
                """UPDATE HPE 
                SET left_hand_distance=?, right_hand_distance=? 
                WHERE ID=? AND PW=?""",
                (left_hand_distance, right_hand_distance, ID, PW)
            )
            self.conn.commit()
            if self.cur.rowcount > 0:
                print(f"손 데이터 삽입 성공: ID={ID}")
                return True
            else:
                print("HPE 데이터가 존재하지 않습니다. 먼저 다른 데이터를 삽입하세요.")
                return False
        except sqlite3.Error as e:
            print(f"손 데이터 삽입 중 오류 발생: {e}")
            return False

    def get_name(self) -> Optional[str]:
        """
        현재 로그인된 사용자의 이름을 반환
        """
        if not self.current_user:
            print("사용자의 이름을 가져오려면 먼저 로그인해야 합니다.")
            return None

        ID, PW = self.current_user
        self.cur.execute(
            "SELECT Name FROM Database_data WHERE ID=? AND PW=?",
            (ID, PW)
        )
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            print("사용자 이름을 찾을 수 없습니다.")
            return None

    def fetch_hpe_data(self) -> Optional[List[Tuple]]:
        if not self.current_user:
            print("HPE 데이터를 조회하려면 먼저 로그인해야 합니다.")
            return None

        ID, PW = self.current_user
        self.cur.execute(
            """SELECT angle_shoulder, center_shoulder_dist, center_mouth_dist, left_hand_distance, right_hand_distance 
            FROM HPE WHERE ID=? AND PW=?""",
            (ID, PW)
        )
        return self.cur.fetchall()

    def fetch_all_tables(self) -> None:
        print("\n=== Database_data 테이블 데이터 ===")
        self.cur.execute("SELECT * FROM Database_data")
        database_data = self.cur.fetchall()
        for record in database_data:
            print(record)

        print("\n=== HPE 테이블 데이터 ===")
        self.cur.execute("SELECT * FROM HPE")
        hpe_data = self.cur.fetchall()
        for record in hpe_data:
            print(record)

    def delete_hpe_data(self) -> bool:
        if not self.current_user:
            print("HPE 데이터를 삭제하려면 먼저 로그인해야 합니다.")
            return False

        ID, PW = self.current_user
        try:
            self.cur.execute(
                "DELETE FROM HPE WHERE ID=? AND PW=?",
                (ID, PW)
            )
            self.conn.commit()
            if self.cur.rowcount > 0:
                print(f"HPE 데이터 삭제 성공: ID={ID}")
                return True
            else:
                print("HPE 데이터가 존재하지 않습니다.")
                return False
        except sqlite3.Error as e:
            print(f"HPE 데이터 삭제 중 오류 발생: {e}")
            return False

    def close_connection(self):
        self.conn.close()

"""
db.fetch_hpe_data를 통해 특정 값 (center_shoulder_dist) 가져오기

hpe_data = db.fetch_hpe_data()

if hpe_data and len(hpe_data) > 0:  # 데이터가 존재하는지 확인
    first_row = hpe_data[0]  # 첫 번째 행 가져오기
    center_shoulder_dist = first_row[1]  # center_shoulder_dist 값 (인덱스 1)
    print(f"첫 번째 행의 center_shoulder_dist: {center_shoulder_dist}")
else:
    print("HPE 데이터가 없습니다.")

"""
