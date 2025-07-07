# 문자열 다루기
str = "Life is too short, You need Python"
print( str )

# 여러줄 문자열
multiline = """
Life is too short,
You need Pyton
"""
print( multiline )

# 문자열 중간에 단따옴표 넣기
print( "Python\'s favorite food is perl" )
# 문자열 중간에 쌍따옴표 넣기
print( 'Python\"s favorite food is perl' )

# 문자열 합치기
print( "Python" + " is fun!" )
# 문자열 곱하기
print( "Python" * 3 )
print( "=" * 50 )

# 문자열 인덱싱
str = "Life is too short, You need Python"
print( str[0] ) # 첫번째 문자
print( str[1] )
print( str[-1] ) # 마지막 문자
print( str[-2] )

# 문자열 슬라이싱
print( str[0:4] ) # Life  시작인덱스:끝인덱스+1
print( str[0:5] )
# "You need Python"을 출력
print( str[19:] )
print( str[:17] ) # "Life is too short"
print( str[:] )
print( str[19:-7] )

# 문자열 포매팅( 문자열에 변수값 넣기 )
print( "I eat %d apples" % 3 )
print( "I eat %d apples, I sell %d apples" % (3, 2) )
print( "%0.4f" % 3.42134234) # 소숫점 4자리까지 출력
print( "%10.4f" % 3.42134234) # 전체자릿수 10자리, 소숫점 4자리까지 출력