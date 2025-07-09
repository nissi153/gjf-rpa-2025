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
my_list.append("d") # 마지막에 추가
print( my_list )

my_list.insert(0, "z")
print( my_list )

other_list = ["x", "y"]
my_list.extend( other_list )
print( my_list )

# 요소 삭제
my_list = ['a','b','c','d','e']
del my_list[2] # 인덱스 2의 'c' 삭제
print( my_list ) # ['a', 'b', 'd', 'e']

my_list.remove('b') # ['a', 'd', 'e']
print( my_list )

popped_item = my_list.pop(0) # 0번 인덱스를 삭제후 삭제된 리스트 반환한다.
print(popped_item)
print(my_list)

my_list.clear() # 모든 요소 삭제
print(my_list)

# 리스트의 길이(요소갯수)
print( len(mixed_list) )

socores = [85, 92, 78, 92, 65]

# 정렬( 오름차순 )
socores.sort()
print( socores ) # [65, 78, 85, 92, 92]

socores.reverse()
print( socores ) # [92, 92, 85, 78, 65]

print( socores.count( 92 ) )
print( socores.index( 78 ) )