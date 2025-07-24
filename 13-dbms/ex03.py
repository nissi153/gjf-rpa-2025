import sqlite3

db_path = './13-dbms/students.db'

conn = sqlite3.connect(db_path)
print( conn )

cursor = conn.cursor()

# 학생정보 수정
query  = '''
        UPDATE student
        SET name = ?, age = ?, grade = ?
        WHERE name = ?
        '''
cursor.execute( query, ('홍길동2', 45, '5학년', '홍길동') )

conn.commit()  # 수정사항을 실제 DB파일에 적용하기(save)
conn.close()

print( "학생정보 수정 완료" )
