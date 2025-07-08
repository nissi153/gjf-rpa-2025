# ex2-6.py

# 형변환 type casting - 데이터형이 변경되는 것
# 암시적 형변환
x = 3
y = 4.12
z = x + y # 다른 두개의 타입이 연산되면, 더 큰 타입으로 변경된다.
print( type(x) ) # int
print( type(y) ) # float
print( type(z) ) # float 

# 명시적 형변환
myInt = int("123")
myFloat = float( 123 )
myBool = bool( 0 )
print( myInt )
print( myFloat )
print( myBool )

try:
    myInt2 = int("123abc한글")
except:
    print("타입 변경 오류! 아리비아 숫자가 아닙니다.")

print( str(123) )
print( str(3.14) )
print( str([1,2,3]) )

# 파이썬에서 False로 간주하는 값
# 숫자 0 (정수,실수)
# 빈 문자열 ""
# 빈 리스트 []
# 빈 튜플 ()
# 빈 딕셔너리 {}
# 빈 세트 set()
# None

# 위의 값 외에는 모두 True로 간주됩니다.
print( bool(0) )
print( bool(1) )
print( bool(0.0) )
print( bool("Hello") )
print( bool("") )
print( bool([]) )
print( bool([1,2]) )
print( bool(()) )
print( bool(None) )



