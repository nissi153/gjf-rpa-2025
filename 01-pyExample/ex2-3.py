# 연습문제

#1.문자열 출력하기
# 문자열 "Python is easy!"를 출력하세요.
print( "Python is easy!" )

# 2. 문자열 인덱싱
# 문자열 s = "Hello Python"에서 첫 번째 문자와 마지막 문자를 출력해보세요.
s = "Hello Python"
print( s[0] )
print( s[-1] )
print( s[0] + " " + s[-1] )

# 3. 문자열 슬라이싱
# 문자열 s = "Life is short, use Python"에서 "use Python"만 출력해보세요.
s = "Life is short, use Python"
print( s[15:] )

# 4. 문자열 합치기
# 변수 a = "Python"과 b = " is fun"을 이용해서 "Python is fun"을 출력하세요.
a = "Python"
b = " is fun"
print( a + b )

# 5. 문자열 곱하기
# 문자열 "Hi!"를 3번 반복한 결과를 출력하세요.
print("Hi!" * 3)

# 6. 문자열 포매팅
# 사과를 5개 먹었다는 문장을 %d를 이용해서 출력하세요.
# 예: "I ate 5 apples"
print( "I ate %d apples" % 5 )

# 7. 문자열 함수 - count()
# 문자열 "banana"에서 문자 'a'가 몇 번 나오는지 세어보세요.
str = "banana"
print( str.count('a') )

# 8. 문자열 함수 - find()와 index() 차이
# 문자열 "hello"에서 'e'의 위치를 find()와 index()로 각각 찾아보고,
# 'z'를 찾을 때 두 함수의 차이를 설명해보세요. (또는 출력해보세요)
try:
    a = "hello"
    print( a.find('e') )
    print( a.find('z') )
    print( a.index('e') )
    print( a.index('z') )
except ValueError:
    print("값을 찾을 수 없습니다.")

# 9. 문자열 나누기
# 문자열 "apple,banana,grape"를 ,를 기준으로 나눠서 리스트로 만들어보세요.
fruit = "apple,banana,grape"
print( fruit.split(',') )

# 10. 문자열 바꾸기
# 문자열 "I love Java"에서 "Java"를 "Python"으로 바꿔보세요.
str = "I love Java"
print( str.replace("Java", "Python") )