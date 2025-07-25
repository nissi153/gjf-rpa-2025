import sqlite3
import datetime

# DB 연결 함수
def connect_db():
    conn = sqlite3.connect('./13-dbms/member.db')
    return conn

# 테이블 생성 함수
def create_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS member (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            joindate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        print("테이블이 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"테이블 생성 중 오류 발생: {e}")
    finally:
        conn.close()

# 회원 추가 함수
def insert_member(name, phone, address):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO member (name, phone, address, joindate)
        VALUES (?, ?, ?, ?)
        ''', (name, phone, address, datetime.datetime.now())) # KST ( UTC + 9 )
        conn.commit()
        print(f"{name} 회원이 성공적으로 추가되었습니다.")
    except Exception as e:
        print(f"회원 추가 중 오류 발생: {e}")
    finally:
        conn.close()

# 전체 회원 조회 함수
def select_all_members():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM member")
        members = cursor.fetchall()
        
        if not members:
            print("등록된 회원이 없습니다.")
            return
        
        print("\n--- 전체 회원 목록 ---")
        for member in members:
            print(f"ID: {member[0]}, 이름: {member[1]}, 전화번호: {member[2]}, 주소: {member[3]}, 가입일: {member[4]}")
    except Exception as e:
        print(f"회원 조회 중 오류 발생: {e}")
    finally:
        conn.close()

# 특정 회원 조회 함수
def select_member_by_id(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM member WHERE id = ?", (id,))
        member = cursor.fetchone()
        
        if member:
            print(f"\n--- ID: {id} 회원 정보 ---")
            print(f"이름: {member[1]}")
            print(f"전화번호: {member[2]}")
            print(f"주소: {member[3]}")
            print(f"가입일: {member[4]}")
            return member
        else:
            print(f"ID: {id} 회원을 찾을 수 없습니다.")
            return None
    except Exception as e:
        print(f"회원 조회 중 오류 발생: {e}")
    finally:
        conn.close()

# 회원 정보 수정 함수
def update_member(id, name, phone, address):
    try:
        # 먼저 해당 ID 회원이 존재하는지 확인
        member = select_member_by_id(id)
        if not member:
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE member 
        SET name = ?, phone = ?, address = ?
        WHERE id = ?
        ''', (name, phone, address, id))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"ID: {id} 회원 정보가 성공적으로 수정되었습니다.")
        else:
            print(f"ID: {id} 회원 정보 수정에 실패했습니다.")
    except Exception as e:
        print(f"회원 정보 수정 중 오류 발생: {e}")
    finally:
        conn.close()

# 회원 삭제 함수
def delete_member(id):
    try:
        # 먼저 해당 ID 회원이 존재하는지 확인
        member = select_member_by_id(id)
        if not member:
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM member WHERE id = ?", (id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"ID: {id} 회원이 성공적으로 삭제되었습니다.")
        else:
            print(f"ID: {id} 회원 삭제에 실패했습니다.")
    except Exception as e:
        print(f"회원 삭제 중 오류 발생: {e}")
    finally:
        conn.close()

# 메인 메뉴 함수
def display_menu():
    print("\n=== 회원 관리 시스템 ===")
    print("1. 테이블 생성")
    print("2. 회원 등록")
    print("3. 전체 회원 조회")
    print("4. 특정 회원 조회")
    print("5. 회원 정보 수정")
    print("6. 회원 삭제")
    print("0. 종료")
    return input("메뉴를 선택하세요: ")

# 메인 함수
def main():
    while True:
        choice = display_menu()
        
        if choice == '1':
            create_table()
        
        elif choice == '2':
            name = input("이름을 입력하세요: ")
            phone = input("전화번호를 입력하세요: ")
            address = input("주소를 입력하세요: ")
            insert_member(name, phone, address)
        
        elif choice == '3':
            select_all_members()
        
        elif choice == '4':
            id = input("조회할 회원의 ID를 입력하세요: ")
            select_member_by_id(int(id))
        
        elif choice == '5':
            id = input("수정할 회원의 ID를 입력하세요: ")
            name = input("새 이름을 입력하세요: ")
            phone = input("새 전화번호를 입력하세요: ")
            address = input("새 주소를 입력하세요: ")
            update_member(int(id), name, phone, address)
        
        elif choice == '6':
            id = input("삭제할 회원의 ID를 입력하세요: ")
            delete_member(int(id))
        
        elif choice == '0':
            print("프로그램을 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()