# ex7-2.py

# 계산기 기능 구현 - 함수

# global 영역
result1 = 0 

def add(num):  #함수 안에서 선언(생성)된 변수는 바깥쪽(global)에서 볼수 없음.    
    # add 함수영역
    global result1
    result1 += num
    return result1  # 함수안에서 선언된 변수는 함수종료시 함께 종료됨.

print( add( 10 ) ) # 10
print( add( 10 ) ) # 20

def sub( num ):
    global result1
    result1 -= num
    return result1

print( sub(10) )
print( sub(10) )

# 계산기 기능 구현 - 클래스
class Calc:
    result = 0
    def add(self, num):
        self.result += num
    def sub(self, num):
        self.result -= num

calc = Calc()
calc.add( 10 )
print( calc.result )
calc.add( 10 )
print( calc.result )
calc.sub( 10 )
print( calc.result )
calc.sub( 10 )
print( calc.result )