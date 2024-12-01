import sqlite3
from typing import List, Tuple, Optional
import re

# 사용자의 ID, PW, 이름 및 자세 판단을 위해 HPE를 통해 도출된 정보가 저장될 Database
class Database:
    def __init__(self, db_name: str = "Database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.current_user: Optional[Tuple[str, str]] = None  # 로그인된 사용자 정보 저장 (ID, PW)

    def create_tables(self):
        # 사용자의 회원가입 정보(ID, PW, Name)를 저장할 Table을 Database에 생성하는 부분
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Database_data(
            ID TEXT,
            PW TEXT,
            Name TEXT,
            PRIMARY KEY (ID, PW)
        )
        """)

        # 사용자의 회원가입 정보 중 ID, PW를 외래 키로 하여, 자세 판단을 위한 HPE 정보를 저장할 Table을 Database에 생성하는 부분
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

    # 사용자로부터 회원가입 정보(ID, PW, Name)를 입력받고, 해당 정보를 DB에 전송하는 함수
    def sign_up(self, ID: str, PW: str, name: str) -> bool:
        try:
            # ID 입력값 검증(ID는 영문, 숫자가 모두 포함된 1~12자 이내)
            if not re.fullmatch(r"(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]{1,12}", ID):
                raise ValueError("ID는 영문, 숫자가 모두 포함된 1~12자 이내여야 합니다.")
            
            # PW 입력값 검증(PW는 영문, 숫자, 특수문자가 모두 포함된 1~12자 이내)
            if not re.fullmatch(r"(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+=-])[A-Za-z0-9!@#$%^&*()_+=-]{1,12}", PW):
                raise ValueError("PW는 영문, 숫자, 특수문자가 모두 포함된 1~12자 이내여야 합니다.")
            
            # Name 입력값 검증(이름은 한글, 영문, 숫자로 이루어진 1~6자 이내)
            if not re.fullmatch(r"[가-힣A-Za-z0-9]{1,6}", name):
                raise ValueError("이름은 한글, 영문, 숫자로 이루어진 1~6자 이내여야 합니다.")

            print(f"회원가입 시도: ID={ID}, PW={PW}, Name={name}")

            # 중복 확인
            self.cur.execute("SELECT * FROM Database_data WHERE ID=? AND PW=?", (ID, PW))
            if self.cur.fetchone():
                print("이미 존재하는 ID와 PW 조합입니다.")
                return False

            # 데이터베이스 삽입
            self.cur.execute(
                "INSERT INTO Database_data (ID, PW, Name) VALUES (?, ?, ?)",
                (ID, PW, name)
            )
            self.conn.commit()
            print("회원가입 성공!")
            return True

        except ValueError as e:
            # 입력값 검증 실패 시
            print(f"회원가입 실패 (입력값 검증 실패): {e}")
            return False
        except sqlite3.IntegrityError as e:
            # 데이터베이스 제약 조건 위반 시
            print(f"회원가입 실패 (데이터베이스 오류): {e}")
            return False
        except Exception as e:
            # 그 외 예상치 못한 오류
            print(f"회원가입 실패 (알 수 없는 오류): {e}")
            return False

    # 사용자로부터 ID, PW를 입력받아 로그인하는 함수
    def log_in(self, ID: str, PW: str) -> bool:
        
        # Database에서 입력받은 ID, PW와 일치하는 정보를 가져온다.
        self.cur.execute(
            "SELECT * FROM Database_data WHERE ID=? AND PW=?",
            (ID, PW)
        )
        user = self.cur.fetchone()

        # ID, PW와 일치하는 정보가 있다면 True
        if user:
            self.current_user = (ID, PW)
            return True
        
        # 아니면 False가 된다.
        else:
            self.current_user = None
            return False

    # HPE를 통해 사용자의 자세 판단을 위한 정보를 입력으로 받아, Database에 저장하는 함수
    def insert_hpe_data(self, 
                        angle_shoulder: float, 
                        center_shoulder_dist: float, 
                        center_mouth_dist: float) -> bool:
        """
        HPE를 통해 얻어진 정보 중, left_hand_distance와 right_hand_distance를 제외한 자세 판단을 위한 정보를
        Database에 저장하는 함수
        """
        # 로그인 여부 판별
        if not self.current_user:
            print("HPE 데이터를 삽입하려면 먼저 로그인해야 합니다.")
            return False

        ID, PW = self.current_user

        # 해당 정보 Database에 저장
        try:
            self.cur.execute(
                """INSERT INTO HPE (ID, PW, angle_shoulder, center_shoulder_dist, center_mouth_dist) 
                VALUES (?, ?, ?, ?, ?)""",
                (ID, PW, angle_shoulder, center_shoulder_dist, center_mouth_dist)
            )
            self.conn.commit()
            print(f"HPE 데이터 삽입 성공: ID={ID}")
            return True
        
        # 실패 시 오류 메시지 출력
        except sqlite3.Error as e:
            print(f"HPE 데이터 삽입 중 오류 발생: {e}")
            return False

    # HPE를 통해 사용자의 자세 판단을 위한 정보를 입력으로 받아, Database에 저장하는 함수 (2)
    def insert_hpe_hands_data(self, 
                              left_hand_distance: float, 
                              right_hand_distance: float) -> bool:
        """
        HPE를 통해 얻어진 정보 중, left_hand_distance와 right_hand_distance를 Database에 저장하는 함수
        """

        # 로그인 여부 확인
        if not self.current_user:
            print("HPE 데이터를 삽입하려면 먼저 로그인해야 합니다.")
            return False

        ID, PW = self.current_user

        # 해당 정보 Database에 저장
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
            
            # 손 정보 등록 이전에 자세 등록이 완료되지 않은 경우
            else:
                print("HPE 데이터가 존재하지 않습니다. 먼저 다른 데이터를 삽입하세요.")
                return False
            
        # 실패 시 오류 메시지 출력
        except sqlite3.Error as e:
            print(f"손 데이터 삽입 중 오류 발생: {e}")
            return False

    # 현재 로그인된 사용자의 이름을 반환하는 함수
    def get_name(self) -> Optional[str]:

        # 로그인 되지 않은 채 이루어진 함수 호출 처리
        if not self.current_user:
            print("사용자의 이름을 가져오려면 먼저 로그인해야 합니다.")
            return None

        # 로그인이 되었다면 현재 로그인된 ID, PW를 바탕으로 Name 정보 가져오기
        ID, PW = self.current_user
        self.cur.execute(
            "SELECT Name FROM Database_data WHERE ID=? AND PW=?",
            (ID, PW)
        )
        result = self.cur.fetchone()
        if result:
            return result[0]
        
        # 실패시 오류 메시지 출력
        else:
            print("사용자 이름을 찾을 수 없습니다.")
            return None

    # Database에 저장된 사용자의 모든 HPE 기반 자세 판단에 사용되는 정보를 불러오는 함수
    def fetch_hpe_data(self) -> Optional[List[Tuple]]:
        # 로그인되지 않은채 이루어진 함수 호출 처리
        if not self.current_user:
            print("HPE 데이터를 조회하려면 먼저 로그인해야 합니다.")
            return None

        # 현재 ID, PW를 바탕으로 Database에 저장된 HPE 기반 자세 판단 사용 정보(자세 등록 정보)를 출력
        ID, PW = self.current_user
        self.cur.execute(
            """SELECT angle_shoulder, center_shoulder_dist, center_mouth_dist, left_hand_distance, right_hand_distance 
            FROM HPE WHERE ID=? AND PW=?""",
            (ID, PW)
        )
        return self.cur.fetchall()

    # Database에 있는 사용자의 모든 정보(회원가입 정보, 자세 등록 정보)를 출력하는 함수
    def fetch_all_tables(self) -> None:
        # 회원가입 정보가 있는 Database_data Table data를 출력
        print("\n=== Database_data 테이블 데이터 ===")
        self.cur.execute("SELECT * FROM Database_data")
        database_data = self.cur.fetchall()
        for record in database_data:
            print(record)

        # 자세 등록 정보가 있는 HPE Table data를 출력
        print("\n=== HPE 테이블 데이터 ===")
        self.cur.execute("SELECT * FROM HPE")
        hpe_data = self.cur.fetchall()
        for record in hpe_data:
            print(record)

    # Database에 저장된 자세 등록 정보를 삭제하는 함수
    def delete_hpe_data(self) -> bool:
        # 로그인 이전에 이루어진 함수 호출에 대한 처리
        if not self.current_user:
            print("HPE 데이터를 삭제하려면 먼저 로그인해야 합니다.")
            return False

        # 현재 로그인된 ID, PW 정보를 바탕으로, Database 내의 해당 ID, PW의 자세 등록 정보를 삭제한다.
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
            
            # 존재하지 않을 시 오류 처리
            else:
                print("HPE 데이터가 존재하지 않습니다.")
                return False
        # 오류 처리
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
