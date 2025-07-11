# ex6-1
# 파일 입출력

# 파일 생성하기
# w 쓰기, r 읽기전용, a 추가
f = open("test1.txt", 'w', encoding='utf-8')
# 줄바꿈 특수문자 \n
f.write('this is test file.\n테스트파일 입니다.')
f.close() # 파일닫기

# 파일 읽어오기
f = open("test1.txt", 'r', encoding='utf-8')
while True:
    line = f.readline()
    if not line: 
        break
    print( line )
f.close()