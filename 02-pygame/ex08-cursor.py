import pygame
import random
import math
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Survival Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_RED = (150, 0, 0)
YELLOW = (255, 255, 0)

# 게임 설정
clock = pygame.time.Clock()
FPS = 60

# 폰트 설정
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 5
        self.color = BLUE
        
    def update(self, mouse_pos):
        # 마우스 방향으로 이동
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 5:  # 마우스와 거리가 5 이상일 때만 이동
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        # 화면 경계 확인
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # 플레이어 중심에 작은 점 표시
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = 3
        self.speed = 8
        self.color = YELLOW
        
        # 타겟 방향으로 이동 벡터 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed
        else:
            self.dx = 0
            self.dy = 0
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def is_out_of_bounds(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)

class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.speed = 2
        self.color = DARK_RED
        
    def update(self, player):
        # 플레이어 방향으로 이동
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # 좀비 눈 그리기
        eye_offset = 5
        pygame.draw.circle(screen, RED, (int(self.x - eye_offset), int(self.y - eye_offset)), 2)
        pygame.draw.circle(screen, RED, (int(self.x + eye_offset), int(self.y - eye_offset)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Game:
    def __init__(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.zombies = []
        self.bullets = []
        self.score = 0
        self.kills = 0
        self.game_over = False
        self.zombie_spawn_timer = 0
        self.zombie_spawn_delay = 120  # 2초마다 좀비 생성 (60 FPS 기준)
        self.survival_time = 0
        
    def spawn_zombie(self):
        # 화면 가장자리에서 좀비 생성
        side = random.randint(0, 3)
        if side == 0:  # 위쪽
            x = random.randint(0, SCREEN_WIDTH)
            y = -20
        elif side == 1:  # 오른쪽
            x = SCREEN_WIDTH + 20
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # 아래쪽
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
        else:  # 왼쪽
            x = -20
            y = random.randint(0, SCREEN_HEIGHT)
            
        self.zombies.append(Zombie(x, y))
    
    def shoot_bullet(self, target_x, target_y):
        bullet = Bullet(self.player.x, self.player.y, target_x, target_y)
        self.bullets.append(bullet)
    
    def update(self):
        if self.game_over:
            return
            
        # 마우스 위치 가져오기
        mouse_pos = pygame.mouse.get_pos()
        
        # 플레이어 업데이트
        self.player.update(mouse_pos)
        
        # 총알 업데이트
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_of_bounds():
                self.bullets.remove(bullet)
        
        # 좀비들 업데이트
        for zombie in self.zombies:
            zombie.update(self.player)
        
        # 좀비 생성
        self.zombie_spawn_timer += 1
        if self.zombie_spawn_timer >= self.zombie_spawn_delay:
            self.spawn_zombie()
            self.zombie_spawn_timer = 0
            # 시간이 지날수록 좀비 생성 속도 증가
            if self.zombie_spawn_delay > 30:
                self.zombie_spawn_delay -= 1
        
        # 총알과 좀비 충돌 검사
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for zombie in self.zombies[:]:
                zombie_rect = zombie.get_rect()
                if bullet_rect.colliderect(zombie_rect):
                    self.bullets.remove(bullet)
                    self.zombies.remove(zombie)
                    self.kills += 1
                    self.score += 10  # 좀비 처치 시 10점 추가
                    break
        
        # 플레이어와 좀비 충돌 검사
        player_rect = self.player.get_rect()
        for zombie in self.zombies:
            zombie_rect = zombie.get_rect()
            if player_rect.colliderect(zombie_rect):
                self.game_over = True
                break
        
        # 생존 시간 점수 증가
        self.survival_time += 1
        if self.survival_time % 60 == 0:  # 1초마다 1점
            self.score += 1
        
        # 화면 밖으로 나간 좀비 제거
        self.zombies = [zombie for zombie in self.zombies 
                       if -50 < zombie.x < SCREEN_WIDTH + 50 and 
                          -50 < zombie.y < SCREEN_HEIGHT + 50]
    
    def draw(self, screen):
        # 배경 그리기
        screen.fill(WHITE)
        
        # 격자 무늬 그리기 (배경 효과)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        
        # 플레이어 그리기
        self.player.draw(screen)
        
        # 총알 그리기
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # 좀비들 그리기
        for zombie in self.zombies:
            zombie.draw(screen)
        
        # UI 그리기
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        kills_text = small_font.render(f"Kills: {self.kills}", True, BLACK)
        screen.blit(kills_text, (10, 50))
        
        zombie_count_text = small_font.render(f"Zombies: {len(self.zombies)}", True, BLACK)
        screen.blit(zombie_count_text, (10, 70))
        
        bullets_count_text = small_font.render(f"Bullets: {len(self.bullets)}", True, BLACK)
        screen.blit(bullets_count_text, (10, 90))
        
        # 조작 안내
        control_text = small_font.render("Mouse Move: Player | Mouse Click: Shoot", True, BLACK)
        screen.blit(control_text, (10, SCREEN_HEIGHT - 30))
        
        # 게임 오버 화면
        if self.game_over:
            # 반투명 오버레이
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 게임 오버 텍스트
            game_over_text = font.render("GAME OVER!", True, RED)
            final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            kills_text = font.render(f"Total Kills: {self.kills}", True, WHITE)
            restart_text = small_font.render("Press SPACE to restart", True, WHITE)
            quit_text = small_font.render("Press ESC to quit", True, WHITE)
            
            # 텍스트 중앙 정렬
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, final_score_rect)
            screen.blit(kills_text, kills_rect)
            screen.blit(restart_text, restart_rect)
            screen.blit(quit_text, quit_rect)
    
    def reset(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.zombies = []
        self.bullets = []
        self.score = 0
        self.kills = 0
        self.game_over = False
        self.zombie_spawn_timer = 0
        self.zombie_spawn_delay = 120
        self.survival_time = 0

def main():
    game = Game()
    
    print("Zombie Survival Game Started!")
    print("Move mouse to control player.")
    print("Click mouse to shoot zombies!")
    print("Survive as long as possible!")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and game.game_over:
                    game.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game.game_over:  # 왼쪽 마우스 클릭
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    game.shoot_bullet(mouse_x, mouse_y)
        
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
