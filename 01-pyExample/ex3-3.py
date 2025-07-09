# ex3-3.py
# while문(40%) - for문(60%)

# 형식
# 반복변수 초기화
# while 조건절:
#    조건절이 True일 때 반복적으로 수행되는 코드
#    반복변수 증감

# 5초 카운트다운
count = 5
while count > 0:
    print(f"{count}")
    count -= 1  #복합대입 연산자 A -= B  ->  A = A - B
print( "발사!" )

# 반복문을 사용시 무한루프에 빠지는 경우
# 1. 콘솔을 클릭후 CTRL + C 키로 빠져나온다.
# 2. 콘솔 세션을 종료 - 휴지통 버튼을 클릭한다.
# 3. VSCode를 껐다 켠다.
# 4. 작업관리자에서 Python 프로세스 끝내기를 한다.

# 무한루프 만들기 - 자판기,엘리베이터 프로그램
count = 0
while True:
    if count > 10:
        break   # 반복문을 종료한다.
    print(f"무한루프 - {count}")
    count += 1
print("무한루프 종료!")

# countinue 문 : 해당회차를 종료하고 반복문의 처음으로 돌아간다.
# 1부터 10사이의 홀수만 출력하기
for i in range(1, 11):
    if i % 2 == 0:  #짝수이면
        continue    #해당회차 종료, 아랫쪽 print문을 건너뜀
    print( i )


