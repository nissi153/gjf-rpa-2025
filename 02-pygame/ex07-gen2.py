import pygame
import random
import math

# 초기화
pygame.init()

# 게임 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# 플레이어 클래스
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.speed = 5
        self.health = 100
        self.max_health = 100
        
    def update(self):
        # 키보드 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # 화면 경계 처리
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)
        
        # 체력바 그리기
        bar_width = 50
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 15
        
        # 체력바 배경
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # 현재 체력
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

# 좀비 클래스
class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12
        self.speed = random.uniform(1, 2)
        self.health = 50
        
    def update(self, player):
        # 플레이어를 향해 이동
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)
        
    def check_collision(self, player):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < self.size + player.size

# 총알 클래스
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = 3
        self.speed = 8
        
        # 타겟 방향 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 화면 밖으로 나가면 제거
        return (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
        
    def check_collision(self, zombie):
        distance = math.sqrt((self.x - zombie.x)**2 + (self.y - zombie.y)**2)
        return distance < self.size + zombie.size

# 게임 클래스
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("좀비 생존 게임")
        self.clock = pygame.time.Clock()
        
        # 게임 객체들
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.zombies = []
        self.bullets = []
        
        # 게임 상태
        self.score = 0
        self.wave = 1
        self.zombies_killed = 0
        self.zombies_per_wave = 5
        self.last_shot_time = 0
        self.shot_delay = 200  # 총알 발사 간격 (밀리초)
        
        # 폰트 (한글 지원)
        try:
            # 시스템 폰트 중 한글을 지원하는 폰트 찾기
            self.font = pygame.font.SysFont('malgun gothic', 36)  # Windows
            if not self.font:
                self.font = pygame.font.SysFont('applegothic', 36)  # macOS
            if not self.font:
                self.font = pygame.font.SysFont('nanumgothic', 36)  # Linux
        except:
            # 기본 폰트 사용
            self.font = pygame.font.Font(None, 36)
        
        # 첫 번째 웨이브 생성
        self.spawn_wave()
    
    def spawn_wave(self):
        for _ in range(self.zombies_per_wave):
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
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 클릭
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_shot_time > self.shot_delay:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        bullet = Bullet(self.player.x, self.player.y, mouse_x, mouse_y)
                        self.bullets.append(bullet)
                        self.last_shot_time = current_time
        return True
    
    def update(self):
        # 플레이어 업데이트
        self.player.update()
        
        # 좀비 업데이트
        for zombie in self.zombies:
            zombie.update(self.player)
            
            # 좀비와 플레이어 충돌 확인
            if zombie.check_collision(self.player):
                self.player.health -= 1
                if self.player.health <= 0:
                    return False  # 게임 오버
        
        # 총알 업데이트
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]
        
        # 총알과 좀비 충돌 확인
        for bullet in self.bullets[:]:
            for zombie in self.zombies[:]:
                if bullet.check_collision(zombie):
                    self.bullets.remove(bullet)
                    self.zombies.remove(zombie)
                    self.score += 10
                    self.zombies_killed += 1
                    break
        
        # 웨이브 완료 확인
        if len(self.zombies) == 0:
            self.wave += 1
            self.zombies_per_wave += 2  # 웨이브마다 좀비 수 증가
            self.spawn_wave()
        
        return True
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # 게임 객체들 그리기
        self.player.draw(self.screen)
        
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # UI 그리기
        score_text = self.font.render(f"점수: {self.score}", True, BLACK)
        wave_text = self.font.render(f"웨이브: {self.wave}", True, BLACK)
        health_text = self.font.render(f"체력: {self.player.health}", True, BLACK)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(wave_text, (10, 50))
        self.screen.blit(health_text, (10, 90))
        
        # 조작법 안내
        try:
            help_font = pygame.font.SysFont('malgun gothic', 24)
            if not help_font:
                help_font = pygame.font.SysFont('applegothic', 24)
            if not help_font:
                help_font = pygame.font.SysFont('nanumgothic', 24)
        except:
            help_font = pygame.font.Font(None, 24)
        
        help_text = help_font.render("WASD/방향키: 이동, 마우스 클릭: 공격", True, GRAY)
        self.screen.blit(help_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
    
    def game_over_screen(self):
        self.screen.fill(BLACK)
        
        # 한글 폰트 설정
        try:
            big_font = pygame.font.SysFont('malgun gothic', 72)
            medium_font = pygame.font.SysFont('malgun gothic', 48)
            small_font = pygame.font.SysFont('malgun gothic', 36)
            
            if not big_font:
                big_font = pygame.font.SysFont('applegothic', 72)
                medium_font = pygame.font.SysFont('applegothic', 48)
                small_font = pygame.font.SysFont('applegothic', 36)
            
            if not big_font:
                big_font = pygame.font.SysFont('nanumgothic', 72)
                medium_font = pygame.font.SysFont('nanumgothic', 48)
                small_font = pygame.font.SysFont('nanumgothic', 36)
        except:
            big_font = pygame.font.Font(None, 72)
            medium_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 36)
        
        game_over_text = big_font.render("게임 오버!", True, RED)
        score_text = medium_font.render(f"최종 점수: {self.score}", True, WHITE)
        wave_text = medium_font.render(f"도달한 웨이브: {self.wave}", True, WHITE)
        restart_text = small_font.render("R키를 눌러 재시작, Q키를 눌러 종료", True, WHITE)
        
        # 텍스트 중앙 배치
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
        self.screen.blit(wave_text, (SCREEN_WIDTH//2 - wave_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
        
        pygame.display.flip()
        
        # 재시작 또는 종료 대기
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True  # 재시작
                    elif event.key == pygame.K_q:
                        return False  # 종료
        
        return False
    
    def run(self):
        running = True
        game_active = True
        
        while running:
            if game_active:
                running = self.handle_events()
                if running:
                    game_active = self.update()
                    self.draw()
            else:
                # 게임 오버 상태
                restart = self.game_over_screen()
                if restart:
                    # 게임 재시작
                    self.__init__()
                    game_active = True
                else:
                    running = False
            
            self.clock.tick(FPS)
        
        pygame.quit()

# 게임 실행
if __name__ == "__main__":
    game = Game()
    game.run()