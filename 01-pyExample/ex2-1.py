# 코멘트(주석) 
#   : 단축키 CTRL + /
#   : 설명글이며 실행이 안됨.
print("hello python") # 쌍따옴표로 묶은 것은 문자열 데이터이다.
print('hello python') # 단따옴표로

# print() 함수 : 콘솔(표준출력창)에 텍스트를 출력한다.

# 정수형(소숫점없음)
a = 123  # 대입연산자 =은 오른쪽의 값을 왼쪽에 덮어쓰기한다.
print(a)
c = -123
print(c)

# 실수형(소숫점있음)
b = 3.14
print(b)
# 지수형 표현
d = 4.24E10  # 10의 10승
print(d)

# 10진수 0~9 10
# 8진수 0~7 10
e = 0o10
print(e)

# 16진수 0~9 a b c d e f 10
f = 0x10
print(f)

# 사칙연산
a = 3 # a변수 재사용, 초기화
b = 4 # b변수 재사용, 초기화
print( a + b ) # 덧셈 
print( a - b ) # 뺄셈
print( a * b ) # 곱셈
print( a / b ) # 나눗셈의 실수 몫 0.75

print( a // b ) # 나눗셈의 정수 몫(소숫점은 버림)  0.75 -> 0
print( a % b ) # 나눗셈의 나머지 3

