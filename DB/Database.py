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

    # 2가지 Table 생성 (1) Database_data (2) HPE
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
            Key_Point INTEGER,
            x REAL,
            y REAL,
            z REAL,
            r REAL,
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
        except sqlite3.IntegrityError:  # 중복된 ID, PW일 경우 처리
            print("이미 존재하는 ID와 PW 조합입니다.")
            return False


    def log_in(self, ID: str, PW: str) -> bool:
        """
        로그인 메소드 - Database_data 테이블의 ID와 PW 비교.
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
            return True
        else:
            return False

    def insert_hpe_data(self, ID: str, PW: str, key_point: int, x: float, y: float, z: float, r: float) -> bool:
        """
        HPE 테이블에 데이터 삽입.
        :param ID: 사용자 ID
        :param PW: 사용자 PW
        :param key_point: Key Point 값
        :param x: x 좌표
        :param y: y 좌표
        :param z: z 좌표
        :param r: r 값
        :return: 삽입 성공 여부
        """
        # ID와 PW로 사용자가 존재하는지 확인
        self.cur.execute(
            "SELECT * FROM Database_data WHERE ID=? AND PW=?",
            (ID, PW)
        )
        if not self.cur.fetchone():
            print("HPE 데이터를 삽입할 수 없습니다. 잘못된 ID 또는 PW입니다.")
            return False

        # 데이터 삽입
        self.cur.execute(
            "INSERT INTO HPE (ID, PW, Key_Point, x, y, z, r) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ID, PW, key_point, x, y, z, r)
        )
        self.conn.commit()
        print(f"HPE 데이터 삽입 성공: {ID}, {PW}, {key_point}, {x}, {y}, {z}, {r}")
        return True

    def fetch_hpe_data(self, ID: str, PW: str) -> List[Tuple]:
        """
        특정 사용자의 HPE 데이터를 조회.
        :param ID: 사용자 ID
        :param PW: 사용자 PW
        :return: HPE 테이블의 데이터 리스트
        """
        self.cur.execute(
            "SELECT Key_Point, x, y, z, r FROM HPE WHERE ID=? AND PW=?",
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

    def delete_database_data(self, ID: str, PW: str) -> bool:
        """
        Database_data 테이블에서 특정 사용자의 데이터를 삭제.
        :param ID: 사용자 ID
        :param PW: 사용자 PW
        :return: 삭제 성공 여부
        """
        try:
            self.cur.execute(
                "DELETE FROM Database_data WHERE ID=? AND PW=?",
                (ID, PW)
            )
            self.conn.commit()
            if self.cur.rowcount > 0:
                print(f"Database_data에서 ID: {ID}, PW: {PW} 데이터 삭제 성공.")
                return True
            else:
                print(f"Database_data에서 ID: {ID}, PW: {PW} 데이터 없음.")
                return False
        except sqlite3.Error as e:
            print(f"Database_data 데이터 삭제 중 오류 발생: {e}")
            return False

    def delete_hpe_data(self, ID: str, PW: str) -> bool:
        """
        HPE 테이블에서 특정 사용자의 데이터를 삭제.
        :param ID: 사용자 ID
        :param PW: 사용자 PW
        :return: 삭제 성공 여부
        """
        try:
            self.cur.execute(
                "DELETE FROM HPE WHERE ID=? AND PW=?",
                (ID, PW)
            )
            self.conn.commit()
            if self.cur.rowcount > 0:
                print(f"HPE에서 ID: {ID}, PW: {PW} 데이터 삭제 성공.")
                return True
            else:
                print(f"HPE에서 ID: {ID}, PW: {PW} 데이터 없음.")
                return False
        except sqlite3.Error as e:
            print(f"HPE 데이터 삭제 중 오류 발생: {e}")
            return False

    def close_connection(self):
        """
        데이터베이스 연결 닫기.
        """
        self.conn.close()
