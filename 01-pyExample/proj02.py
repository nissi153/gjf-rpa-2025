# proj02.py

# 콘솔기반 자판기 앱
# 클래스 기반으로 작성합니다.

'''
== 자판기 ===
상품 목록:
1. 콜라 - 1500원 (10개)
2. 사이다 - 1300원 (8개)
3. 커피 - 2000원 (5개)
4. 돈 넣기
5. 거스름돈 반환
6. 종료
현재 투입된 금액: 0원

선택하세요 (1-6): 4
넣을 금액을 입력하세요: 3000
3000원이 투입되었습니다. 총 금액: 3000원

=== 자판기 ===
상품 목록:
1. 콜라 - 1500원 (10개)
2. 사이다 - 1300원 (8개)
3. 커피 - 2000원 (5개)
4. 돈 넣기
5. 거스름돈 반환
6. 종료
현재 투입된 금액: 3000원

선택하세요 (1-6): 1
콜라을(를) 구매했습니다!
잔액: 1500원

=== 자판기 ===
상품 목록:
1. 콜라 - 1500원 (9개)
2. 사이다 - 1300원 (8개)
3. 커피 - 2000원 (5개)
4. 돈 넣기
5. 거스름돈 반환
6. 종료
현재 투입된 금액: 1500원

선택하세요 (1-6): 2
사이다을(를) 구매했습니다!
잔액: 200원

=== 자판기 ===
상품 목록:
1. 콜라 - 1500원 (9개)
2. 사이다 - 1300원 (7개)
3. 커피 - 2000원 (5개)
4. 돈 넣기
5. 거스름돈 반환
6. 종료
현재 투입된 금액: 200원

선택하세요 (1-6): 6
프로그램을 종료합니다.

총 매출: 2800원
재고 현황:
- 콜라: 9개
- 사이다: 7개
- 커피: 5개
거스름돈 200원이 반환되었습니다.
'''

class VendingMachine:
    def __init__(self):
        # 상품 정보 (이름, 가격, 재고)
        self.products = {  # 딕셔너리 - 키가 숫자인 경우, 값도 Dict
            1: {"name": "콜라", "price": 1500, "stock": 10},
            2: {"name": "사이다", "price": 1300, "stock": 8},
            3: {"name": "커피", "price": 2000, "stock": 5}
        }
        
        self.inserted_money = 0  # 현재 투입된 금액
        self.total_sales = 0     # 총 매출
    
    def display_menu(self):
        """메뉴를 출력하는 함수"""
        print("\n=== 자판기 ===")
        print("상품 목록:")
        
        for num, product in self.products.items():
            print(f"{num}. {product['name']} - {product['price']}원 ({product['stock']}개)")
        
        print("4. 돈 넣기")
        print("5. 거스름돈 반환")
        print("6. 종료")
        print(f"현재 투입된 금액: {self.inserted_money}원")
    
    def insert_money(self):
        """돈을 넣는 함수"""
        try:
            amount = int(input("넣을 금액을 입력하세요: "))
            if amount > 0:
                self.inserted_money += amount
                print(f"{amount}원이 투입되었습니다. 총 금액: {self.inserted_money}원")
            else:
                print("0원보다 큰 금액을 입력해주세요.")
        except ValueError:
            print("올바른 금액을 입력해주세요.")
    
    def buy_product(self, product_num):
        """상품을 구매하는 함수"""
        if product_num not in self.products:
            print("잘못된 상품 번호입니다.")
            return
        
        product = self.products[product_num]
        
        # 재고 확인
        if product["stock"] <= 0:
            print(f"{product['name']}은(는) 품절입니다.")
            return
        
        # 금액 확인
        if self.inserted_money < product["price"]:
            print(f"금액이 부족합니다. {product['price'] - self.inserted_money}원이 더 필요합니다.")
            return
        
        # 구매 처리
        self.products[product_num]["stock"] -= 1
        self.inserted_money -= product["price"]
        self.total_sales += product["price"]
        
        print(f"{product['name']}을(를) 구매했습니다!")
        print(f"잔액: {self.inserted_money}원")
    
    def return_change(self):
        """거스름돈을 반환하는 함수"""
        if self.inserted_money > 0:
            print(f"거스름돈 {self.inserted_money}원이 반환되었습니다.")
            self.inserted_money = 0
        else:
            print("반환할 거스름돈이 없습니다.")
    
    def show_final_status(self):
        """최종 상태를 출력하는 함수"""
        print(f"\n총 매출: {self.total_sales}원")
        print("재고 현황:")
        for product in self.products.values():
            print(f"- {product['name']}: {product['stock']}개")
        
        if self.inserted_money > 0:
            print(f"거스름돈 {self.inserted_money}원이 반환되었습니다.")
    
    def run(self):
        """자판기 메인 실행 함수"""
        print("자판기 프로그램을 시작합니다!")
        
        while True:
            self.display_menu()
            
            try:
                choice = int(input("\n선택하세요 (1-6): "))
                
                if choice in [1, 2, 3]:
                    self.buy_product(choice)
                elif choice == 4:
                    self.insert_money()
                elif choice == 5:
                    self.return_change()
                elif choice == 6:
                    print("프로그램을 종료합니다.")
                    self.show_final_status()
                    break
                else:
                    print("1-6 사이의 번호를 선택해주세요.")
                    
            except ValueError:
                print("숫자를 입력해주세요.")
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                self.show_final_status()
                break

def main():
    """메인 함수"""
    vending_machine = VendingMachine()
    vending_machine.run()

if __name__ == "__main__":
    main()


