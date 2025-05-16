import pygame
import random
import sys
import json
import os

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")

# Load background
bg_img = pygame.image.load("assets-2/BG.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Load hình máy bay
player_img = pygame.image.load("assets-2/Player_BTN.png")
player_img = pygame.transform.scale(player_img, (100, 80))
enemy_img = pygame.image.load("assets-2/Enemy_BTN.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# Load hình ảnh đạn
bullet_img = pygame.image.load("assets-2/Bullet_BTN.png")
bullet_img = pygame.transform.scale(bullet_img, (30, 25))

#Load hình coin
coin_img = pygame.image.load("assets-2/coin.png")
coin_img = pygame.transform.scale(coin_img, (12,12))

# Load hình ảnh nút
start_btn_img = pygame.image.load("assets-2/Start_BTN.png")
replay_btn_img = pygame.image.load("assets-2/Replay_BTN.png")
exit_btn_img = pygame.image.load("assets-2/Exit_BTN.png")

# Load hình ảnh header
header1_img = pygame.image.load("assets-2/Header1.png")
header1_img = pygame.transform.scale(header1_img, (500, 50))
header2_img = pygame.image.load("assets-2/Header2.png")
header2_img = pygame.transform.scale(header2_img, (450, 60))

# Màu sắc
WHITE = (255, 255, 255)

# Font chữ
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 36)  # Font cho điểm số

# Biến điểm
score = 0
high_score = 0

# Vàng, mana
coins_score = 0
total_coins = 0
mana = 0

# File lưu điểm cao nhất
SCORE_FILE = "high_score.json"

def load_high_score():
    global high_score
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                data = json.load(f)
                high_score = data.get('high_score', 0)
    except:
        high_score = 0

def load_total_coins():
    global total_coins
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                data = json.load(f)
                total_coins = data.get('total_coins', 0)
    except:
        total_coins = 0

def add_total_coin():
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump({'high_score': high_score , 'total_coins' : total_coins + coins_score}, f)
    except:
        pass

def save_high_score():
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump({'high_score': high_score, 'total_coins' : total_coins + coins_score}, f)
    except:
        pass

# Class Button
class Button:
    def __init__(self, x, y, width, height, image):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False

    def draw(self, surface):
        # Hiệu ứng hover: tăng sáng nhẹ
        if self.is_hovered:
            img = self.image.copy()
            img.fill((30, 30, 30, 0), special_flags=pygame.BLEND_RGB_ADD)
            surface.blit(img, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Người chơi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8

    def update(self):
        # Lấy vị trí chuột
        mouse_pos = pygame.mouse.get_pos()
        # Di chuyển máy bay đến vị trí chuột theo trục x
        self.rect.centerx = mouse_pos[0]
        # Giới hạn không cho máy bay đi ra ngoài màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
# Coins
class Coin(pygame.sprite.Sprite):
    def __init__(self, val, x ,y):
        super().__init__()
        self.image = coin_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.val = val
        self.speed = 0.5
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            all_sprites.remove(self)

# Kẻ địch
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.coins = random.randint(1,100)
        self.manas = random.randint(1,3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

# Tạo sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
coins = pygame.sprite.Group()
# Tạo người chơi
player = Player()
all_sprites.add(player)

# Tạo kẻ địch
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def game_over_screen():
    global high_score
    
    # Cập nhật điểm cao nhất
    if score > high_score:
        high_score = score
        save_high_score()
    # Cập nhật coins
    add_total_coin()
    
    screen.blit(bg_img, (0, 0))
    # Vẽ YOU LOSE
    screen.blit(header1_img, (WIDTH//2 - header1_img.get_width()//2, HEIGHT//2 - 180))
    
    # Hiển thị điểm số
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 80))
    
    # Hiển thị điểm cao nhất
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 30))
    
    # Các nút
    replay_w, replay_h = 60, 50
    exit_w, exit_h = 200, 50
    button_gap = 20
    total_width = replay_w + button_gap + exit_w
    start_x = WIDTH//2 - total_width//2
    y = HEIGHT//2 + 30
    
    restart_button = Button(start_x, y, replay_w, replay_h, replay_btn_img)
    quit_button = Button(start_x + replay_w + button_gap, y, exit_w, exit_h, exit_btn_img)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if restart_button.handle_event(event):
                waiting = False
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        
        # Vẽ các nút
        restart_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

def reset_game():
    global all_sprites, enemies, bullets, player, score
    
    # Reset điểm số
    score = 0
    
    # Xóa tất cả sprite
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    
    # Tạo lại người chơi
    player = Player()
    all_sprites.add(player)
    
    # Tạo lại kẻ địch
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

def start_screen():
    screen.blit(bg_img, (0, 0))
    # Vẽ hình SPACE GAME
    screen.blit(header1_img, (WIDTH//2 - header1_img.get_width()//2, HEIGHT//2 - 180))
    # Hiển thị điểm cao nhất
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 60))
    # Hiển thị số coin đang có
    total_coins_text = score_font.render(f"Total coins: {total_coins}", True, WHITE)
    screen.blit(total_coins_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 100))
    # Tạo các nút
    start_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, start_btn_img)
    exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, exit_btn_img)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if start_button.handle_event(event):
                waiting = False
            if exit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        
        # Vẽ các nút
        start_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()

# Game loop
clock = pygame.time.Clock()
running = True
mouse_pressed = False
shoot_delay = 100
last_shot = 0

# Load điểm cao nhất khi bắt đầu game
load_high_score()
# Load total coins
load_total_coins()

# Hiển thị màn hình bắt đầu
start_screen()

while running:
    # Giữ game chạy ở 60 FPS
    clock.tick(60)
    current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại
    
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Chuột trái
                mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Chuột trái
                mouse_pressed = False

    # Bắn đạn khi giữ chuột và đã đủ thời gian chờ
    if mouse_pressed and current_time - last_shot > shoot_delay:
        player.shoot()
        last_shot = current_time

    # Update
    all_sprites.update()

    # Kiểm tra va chạm giữa đạn và kẻ địch
    hits_bullet = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits_bullet:
        score += 1  # Tăng điểm khi bắn trúng
        enemy = Enemy()
        coin = Coin(hit.coins, hit.rect.x, hit.rect.y)
        all_sprites.add(enemy, coin)
        enemies.add(enemy)
        coins.add(coin)

    # Kiểm tra va chạm player và coin
    hits_coin = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits_coin:
        coins_score += hit.val

    # Kiểm tra va chạm giữa người chơi và kẻ địch
    hits_enemy = pygame.sprite.spritecollide(player, enemies, False)
    if hits_enemy:
        game_over_screen()
        reset_game()

    # Vẽ
    screen.blit(bg_img, (0, 0))
    all_sprites.draw(screen)
    
    # Hiển thị điểm số
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    coins_score_text = score_font.render(f"Coins: {coins_score}", True, WHITE)
    screen.blit(coins_score_text, (10,50))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit() 