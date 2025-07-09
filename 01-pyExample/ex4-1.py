# ex4-1.py
# 리스트 List : 여러 개의 값을 순서대로 저장하고 관리할 때 사용

# 빈 리스트
empty_list = []
print( empty_list )

numbers = [1, 2, 3, 4, 5]
mixed_list = ["apple", 123, 3.14, True ]
nested_list = [ [1,2], ["a", "b"], [True, False] ]

print( numbers[0] ) # 1 0인덱스
print( numbers[:3] ) # [1, 2, 3] 0~2 인덱스
print( numbers[1:] ) # [2, 3, 4, 5] 1~마지막 인덱스
print( numbers[::2] ) # [1, 3, 5] 두 칸씩 인덱스
print( numbers[::-1] ) # [5, 4, 3, 2, 1] 역순으로 

# 요소 변경
my_list = ["a", "b", "c"]  # 인덱스 0,1,2
my_list[1] = "hello"
print( my_list )

# my_list[3] = "d" # index out of range
my_list.append("d")
print( my_list )

