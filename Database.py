import sqlite3

# [] 여기서 최초 DB 생성
# connect() 메소드에 입력한 DB가 이미 존재한다면 그대로 사용할 것이고, 존재하지 않는다면 새롭게 friend.db라는 DB를 생성할 것이다.
conn = sqlite3.connect('friend.db')

# [GUI] GUI에서 사용자 정보 최초 회원가입시 DB에 등록
friend_data = list(tuple())
friend_data.append(('김상욱', 22, '010-4545-6767', '서울특별시 종로구 세종대로 종로 1가'))
friend_data.append(('최지훈', 20, '010-7896-1234', '​전라북도 전주시 덕진구 석소로 77, 101동 101호(인후동1가, 대우아파트)'))
friend_data.append(('Dr.Bae', 67, '010-8452-5678', '​전라북도 전주시 덕진구 석소2길 21-1(우아동2가)'))
friend_data.append(('강서혁', 27, '010-1414-6767', '경상남도 의령군 화정면 화정로 41-6'))
friend_data.append(('유민규', 21, '010-6497-6497', '서울특별시 동작구 흑석한강로 2(흑석동)'))

# db 쿼리를 조작하기 위한 커서 객체 생성
cur = conn.cursor()

# 테이블 생성
cur.execute("""CREATE TABLE IF NOT EXISTS friend_data(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  age INTEGER,
  number TEXT,
  address TEXT
  )""")

# executemany() 메소드를 사용하면 여러개의 데이터를 배열로 전달하여 한 번에 삽입할 수 있다.
cur.executemany('INSERT INTO friend_data (name, age, number, address) VALUES (?, ?, ?, ?)', friend_data)
# 마지막으로 쿼리를 삽입(INSERT) / 삭제(DELETE) / 수정(UPDATE) 할 때는 commit() 메소드를 호출하여 변경사항을 인지시켜주어야 한다.
conn.commit()

# 마지막엔 무조건 close() 메소드로 db연결을 해제해야 한다.
conn.close()

"""
#데이터 조회

데이터를 삽입했으니, 정상적으로 데이터가 들어갔는지 확인해볼 필요가 있다.

이번에는 SELECT 쿼리문을 사용하여 friend_data 테이블에 있는 데이터를 모두 가져와보도록 하겠다.

fetchall() 메소드를 사용하면 execute() 메소드로 탐색한 데이터를 배열로 가져올 수 있다.

그리고 for문을 통해 결과를 출력해보자.

conn = sqlite3.connect("friend.db")

cur = conn.cursor()
cur.execute("SELECT * FROM friend_data")

friends = cur.fetchall()

for friend in friends:
  print(friend)

conn.close()
"""

"""
#데이터 수정

위에서 '최지훈'이라는 친구의 번호를 잘못 저장했다고 언급했다.

그렇다면 번호를 어떻게 수정할 수 있을까?  바로 UPDATE문이다.

UPDATE문의 SET에는 변경할 컬럼과 값을 입력해주고, WHERE절에는 수정할 데이터의 name이 최지훈이라는 사실을 알려준다.

그리고 다시 SELECT문을 통해 최지훈의 데이터를 출력해보자.

conn = sqlite3.connect("friend.db")

cur = conn.cursor()
cur.execute("UPDATE friend_data SET number=? WHERE name=?", ('010-1234-5678', '최지훈'))

cur.execute("SELECT * FROM friend_data WHERE name=?", ('최지훈', ))
friend = cur.fetchone()

print(friend)

conn.commit()
conn.close()
"""

"""
#데이터 삭제
BuNa는 또다시 고민하기 시작했다.

바로 대학교 교수님인 Dr.Bae와 손절하여 더 이상 필요 없는 데이터를 지우고 싶었기 때문이다.

이런 경우에는 DELETE 문을 통해 지우고 싶은 데이터의 컬럼명과 구분할 수 있는 값을 전달해주어 삭제하면 된다.

위 코드를 보면 알 수 있다시피 이름이 'Dr.Bae'인 데이터를 찾아서 삭제해달라고 요청하고 있다.

데이터가 정상적으로 제거되었는지 SELECT문을 통해 모든 데이터를 불러오고 출력해보자.

conn = sqlite3.connect("friend.db")

cur = conn.cursor()
cur.execute("DELETE FROM friend_data WHERE name=?", ('Dr.Bae', ))

cur.execute("SELECT * FROM friend_data")
friends = cur.fetchall()

for friend in friends:
  print(friend)

conn.commit()
conn.close()
"""

"""
import pandas as pd

conn = sqlite3.connect('friend.db')
cur = conn.cursor()

cur.execute("SELECT * FROM friend_data")

rows = cur.fetchall()

# 테이블 컬럼명 가져오기
columns = [column[0] for column in cur.description]

frame = pd.DataFrame.from_records(data=rows, columns=columns)

conn.close()

frame
"""