# ex2-8.py
# 조건문
# 특정 조건이 참일 때만, 코드를 실행하게 한다. 선택적 실행.

# if 조건(절, True 또는 False):
#     조건이 Ture일 때 실행될 코드(들여쓰기 필수!)

# 단순 if문
score = 85
if score >= 60:
    print("합격입니다!")

# if else문
age = 15
if age >= 18:
    print("성인입니다.")
else:
    print("미성년자입니다.")    

# if elif문 
month = 6
if month <= 3:
    print("1,2,3월")
elif month <= 6:
    print("4,5,6월")

# if elif else문
month = 6
if month <= 3:
    print("1,2,3월")
elif month <= 6:
    print("4,5,6월")
else:
    print("그외의 월")