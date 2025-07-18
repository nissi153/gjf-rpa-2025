import pygame
import sys

# pygame 라이브러리 : 파이썬에서 2D게임만드는 기능을 가진 라이브러리.
# pip install pygame  : 관리자 권한으로 열기
# py -m pip install pygame

# 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("기본 창 띄우기")

# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))  # 흰색 배경
    pygame.display.update()
