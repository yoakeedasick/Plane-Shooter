import pygame
import random
import sys
import json
import os

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")

# Load background
bg_img = pygame.image.load("assets-2/BG.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Load hình máy bay
player_img = pygame.image.load("assets-2/Player.png")
player_img = pygame.transform.scale(player_img, (100, 80))
enemy_img = pygame.image.load("assets-2/Enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# Load hình ảnh đạn
bullet_img = pygame.image.load("assets-2/Bullet_BTN.png")
bullet_img = pygame.transform.scale(bullet_img, (30, 25))

# Load hình tên lửa
rocket_img = pygame.image.load("assets-2/Rocket.png")
rocket_img = pygame.transform.scale(rocket_img, (15, 40))

# Load hình nâng cấp
upgrade_img = pygame.image.load("assets-2/Upgrade.png")
upgrade_img = pygame.transform.scale(upgrade_img, (30, 40))

#Load hình Cristal
cristal_img = pygame.image.load("assets-2/Cristal_Icon.png")
cristal_img = pygame.transform.scale(cristal_img, (17, 27))

#Load ảnh mana
mana_img = pygame.image.load("assets-2/mana.png")
mana_img = pygame.transform.scale(mana_img, (17,17))

# Load hình ảnh nút
start_btn_img = pygame.image.load("assets-2/Start_BTN.png")
replay_btn_img = pygame.image.load("assets-2/Replay_BTN.png")
exit_btn_img = pygame.image.load("assets-2/Exit_BTN.png")
shop_btn_img = pygame.image.load("assets-2/Shop_BTN.png")
menu_btn_img = pygame.image.load("assets-2/Menu_BTN.png") 
pause_btn_img = pygame.image.load("assets-2/Pause_BTN.png")
continue_btn_img = pygame.image.load("assets-2/Continue_BTN.png")

table_img = pygame.image.load("assets-2/Table.png")

# Load hình ảnh header
start_img = pygame.image.load("assets-2/Start.png")
start_img = pygame.transform.scale(start_img, (400, 50))
end_img = pygame.image.load("assets-2/End.png")
end_img = pygame.transform.scale(end_img, (450, 60))
shop_img = pygame.image.load("assets-2/Shop.png")
shop_img = pygame.transform.scale(shop_img, (100, 25))
pause_img = pygame.image.load("assets-2/Pause.png")
pause_img = pygame.transform.scale(pause_img, (200, 40))

# Màu sắc
WHITE = (255, 255, 255)

# Font chữ
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 36)  # Font cho điểm số

# Biến điểm
score = 0
high_score = 0
is_paused = False  # biến theo dõi trạng thái tạm dừng
from_menu = False  # biến theo dõi nguồn gọi start_screen
resume_time = 0  # biến theo dõi thời gian tiếp tục

# Cristal
cristal_score = 0
total_cristal = 0

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

def load_total_cristal():
    global total_cristal
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                data = json.load(f)
                total_cristal = data.get('total_cristal', 0)
    except:
        total_cristal = 0

def add_total_cristal():
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump({'high_score': high_score , 'total_cristal' : total_cristal + cristal_score}, f)
    except:
        pass

def save_high_score():
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump({'high_score': high_score, 'total_cristal' : total_cristal + cristal_score}, f)
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
        self.left_rockets = 0  # Số tên lửa bên trái
        self.right_rockets = 0  # Số tên lửa bên phải
        self.last_pos = (WIDTH // 2, HEIGHT - 10)  # Lưu vị trí cuối cùng

    def update(self):
        current_time = pygame.time.get_ticks()
        # Chỉ cho phép di chuyển sau khi đã qua thời gian chờ tiếp tục
        if current_time - resume_time > 700:  # Đợi 700ms sau khi tiếp tục
            # Lấy vị trí chuột
            mouse_pos = pygame.mouse.get_pos()
            # Di chuyển máy bay đến vị trí chuột theo cả trục x và y
            self.rect.centerx = mouse_pos[0]
            self.rect.centery = mouse_pos[1]
            self.last_pos = (self.rect.centerx, self.rect.centery)
        else:
            # Giữ nguyên vị trí cuối cùng
            self.rect.centerx = self.last_pos[0]
            self.rect.centery = self.last_pos[1]

        # Giới hạn không cho máy bay đi ra ngoài màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
        # Bắn tên lửa liên tục nếu có
        if self.left_rockets > 0:
            rocket = Rocket(self.rect.left + 20, self.rect.top)
            all_sprites.add(rocket)
            bullets.add(rocket)
            
        if self.right_rockets > 0:
            rocket = Rocket(self.rect.right - 20, self.rect.top)
            all_sprites.add(rocket)
            bullets.add(rocket)

    def add_rocket(self):
        # Thêm tên lửa vào bên có ít tên lửa hơn
        if self.left_rockets <= self.right_rockets and self.left_rockets < 1:
            self.left_rockets += 1
        elif self.right_rockets < 1:
            self.right_rockets += 1

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

# Tên lửa
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rocket_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -12

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Vật phẩm nâng cấp
class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = upgrade_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Cristal
class Cristal(pygame.sprite.Sprite):
    def __init__(self, val, x ,y):
        super().__init__()
        self.image = cristal_img.convert_alpha()
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
        self.rect.y = random.randrange(-150, -60)
        self.speedy = random.randrange(1, 4)
        self.coins = random.randint(1,100)
        self.manas = random.randint(1,3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -60)
            self.speedy = random.randrange(1, 4)

# Class Shop
class Shop:
    def __init__(self):
        self.image = pygame.transform.scale(shop_btn_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH - 10, 10)
        self.is_hovered = False

    def draw(self, surface):
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
                shop_screen()  # Chuyển sang màn hình shop
                return True
        return False

# Class Pause
class Pause:
    def __init__(self):
        self.image = pygame.transform.scale(pause_btn_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.bottomright = (WIDTH - 10, HEIGHT - 10)
        self.is_hovered = False

    def draw(self, surface):
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
                pause_screen()
                return True
        return False



# Tạo sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
cristal = pygame.sprite.Group()
manas = pygame.sprite.Group()
upgrades = pygame.sprite.Group()  # Thêm group cho upgrade

# Tạo người chơi và pause button
player = Player()
pause_button = Pause()  # Tạo instance của PauseButton
all_sprites.add(player)

# Tạo kẻ địch
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Màn hình bắt đầu
def start_screen():
    global is_paused, from_menu
    load_high_score()

    # Nếu đang tạm dừng và không phải từ menu, quay lại game
    if is_paused and not from_menu:
        is_paused = False
        return
    
    # Nếu từ menu, reset game
    if from_menu:
        reset_game()
        is_paused = False

    screen.blit(bg_img, (0, 0))
    # Vẽ hình SPACE GAME
    screen.blit(start_img, (WIDTH//2 - start_img.get_width()//2, HEIGHT//2 - 170))
    # Hiển thị điểm cao nhất
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 70))
    # Tạo các nút
    start_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, start_btn_img)
    exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, exit_btn_img)
    
    # Tạo nút Shop ở góc phải trên
    shop = Shop()
    
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
            # Xử lý sự kiện cho shop
            shop.handle_event(event)
        
        # Vẽ các nút
        start_button.draw(screen)
        exit_button.draw(screen)
        shop.draw(screen)  # Vẽ nút Shop
        pygame.display.flip()

# Màn hình tạm dừng
def pause_screen():
    global is_paused, from_menu, resume_time
    is_paused = True  # Đánh dấu game đang tạm dừng
    
    # Kích thước nút
    btn_w, btn_h = 60, 50
    btn_gap = 20
    total_width = btn_w * 3 + btn_gap * 2
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT // 2 - 50

    continue_button = Button(start_x, y, btn_w, btn_h, continue_btn_img)
    replay_button = Button(start_x + btn_w + btn_gap, y, btn_w, btn_h, replay_btn_img)
    menu_button = Button(start_x + (btn_w + btn_gap) * 2, y, btn_w, btn_h, menu_btn_img)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if continue_button.handle_event(event):
                resume_time = pygame.time.get_ticks()  # Lưu thời điểm nhấn tiếp tục
                waiting = False
            if replay_button.handle_event(event):
                waiting = False
                reset_game()
            if menu_button.handle_event(event):
                waiting = False
                from_menu = True
                start_screen()
                from_menu = False
                return
        
        # Vẽ
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        
        # Vẽ lớp overlay tối
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Vẽ chữ PAUSE
        screen.blit(pause_img, (WIDTH//2 - pause_img.get_width()//2, HEIGHT//2 - 120))
        
        # Vẽ các nút 
        continue_button.draw(screen)
        replay_button.draw(screen)
        menu_button.draw(screen)
        
        pygame.display.flip()

# Màn hình game over
def game_over_screen():
    global high_score
    
    # Cập nhật điểm cao nhất
    if score > high_score:
        high_score = score
        save_high_score()
    # Cập nhật Cristal
    add_total_cristal()
    
    screen.blit(bg_img, (0, 0))
    # Vẽ YOU LOSE
    screen.blit(end_img, (WIDTH//2 - end_img.get_width()//2, HEIGHT//2 - 190))
    
    # Hiển thị điểm số
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 100))
    
    # Hiển thị số cristal đã thu thập trong màn này
    cristal_text = score_font.render(f"Cristal: {cristal_score}", True, WHITE)
    screen.blit(cristal_text, (WIDTH//2 - cristal_text.get_width()//2, HEIGHT//2 - 50))
    
    # Hiển thị điểm cao nhất
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2))
    
    # Các nút
    replay_w, replay_h = 60, 50
    menu_w, menu_h = 60, 50
    exit_w, exit_h = 200, 50
    button_gap = 20
    
    # Tính toán vị trí cho các nút
    total_width = replay_w + button_gap + menu_w
    start_x = WIDTH//2 - total_width//2
    y = HEIGHT//2 + 60
    
    restart_button = Button(start_x, y, replay_w, replay_h, replay_btn_img)
    menu_button = Button(start_x + replay_w + button_gap, y, menu_w, menu_h, menu_btn_img)
    quit_button = Button(WIDTH//2 - exit_w//2, y + replay_h + button_gap, exit_w, exit_h, exit_btn_img)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if restart_button.handle_event(event):
                waiting = False
            if menu_button.handle_event(event):
                waiting = False
                add_total_cristal()
                start_screen()
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        
        # Vẽ các nút
        restart_button.draw(screen)
        menu_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

def reset_game():
    global all_sprites, enemies, bullets, player, score, cristal_score
    
    # Reset điểm số và cristal
    score = 0
    cristal_score = 0
    
    # Xóa tất cả sprite
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    cristal.empty()
    
    # Tạo lại người chơi
    player = Player()
    all_sprites.add(player)
    
    # Tạo lại kẻ địch
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Màn hình shop
def shop_screen():    
    load_total_cristal()
    # Tạo nút quay về menu
    menu_button = Button(WIDTH - 60, 10, 50, 50, menu_btn_img)
    
    # Thiết lập bảng
    table = pygame.transform.scale(table_img, (400, 500))
    table_rect = table.get_rect()
    table_rect.center = (WIDTH // 2, HEIGHT // 2)
    
    # Thiết lập hình chữ Shop
    shop_title_rect = shop_img.get_rect()
    shop_title_rect.midtop = (table_rect.centerx, table_rect.top + 15)
    
    # Thiết lập hiển thị cristal
    cristal_display = pygame.transform.scale(cristal_img, (20, 30))
    cristal_rect = cristal_display.get_rect()
    cristal_rect.topleft = (10, 10)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if menu_button.handle_event(event):
                waiting = False
                start_screen()
                return
        
        # Vẽ
        screen.blit(bg_img, (0, 0))
        screen.blit(table, table_rect)
        screen.blit(shop_img, shop_title_rect)
        menu_button.draw(screen)
        
        # Vẽ hình cristal và số lượng
        screen.blit(cristal_display, cristal_rect)
        cristal_text = score_font.render(f"{total_cristal}", True, WHITE)
        screen.blit(cristal_text, (cristal_rect.right + 5, cristal_rect.centery - cristal_text.get_height()//2))
        
        pygame.display.flip()

# Game loop
clock = pygame.time.Clock()
running = True
mouse_pressed = False
shoot_delay = 100
last_shot = 0

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
        # Xử lý sự kiện cho nút pause
        pause_button.handle_event(event)

    # Bắn đạn khi giữ chuột và đã đủ thời gian chờ
    if mouse_pressed and current_time - last_shot > shoot_delay:
        # Chỉ cho phép bắn sau khi đã qua thời gian chờ tiếp tục
        if current_time - resume_time > 500:  # Đợi 500ms sau khi tiếp tục
            player.shoot()
            last_shot = current_time

    # Update
    all_sprites.update()

    # Kiểm tra va chạm giữa đạn và kẻ địch
    hits_bullet = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits_bullet:
        score += 1  # Tăng điểm khi bắn trúng
        enemy = Enemy()
        # Đảm bảo y >= 10 (hoặc giá trị phù hợp)
        cristal_y = max(hit.rect.y, 10)
        # Tỉ lệ 50% rơi ra cristal
        if random.random() < 0.3:
            cristal_sprite = Cristal(random.choice([1,2,5]), hit.rect.x, cristal_y)
            all_sprites.add(cristal_sprite)
            cristal.add(cristal_sprite)
        all_sprites.add(enemy)
        enemies.add(enemy)
        
        # Tỉ lệ 20% rơi ra vật phẩm nâng cấp
        if random.random() < 0.2 and (player.left_rockets + player.right_rockets) < 2:
            upgrade_y = max(hit.rect.y, 10)
            upgrade = Upgrade(hit.rect.x, upgrade_y)
            all_sprites.add(upgrade)
            upgrades.add(upgrade)

    # Kiểm tra va chạm player và Cristal
    hits_cristal = pygame.sprite.spritecollide(player, cristal, True)
    for hit in hits_cristal:
        cristal_score += hit.val

    # Kiểm tra va chạm player và upgrade
    hits_upgrade = pygame.sprite.spritecollide(player, upgrades, True)
    for hit in hits_upgrade:
        player.add_rocket()

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
    cristal_score_text = score_font.render(f"Cristal: {cristal_score}", True, WHITE)
    screen.blit(cristal_score_text, (10,50))
    screen.blit(score_text, (10, 10))
    
    # Vẽ nút pause
    pause_button.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit() 