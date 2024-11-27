import sqlite3
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = "Database.db"):
        """
        Database 클래스 초기화 및 연결.
        :param db_name: 데이터베이스 파일 이름
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.current_user: Optional[Tuple[str, str]] = None  # 로그인된 사용자 정보 저장 (ID, PW)

    def create_tables(self):
        """
        테이블 생성: Database_data 및 HPE 테이블
        """
        # Database_data 테이블 생성
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Database_data(
            ID TEXT,
            PW TEXT,
            Name TEXT,
            PRIMARY KEY (ID, PW)
        )
        """)

        # HPE 테이블 생성
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

    def sign_up(self, ID: str, PW: str, name: str) -> bool:
        """
        회원가입 메소드 - Database_data 테이블에 ID, PW, 이름 추가.
        :param ID: 사용자 ID
        :param PW: 사용자 PW
        :param name: 사용자 이름
        :return: 성공 여부
        """
        try:
            self.cur.execute(
                "INSERT INTO Database_data (ID, PW, Name) VALUES (?, ?, ?)",
                (ID, PW, name)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # print("이미 존재하는 ID와 PW 조합입니다.")
            return False

    def log_in(self, ID: str, PW: str) -> bool:
        """
        로그인 메소드 - Database_data 테이블의 ID와 PW 비교.
        로그인 성공 시 current_user에 정보 저장.
        :param ID: 사용자 ID
        :param PW: 사용자 PW
        :return: 로그인 성공 여부
        """
        self.cur.execute(
            "SELECT * FROM Database_data WHERE ID=? AND PW=?",
            (ID, PW)
        )
        user = self.cur.fetchone()
        if user:
            self.current_user = (ID, PW)  # 로그인 성공 시 현재 사용자 정보 저장
            return True # print(f"로그인 성공: ID={ID}")
        else:
            self.current_user = None
            return False # print("로그인 실패: 잘못된 ID 또는 PW입니다.")

    def insert_hpe_data(self, 
                        angle_shoulder: float, 
                        center_shoulder_dist: float, 
                        center_mouth_dist: float, 
                        left_hand_distance: float, 
                        right_hand_distance: float) -> bool:
        """
        로그인된 사용자의 HPE 데이터를 삽입.
        :param angle_shoulder: 어깨 각도
        :param center_shoulder_dist: 중앙 어깨 거리
        :param center_mouth_dist: 중앙 입 거리
        :param left_hand_distance: 왼손 거리
        :param right_hand_distance: 오른손 거리
        :return: 삽입 성공 여부
        """
        if not self.current_user:
            print("HPE 데이터를 삽입하려면 먼저 로그인해야 합니다.")
            return False

        ID, PW = self.current_user
        try:
            self.cur.execute(
                """INSERT INTO HPE (ID, PW, angle_shoulder, center_shoulder_dist, center_mouth_dist, left_hand_distance, right_hand_distance) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (ID, PW, angle_shoulder, center_shoulder_dist, center_mouth_dist, left_hand_distance, right_hand_distance)
            )
            self.conn.commit()
            print(f"HPE 데이터 삽입 성공: ID={ID}")
            return True
        except sqlite3.Error as e:
            print(f"HPE 데이터 삽입 중 오류 발생: {e}")
            return False

    def fetch_hpe_data(self) -> Optional[List[Tuple]]:
        """
        로그인된 사용자의 HPE 데이터를 조회.
        :return: HPE 테이블의 데이터 리스트 또는 None
        """
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
        """
        Database_data와 HPE 테이블의 모든 데이터를 출력.
        """
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
        """
        로그인된 사용자의 HPE 데이터를 삭제.
        :return: 삭제 성공 여부
        """
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
        """
        데이터베이스 연결 닫기.
        """
        self.conn.close()
