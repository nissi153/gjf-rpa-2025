# ex4-4.py
# 세트 Set (집합)
# 중복되지 않는 요소를 가지며, 비순차적인 집합 특성을 갖는 데이터 구조
# 합집합, 교집합, 차집합 

set_0 = { 1, 2, 3, 3 }
set_1 = set( [1, 2, 3, 3] )
set_2 = set( "Hello" )
set_3 = set()

print(set_0) # {1, 2, 3}
print(set_1)
print(set_2) # {'l', 'o', 'e', 'H'}
print(set_3)

# 인덱스를 이용하려면 리스트로 타입 변경한다
list_0 = list( set_0 )
print( list_0 )
print( list_0[0] )
# 리스트를 세트로 변경
list_10 = [10, 20, 30]
set_10 = set( list_10 )
print( set_10 )
