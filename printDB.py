from DB.db import Database  # db.py에서 Database 클래스를 가져옴
import os

def print_database_contents():
    # printDB.py와 같은 디렉토리에 있는 Database.db 파일 경로 설정
    db_path = os.path.join(os.path.dirname(__file__), "Database.db")
    
    if not os.path.exists(db_path):
        print(f"데이터베이스 파일이 존재하지 않습니다: {db_path}")
        return

    # Database 클래스 인스턴스 생성 및 테이블 데이터 출력
    db = Database(db_name=db_path)
    
    print("=== 데이터베이스 내용 출력 ===")
    db.fetch_all_tables()  # 모든 테이블 내용 출력 메서드 호출
    
    # 연결 닫기
    db.close_connection()

if __name__ == "__main__":
    print_database_contents()
