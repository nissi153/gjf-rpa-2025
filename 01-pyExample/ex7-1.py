# ex7-1.py
# 클래스 Class
# 객체지향(사물,물건 지향) 프로그래밍 : 아날로드의 모든 세계를 클래스로 코드화 시키는 것
# 클래스는 변수 + 함수로 구성되어 있음.
#          속성   행동
# 클래스를 메모리에 올리면(생성) 클래스 객체(Object, Instance)가 된다.
# (Code)                                (in Memory, 실행가능 상태)

class Dog:
    age = 10 #속성
    def eat():  #행동
        print( "사료를 먹는다." )

class Cat:
    age = 5 #속성
    def craw(): #행동
        print("햘킨다")