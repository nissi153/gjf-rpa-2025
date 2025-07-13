# ex5-2.py
# 종합 연습문제 1
# 숫자 맞추기 게임
'''
문제설명
컴퓨터가 1부터 20 사이의 정수 중 하나를 무작위로 선택합니다.
사용자는 숫자를 추측하면서 컴퓨터가 선택한 숫자를 맞춰야 합니다.

<입출력 예시>
1~20 숫자 입력: 10
너무 작아요.
1~20 숫자 입력: 15
너무 커요.
1~20 숫자 입력: 13
정답입니다! 3번 만에 맞췄습니다.
'''
# import random
# number = random.randint(1, 21)
# print( number )
# count = 1
# while True:
#     input_num = int( input('1~20 숫자 입력: ') )
#     if number == input_num:
#         print(f'정답입니다! {count}번째 성공!')
#         break
#     elif number < input_num:
#         print('너무 커요.')
#         count += 1
#         continue
#     else:
#         print('너무 작아요.')
#         count += 1
#         continue

# 종합 연습문제 2
# 도서 대여 시스템
문제설명2 = '''
사용자가 책을 선택해 대여하거나 반납할 수 있는 프로그램을 작성합니다.
예시 입력/출력
== 도서 관리 시스템 ==
1. 대여  2. 반납  3. 목록 조회  4. 종료
번호 입력: 1
대여할 책 제목: 파이썬기초
>> 대여 완료!

1. 대여  2. 반납  3. 목록 조회  4. 종료
번호 입력: 1
대여할 책 제목: 파이썬기초
>> 이미 대여 중입니다.

1. 대여  2. 반납  3. 목록 조회  4. 종료
번호 입력: 2
대여할 책 제목: 파이썬기초
>> 반납 완료!

1. 대여  2. 반납  3. 목록 조회  4. 종료
번호 입력: 3
== 현재 도서 목록 ==
[대여 가능] HTML기초  
[대여 가능] JS기초  
[대여 중]   파이썬기초  
[대여 중]   CSS기초  
'''

# 도서 대여 시스템 구현
class LibrarySystem:
    def __init__(self):
        my_library = {
            "대여" : ["HTML기초", "JS기초"],
            "반납" : ["파이썬기초", "CSS기초"]
        }
        # my_library 딕셔너리를 사용하여 초기 데이터 설정
        self.available_books = my_library["대여"].copy()  # 대여 가능한 책들
        self.rented_books = my_library["반납"].copy()     # 대여 중인 책들
    
    def display_menu(self):
        """메뉴를 출력하는 함수"""
        print("\n== 도서 관리 시스템 ==")
        print("1. 대여  2. 반납  3. 목록 조회  4. 종료")
    
    def rent_book(self):
        """도서를 대여하는 함수"""
        book_title = input("대여할 책 제목: ").strip()
        
        if book_title in self.rented_books:
            print(">> 이미 대여 중입니다.")
        elif book_title in self.available_books:
            self.available_books.remove(book_title)
            self.rented_books.append(book_title)
            print(">> 대여 완료!")
        else:
            print(">> 해당 도서가 존재하지 않습니다.")
    
    def return_book(self):
        """도서를 반납하는 함수"""
        book_title = input("반납할 책 제목: ").strip()
        
        if book_title in self.rented_books:
            self.rented_books.remove(book_title)
            self.available_books.append(book_title)
            print(">> 반납 완료!")
        elif book_title in self.available_books:
            print(">> 이미 반납된 도서입니다.")
        else:
            print(">> 해당 도서가 존재하지 않습니다.")
    
    def display_books(self):
        """도서 목록을 출력하는 함수"""
        print("\n== 현재 도서 목록 ==")
        
        # 대여 가능한 책들 출력
        for book in self.available_books:
            print(f"[대여 가능] {book}")
        
        # 대여 중인 책들 출력
        for book in self.rented_books:
            print(f"[대여 중]   {book}")
    
    def run(self):
        """메인 실행 함수"""
        while True:
            self.display_menu()
            
            try:
                choice = int(input("번호 입력: "))
                
                if choice == 1:
                    self.rent_book()
                elif choice == 2:
                    self.return_book()
                elif choice == 3:
                    self.display_books()
                elif choice == 4:
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("1-4 사이의 번호를 입력해주세요.")
                    
            except ValueError:
                print("숫자만 입력해주세요.")
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                break

def main():
    """메인 함수"""
    library = LibrarySystem()
    library.run()

if __name__ == "__main__":
    main()
