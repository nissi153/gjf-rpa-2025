import sqlite3

db_path = './13-dbms/students.db'

conn = sqlite3.connect(db_path)
print( conn )

cursor = conn.cursor()

# 학생정보 삭제
query = '''
        DELETE FROM student
        WHERE name = ?        
        '''
cursor.execute( query, ('강감찬',) )

conn.commit()
conn.close()

print('학생정보 삭제 성공')

