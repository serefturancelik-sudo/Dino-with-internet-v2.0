import pygame
import sys
import random
import math

# --- PYGAME BAŞLANGIÇ ---
pygame.init()
pygame.font.init()

# --- 1. TAM EKRAN AYARI ---
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Dinozor: Uzay Kaçışı (Mobil)")

clock = pygame.time.Clock()
FPS = 60

# --- RENKLER ---
COLOR_BG = (247, 247, 247)       
COLOR_DARK_BG = (30, 30, 40)     
COLOR_MARS_BG = (120, 40, 30)     
COLOR_SPACE_BG = (10, 10, 25)     
COLOR_TEXT = (83, 83, 83)        
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (46, 204, 113)
COLOR_RED = (231, 76, 60)
COLOR_BLUE = (52, 152, 219)
COLOR_YELLOW = (241, 196, 15)
COLOR_ORANGE = (230, 126, 34)
COLOR_GRAY = (200, 200, 200)       
COLOR_DARK_GRAY = (100, 100, 100) 

# --- OYUN DURUMLARI (STATES) ---
STATE_MENU = 0
STATE_CLASSIC = 1    
STATE_WIFI_BOMB = 2  
STATE_PUZZLE = 3     
STATE_HELICOPTER = 4      
STATE_MARS_TRAVEL = 5     
STATE_MARS_BATTLE = 6     
STATE_MARS_KING = 7       
STATE_GAME_OVER = 8  

# --- ÇIZIM FONKSİYONLARI ---
def draw_dino(surf, x, y, frame=0, is_jumping=False):
    current_bg = screen.get_at((0,0)) if (x >= 0 and x < SCREEN_WIDTH and y >= 0 and y < SCREEN_HEIGHT) else COLOR_BG
    erase_color = COLOR_BG if current_bg == COLOR_BG else current_bg
    
    pygame.draw.rect(surf, COLOR_TEXT, (x + 20, y, 24, 16)) 
    pygame.draw.rect(surf, erase_color, (x + 24, y + 4, 4, 4)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x + 16, y + 12, 16, 12)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x + 4, y + 20, 32, 16)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x, y + 24, 8, 8)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x + 32, y + 22, 6, 4)) 
    
    if is_jumping:
        pygame.draw.rect(surf, COLOR_TEXT, (x + 10, y + 36, 6, 6))
        pygame.draw.rect(surf, COLOR_TEXT, (x + 24, y + 36, 6, 6))
    else:
        if frame == 0:
            pygame.draw.rect(surf, COLOR_TEXT, (x + 10, y + 36, 6, 8))
            pygame.draw.rect(surf, COLOR_TEXT, (x + 24, y + 36, 6, 4))
        else:
            pygame.draw.rect(surf, COLOR_TEXT, (x + 10, y + 36, 6, 4))
            pygame.draw.rect(surf, COLOR_TEXT, (x + 24, y + 36, 6, 8))

def draw_cactus(surf, x, y):
    pygame.draw.rect(surf, COLOR_TEXT, (x + 10, y, 8, 40)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x, y + 12, 10, 6)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x, y + 6, 6, 10))
    pygame.draw.rect(surf, COLOR_TEXT, (x + 18, y + 18, 10, 6)) 
    pygame.draw.rect(surf, COLOR_TEXT, (x + 22, y + 10, 6, 12))

def draw_wifi_bomb(surf, x, y, pulse=0):
    pygame.draw.circle(surf, COLOR_RED, (x + 15, y + 15), 12)
    pygame.draw.line(surf, COLOR_ORANGE, (x + 15, y + 3), (x + 15, y - 5), 3)
    if pulse % 20 < 10:
        pygame.draw.circle(surf, COLOR_YELLOW, (x + 15, y - 7), 4) 
        
    pygame.draw.circle(surf, COLOR_WHITE, (x + 15, y + 15), 2)
    pygame.draw.arc(surf, COLOR_WHITE, (x + 10, y + 10, 10, 10), math.pi/4, 3*math.pi/4, 2)
    pygame.draw.arc(surf, COLOR_WHITE, (x + 6, y + 6, 18, 18), math.pi/4, 3*math.pi/4, 2)

def draw_spaceship(surf, x, y, hover=0):
    hover_offset = int(math.sin(hover * 0.1) * 5)
    ny = y + hover_offset
    pygame.draw.ellipse(surf, COLOR_BLUE, (x + 15, ny, 30, 20)) 
    pygame.draw.ellipse(surf, COLOR_GREEN, (x, ny + 10, 60, 20)) 
    pygame.draw.circle(surf, COLOR_YELLOW, (x + 10, ny + 20), 3)
    pygame.draw.circle(surf, COLOR_YELLOW, (x + 30, ny + 22), 3)
    pygame.draw.circle(surf, COLOR_YELLOW, (x + 50, ny + 20), 3)

def draw_helicopter(surf, x, y, frame=0):
    rotor_offset = (frame % 2) * 20
    pygame.draw.line(surf, COLOR_DARK_GRAY, (x - 20 + rotor_offset, y - 15), (x + 60 - rotor_offset, y - 15), 4)
    pygame.draw.line(surf, COLOR_TEXT, (x + 20, y - 15), (x + 20, y), 4)
    pygame.draw.ellipse(surf, COLOR_ORANGE, (x, y, 50, 30))
    pygame.draw.arc(surf, COLOR_BLUE, (x + 25, y + 2, 20, 20), 0, math.pi/2, 3)
    pygame.draw.line(surf, COLOR_ORANGE, (x, y + 15), (x - 30, y + 5), 6)
    pygame.draw.rect(surf, COLOR_RED, (x - 35, y, 8, 15))
    pygame.draw.line(surf, COLOR_TEXT, (x + 5, y + 30), (x + 10, y + 38), 3)
    pygame.draw.line(surf, COLOR_TEXT, (x + 35, y + 30), (x + 40, y + 38), 3)
    pygame.draw.line(surf, COLOR_TEXT, (x - 5, y + 38), (x + 50, y + 38), 4)

def draw_martian(surf, x, y, frame=0):
    bounce = int(math.sin(frame * 0.15) * 4)
    pygame.draw.circle(surf, COLOR_GREEN, (x + 20, y + 15 + bounce), 12)
    pygame.draw.line(surf, COLOR_GREEN, (x + 15, y + 5 + bounce), (x + 10, y - 5 + bounce), 2)
    pygame.draw.line(surf, COLOR_GREEN, (x + 25, y + 5 + bounce), (x + 30, y - 5 + bounce), 2)
    pygame.draw.circle(surf, COLOR_YELLOW, (x + 10, y - 5 + bounce), 3)
    pygame.draw.circle(surf, COLOR_YELLOW, (x + 30, y - 5 + bounce), 3)
    pygame.draw.circle(surf, COLOR_RED, (x + 15, y + 12 + bounce), 3)
    pygame.draw.circle(surf, COLOR_RED, (x + 25, y + 12 + bounce), 3)
    pygame.draw.rect(surf, COLOR_GREEN, (x + 10, y + 27 + bounce, 20, 15), border_radius=4)
    if (frame // 10) % 2 == 0:
        pygame.draw.line(surf, COLOR_GREEN, (x + 13, y + 42 + bounce), (x + 8, y + 52 + bounce), 3)
        pygame.draw.line(surf, COLOR_GREEN, (x + 27, y + 42 + bounce), (x + 32, y + 52 + bounce), 3)
    else:
        pygame.draw.line(surf, COLOR_GREEN, (x + 13, y + 42 + bounce), (x + 18, y + 52 + bounce), 3)
        pygame.draw.line(surf, COLOR_GREEN, (x + 27, y + 42 + bounce), (x + 22, y + 52 + bounce), 3)

def draw_crown(surf, x, y):
    points = [(x, y + 15), (x + 5, y), (x + 15, y + 10), (x + 25, y), (x + 35, y + 10), (x + 45, y), (x + 50, y + 15)]
    pygame.draw.polygon(surf, COLOR_YELLOW, points)
    pygame.draw.rect(surf, COLOR_ORANGE, (x, y + 15, 50, 6))

class EnergyNode:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.is_active = False

class Game:
    def __init__(self):
        self.state = STATE_MENU
        self.time_limit = 600 * 1000 
        self.start_ticks = pygame.time.get_ticks()
        self.time_remaining = self.time_limit
        
        self.classic_passed_count = 0
        self.needed_classic_jumps = 10  
        self.bombs_dodged = 0
        self.needed_bomb_dodges = 15    
        
        self.font_large = pygame.font.SysFont("Courier New", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Courier New", 22, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 16, bold=True)
        
        self.is_paused = False
        self.pause_icon_rect = pygame.Rect(SCREEN_WIDTH - 60, 20, 30, 30)
        
        btn_width, btn_height = 200, 60
        self.resume_btn_rect = pygame.Rect(
            (SCREEN_WIDTH - btn_width) // 2, 
            (SCREEN_HEIGHT - btn_height) // 2, 
            btn_width, 
            btn_height
        )
        
        self.reset_game_states()

    def reset_game_states(self):
        self.start_ticks = pygame.time.get_ticks()
        self.time_remaining = self.time_limit
        self.classic_passed_count = 0
        self.bombs_dodged = 0
        self.is_paused = False 
        
        self.dino_x = 100
        self.dino_y = 350
        self.dino_vel_y = 0
        self.is_jumping = False
        self.gravity = 0.8
        self.jump_strength = -15
        self.dino_width = 44
        self.dino_height = 44
        self.dino_frame = 0
        self.dino_frame_timer = 0
        self.dino_speed = 7
        
        self.cacti = []
        self.cactus_spawn_timer = 0
        self.game_speed = 7
        
        self.bombs = []
        self.bomb_spawn_timer = 0
        self.pulse_counter = 0
        
        self.spaceship_x = SCREEN_WIDTH + 100 
        self.spaceship_y = 300
        self.spaceship_hover = 0
        self.spaceship_ready = False
        
        self.heli_x = SCREEN_WIDTH + 100
        self.heli_y = 150
        self.heli_frame = 0
        self.dino_falling_from_ship = False
        
        self.mars_travel_distance = 0
        self.needed_mars_distance = 300
        self.space_obstacles = []
        
        self.martians = []
        self.martians_defeated = 0
        self.needed_martian_kills = 10
        self.projectiles = []
        
        self.puzzle_nodes = [
            EnergyNode((SCREEN_WIDTH // 4) - 50, 150, COLOR_RED),
            EnergyNode((SCREEN_WIDTH // 4) - 50, 300, COLOR_BLUE),
            EnergyNode((SCREEN_WIDTH // 4) - 50, 450, COLOR_YELLOW),
            EnergyNode((3 * SCREEN_WIDTH // 4) - 50, 150, COLOR_RED),
            EnergyNode((3 * SCREEN_WIDTH // 4) - 50, 300, COLOR_BLUE),
            EnergyNode((3 * SCREEN_WIDTH // 4) - 50, 450, COLOR_YELLOW)
        ]
        self.selected_node = None
        self.connections = []

    def update_timer(self):
        if self.state in [STATE_CLASSIC, STATE_WIFI_BOMB, STATE_PUZZLE, STATE_HELICOPTER, STATE_MARS_TRAVEL, STATE_MARS_BATTLE] and not self.is_paused:
            passed_time = pygame.time.get_ticks() - self.start_ticks
            self.time_remaining = max(0, self.time_limit - passed_time)
            if self.time_remaining <= 0:
                self.state = STATE_GAME_OVER

    def draw_hud(self):
        seconds = int((self.time_remaining / 1000) % 60)
        minutes = int((self.time_remaining / (1000 * 60)) % 60)
        time_str = f"SÜRE: {minutes:02d}:{seconds:02d}"
        
        timer_color = COLOR_TEXT if screen.get_at((0,0)) in [COLOR_BG, COLOR_GRAY] else COLOR_WHITE
        if minutes < 1 and pygame.time.get_ticks() % 500 < 250:
            timer_color = COLOR_RED
                
        time_text = self.font_medium.render(time_str, True, timer_color)
        screen.blit(time_text, (20, 20))
        
        status_text_str = ""
        if self.state == STATE_CLASSIC:
            status_text_str = f"Kaktüs Geç: {self.classic_passed_count}/{self.needed_classic_jumps}"
        elif self.state == STATE_WIFI_BOMB:
            status_text_str = f"Bombadan Kaç: {self.bombs_dodged}/{self.needed_bomb_dodges}"
            if self.spaceship_ready and self.spaceship_x <= (SCREEN_WIDTH // 2) - 30:
                status_text_str = "Geminin altına gel ve GEMİYE DOKUN!"
        elif self.state == STATE_PUZZLE:
            status_text_str = "Ameleliği bitir: Aynı Renkleri Birleştir!"
        elif self.state == STATE_HELICOPTER:
            status_text_str = "IŞINLANMA AKTİF: Direkt helikoptere dokun!"
        elif self.state == STATE_MARS_TRAVEL:
            status_text_str = f"Mars Yolculuğu: {int((self.mars_travel_distance/self.needed_mars_distance)*100)}% - Göktaşlarından Kaç!"
        elif self.state == STATE_MARS_BATTLE:
            status_text_str = f"Marslıları Temizle: {self.martians_defeated}/{self.needed_martian_kills} - Ateş etmek için dokun!"
            
        status_text = self.font_small.render(status_text_str, True, timer_color)
        screen.blit(status_text, (20, 55))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.state in [STATE_CLASSIC, STATE_WIFI_BOMB, STATE_PUZZLE, STATE_HELICOPTER, STATE_MARS_TRAVEL, STATE_MARS_BATTLE]:
                    if not self.is_paused and self.pause_icon_rect.collidepoint(mouse_pos):
                        self.is_paused = True
                        self.pause_start_ticks = pygame.time.get_ticks()
                        continue
                    elif self.is_paused and self.resume_btn_rect.collidepoint(mouse_pos):
                        self.is_paused = False
                        self.start_ticks += (pygame.time.get_ticks() - self.pause_start_ticks)
                        continue
                
                if self.is_paused:
                    continue 

                if self.state == STATE_MENU:
                    self.reset_game_states()
                    self.state = STATE_CLASSIC
                    
                elif self.state in [STATE_MARS_KING, STATE_GAME_OVER]:
                    self.state = STATE_MENU
                    
                elif self.state == STATE_CLASSIC:
                    if not self.is_jumping:
                        self.dino_vel_y = self.jump_strength
                        self.is_jumping = True
                        
                elif self.state == STATE_WIFI_BOMB:
                    if self.spaceship_ready and self.spaceship_x <= (SCREEN_WIDTH // 2) - 30:
                        ship_rect = pygame.Rect(self.spaceship_x - 10, self.spaceship_y - 10, 80, 50)
                        if ship_rect.collidepoint(mouse_pos):
                            if abs((self.dino_x + self.dino_width//2) - (self.spaceship_x + 30)) < 100:
                                self.state = STATE_PUZZLE
                                
                elif self.state == STATE_HELICOPTER:
                    # --- IŞINLANMA KONTROLÜ ---
                    # Helikopterin kapladığı alanı geniş bir kutu olarak algıla (tıklama kolaylığı için)
                    heli_clickable_rect = pygame.Rect(self.heli_x - 30, self.heli_y - 20, 110, 70)
                    if heli_clickable_rect.collidepoint(mouse_pos):
                        # Dokunulduğunda direkt helikopterin içine ışınla ve sahneyi değiştir!
                        self.state = STATE_MARS_TRAVEL
                        self.dino_x = SCREEN_WIDTH // 4
                        self.dino_y = SCREEN_HEIGHT // 2
                        
                elif self.state == STATE_MARS_BATTLE:
                    self.projectiles.append({
                        "x": self.dino_x + self.dino_width,
                        "y": self.dino_y + 15,
                        "vx": 12
                    })
                        
                elif self.state == STATE_PUZZLE:
                    for node in self.puzzle_nodes:
                        if node.rect.collidepoint(mouse_pos):
                            if self.selected_node is None:
                                self.selected_node = node
                            else:
                                if node != self.selected_node and node.color == self.selected_node.color:
                                    already_connected = any(node in conn or self.selected_node in conn for conn in self.connections)
                                    if not already_connected:
                                        self.connections.append((self.selected_node, node))
                                        node.is_active = True
                                        self.selected_node.is_active = True
                                self.selected_node = None

    def update(self):
        if self.is_paused:
            return 

        self.update_timer()
        self.dino_frame_timer += 1
        if self.dino_frame_timer >= 6:
            self.dino_frame = 1 - self.dino_frame
            self.dino_frame_timer = 0
            
        if self.state == STATE_CLASSIC:
            self.update_classic_mode()
        elif self.state == STATE_WIFI_BOMB:
            self.update_wifi_bomb_mode()
        elif self.state == STATE_PUZZLE:
            if len(self.connections) == 3:
                self.state = STATE_HELICOPTER
                self.dino_x = SCREEN_WIDTH // 2 - 100
                self.dino_y = 100  
                self.spaceship_x = SCREEN_WIDTH // 2 - 30
                self.spaceship_y = 80
                self.dino_falling_from_ship = True
        elif self.state == STATE_HELICOPTER:
            self.update_helicopter_mode()
        elif self.state == STATE_MARS_TRAVEL:
            self.update_mars_travel_mode()
        elif self.state == STATE_MARS_BATTLE:
            self.update_mars_battle_mode()

    def update_classic_mode(self):
        self.dino_vel_y += self.gravity
        self.dino_y += self.dino_vel_y
        if self.dino_y >= 350:
            self.dino_y = 350
            self.dino_vel_y = 0
            self.is_jumping = False
            
        self.cactus_spawn_timer += 1
        if self.cactus_spawn_timer > random.randint(70, 120):
            self.cacti.append(pygame.Rect(SCREEN_WIDTH + 50, 350, 30, 40))
            self.cactus_spawn_timer = 0
            
        for cactus in self.cacti[:]:
            cactus.x -= self.game_speed
            if cactus.x < -50:
                self.cacti.remove(cactus)
                self.classic_passed_count += 1
                
            dino_rect = pygame.Rect(self.dino_x + 5, self.dino_y, self.dino_width - 10, self.dino_height)
            if dino_rect.colliderect(cactus):
                self.state = STATE_GAME_OVER
                
        if self.classic_passed_count >= self.needed_classic_jumps:
            self.dino_x, self.dino_y = SCREEN_WIDTH // 2, 450
            self.state = STATE_WIFI_BOMB

    def update_wifi_bomb_mode(self):
        self.pulse_counter += 1
        
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]: 
            mouse_x, _ = pygame.mouse.get_pos()
            
            ship_rect = pygame.Rect(self.spaceship_x - 10, self.spaceship_y - 10, 80, 50)
            if not (self.spaceship_ready and ship_rect.collidepoint((mouse_x, _))):
                if mouse_x < SCREEN_WIDTH // 2:
                    self.dino_x -= self.dino_speed
                else:
                    self.dino_x += self.dino_speed
                
        self.dino_x = max(10, min(self.dino_x, SCREEN_WIDTH - self.dino_width - 10))
        
        self.bomb_spawn_timer += 1
        if self.bomb_spawn_timer > 25:
            bx = random.randint(20, SCREEN_WIDTH - 50)
            self.bombs.append(pygame.Rect(bx, -40, 30, 30))
            self.bomb_spawn_timer = 0
            
        for bomb in self.bombs[:]:
            bomb.y += 5
            if bomb.y > SCREEN_HEIGHT:
                self.bombs.remove(bomb)
                self.bombs_dodged += 1
                
            dino_rect = pygame.Rect(self.dino_x, self.dino_y, self.dino_width, self.dino_height)
            if dino_rect.colliderect(bomb):
                self.state = STATE_GAME_OVER
                
        if self.bombs_dodged >= self.needed_bomb_dodges:
            self.spaceship_ready = True
            
        if self.spaceship_ready:
            if self.spaceship_x > (SCREEN_WIDTH // 2) - 30:
                self.spaceship_x -= 3

    def update_helicopter_mode(self):
        self.heli_frame += 1
        if self.heli_x > SCREEN_WIDTH // 2 + 100:
            self.heli_x -= 4
            
        if self.dino_falling_from_ship:
            self.dino_y += 4
            if self.dino_y >= 450:
                self.dino_y = 450
                self.dino_falling_from_ship = False

    def update_mars_travel_mode(self):
        self.heli_frame += 1
        self.mars_travel_distance += 1
        
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            _, mouse_y = pygame.mouse.get_pos()
            if mouse_y < SCREEN_HEIGHT // 2:
                self.dino_y -= 6
            else:
                self.dino_y += 6
                
        self.dino_y = max(50, min(self.dino_y, SCREEN_HEIGHT - 100))
        
        if random.randint(1, 30) == 1:
            ox = SCREEN_WIDTH + 50
            oy = random.randint(50, SCREEN_HEIGHT - 100)
            self.space_obstacles.append(pygame.Rect(ox, oy, 25, 25))
            
        for obs in self.space_obstacles[:]:
            obs.x -= 8
            if obs.x < -50:
                self.space_obstacles.remove(obs)
                
            dino_heli_rect = pygame.Rect(self.dino_x, self.dino_y, 60, 40)
            if dino_heli_rect.colliderect(obs):
                self.state = STATE_GAME_OVER
                
        if self.mars_travel_distance >= self.needed_mars_distance:
            self.state = STATE_MARS_BATTLE
            self.dino_x = 100
            self.dino_y = 450
            self.projectiles.clear()
            self.martians.clear()

    def update_mars_battle_mode(self):
        self.heli_frame += 1
        
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x < self.dino_x:
                self.dino_x -= 5
            elif mouse_x > self.dino_x + self.dino_width:
                self.dino_x += 5
        self.dino_x = max(10, min(self.dino_x, SCREEN_WIDTH // 2))
        
        for proj in self.projectiles[:]:
            proj["x"] += proj["vx"]
            if proj["x"] > SCREEN_WIDTH:
                self.projectiles.remove(proj)
                
        if random.randint(1, 40) == 1 and len(self.martians) < 4:
            mx = SCREEN_WIDTH + 50
            my = 440
            self.martians.append(pygame.Rect(mx, my, 40, 50))
            
        for martian in self.martians[:]:
            martian.x -= 4
            if martian.x < -50:
                self.martians.remove(martian)
                
            dino_rect = pygame.Rect(self.dino_x, self.dino_y, self.dino_width, self.dino_height)
            if dino_rect.colliderect(martian):
                self.state = STATE_GAME_OVER
                
            m_rect = pygame.Rect(martian.x, martian.y, 40, 50)
            for proj in self.projectiles[:]:
                p_rect = pygame.Rect(proj["x"], proj["y"], 10, 5)
                if p_rect.colliderect(m_rect):
                    if proj in self.projectiles: self.projectiles.remove(proj)
                    if martian in self.martians: self.martians.remove(martian)
                    self.martians_defeated += 1
                    
        if self.martians_defeated >= self.needed_martian_kills:
            self.state = STATE_MARS_KING

    def draw(self):
        if self.state == STATE_MENU: self.draw_menu()
        elif self.state == STATE_CLASSIC: self.draw_classic()
        elif self.state == STATE_WIFI_BOMB: self.draw_wifi_bomb_stage()
        elif self.state == STATE_PUZZLE: self.draw_puzzle_stage()
        elif self.state == STATE_HELICOPTER: self.draw_helicopter_stage()
        elif self.state == STATE_MARS_TRAVEL: self.draw_mars_travel_stage()
        elif self.state == STATE_MARS_BATTLE: self.draw_mars_battle_stage()
        elif self.state == STATE_MARS_KING: self.draw_mars_king_stage()
        elif self.state == STATE_GAME_OVER: self.draw_game_over()
        
        if self.state in [STATE_CLASSIC, STATE_WIFI_BOMB, STATE_PUZZLE, STATE_HELICOPTER, STATE_MARS_TRAVEL, STATE_MARS_BATTLE]:
            if not self.is_paused:
                line_color = COLOR_WHITE if self.state in [STATE_PUZZLE, STATE_MARS_TRAVEL, STATE_MARS_BATTLE] else COLOR_TEXT
                pygame.draw.rect(screen, line_color, (self.pause_icon_rect.x, self.pause_icon_rect.y, 8, 30))
                pygame.draw.rect(screen, line_color, (self.pause_icon_rect.x + 16, self.pause_icon_rect.y, 8, 30))
            else:
                mouse_pos = pygame.mouse.get_pos()
                if self.resume_btn_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, COLOR_GRAY, self.resume_btn_rect, border_radius=10)
                    text_color = COLOR_DARK_BG
                else:
                    pygame.draw.rect(screen, COLOR_DARK_GRAY, self.resume_btn_rect, border_radius=10)
                    text_color = COLOR_WHITE
                    
                resume_text = self.font_medium.render("DEVAM ET", True, text_color)
                text_rect = resume_text.get_rect(center=self.resume_btn_rect.center)
                screen.blit(resume_text, text_rect)

        pygame.display.flip()

    def draw_menu(self):
        screen.fill(COLOR_BG)
        title_text = self.font_large.render("DİNO: MARS'IN KRALI", True, COLOR_TEXT)
        info_text_1 = self.font_medium.render("DÜNYADAN KAÇIŞ VE MARS'I FETHETME HİKAYESİ!", True, COLOR_RED)
        info_text_2 = self.font_small.render("Kaktüsler, bombalar, helikopterler ve Marslı savaşçılar seni bekliyor.", True, COLOR_TEXT)
        start_text = self.font_medium.render("[ BAŞLAMAK İÇİN EKRANA DOKUNUN ]", True, COLOR_BLUE)
        draw_dino(screen, (SCREEN_WIDTH // 2) - 22, 240)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 80))
        screen.blit(info_text_1, (SCREEN_WIDTH // 2 - info_text_1.get_width() // 2, 150))
        screen.blit(info_text_2, (SCREEN_WIDTH // 2 - info_text_2.get_width() // 2, 330))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 450))

    def draw_classic(self):
        screen.fill(COLOR_BG)
        pygame.draw.line(screen, COLOR_TEXT, (0, 390), (SCREEN_WIDTH, 390), 2)
        draw_dino(screen, self.dino_x, self.dino_y, self.dino_frame, self.is_jumping)
        for cactus in self.cacti: draw_cactus(screen, cactus.x, cactus.y)
        self.draw_hud()

    def draw_wifi_bomb_stage(self):
        screen.fill(COLOR_BG)
        pygame.draw.line(screen, COLOR_TEXT, (0, 490), (SCREEN_WIDTH, 490), 2)
        draw_dino(screen, self.dino_x, self.dino_y, self.dino_frame, False)
        for bomb in self.bombs: draw_wifi_bomb(screen, bomb.x, bomb.y, self.pulse_counter)
            
        if self.spaceship_ready:
            self.spaceship_hover += 1
            draw_spaceship(screen, self.spaceship_x, self.spaceship_y, self.spaceship_hover)
            if pygame.time.get_ticks() % 600 < 300:
                arrow_text = self.font_small.render("GEMİYE DOKUN VE BİN!", True, COLOR_GREEN)
                screen.blit(arrow_text, (self.spaceship_x - 40, self.spaceship_y - 30))
        
        pygame.draw.line(screen, (220, 220, 220), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 1)
        self.draw_hud()

    def draw_puzzle_stage(self):
        screen.fill(COLOR_DARK_BG)
        panel_title = self.font_large.render("KONTROL PANELİ", True, COLOR_WHITE)
        instruction = self.font_small.render("Panellere sırayla dokunarak aynı renkleri birbirine bağla!", True, COLOR_YELLOW)
        screen.blit(panel_title, (SCREEN_WIDTH // 2 - panel_title.get_width() // 2, 30))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 80))
        
        for node1, node2 in self.connections:
            pygame.draw.line(screen, node1.color, node1.rect.center, node2.rect.center, 8)
        if self.selected_node:
            pygame.draw.line(screen, self.selected_node.color, self.selected_node.rect.center, pygame.mouse.get_pos(), 4)
            
        for node in self.puzzle_nodes:
            border_color = COLOR_WHITE if node.is_active else (100, 100, 100)
            pygame.draw.rect(screen, border_color, node.rect, 4, border_radius=5)
            pygame.draw.rect(screen, node.color, node.rect.inflate(-12, -12), border_radius=3)
            if self.selected_node == node:
                pygame.draw.rect(screen, COLOR_WHITE, node.rect.inflate(8, 8), 2, border_radius=8)

        pygame.draw.rect(screen, (50, 50, 70), ((SCREEN_WIDTH // 2) - 80, 200, 160, 180), border_radius=15)
        status_color = COLOR_RED if len(self.connections) < 3 else COLOR_GREEN
        status_text = "SİSTEM: GÜÇSÜZ" if len(self.connections) < 3 else "SİSTEM: HAZIR"
        status_render = self.font_medium.render(status_text, True, status_color)
        screen.blit(status_render, (SCREEN_WIDTH // 2 - status_render.get_width() // 2, 280))
        self.draw_hud()

    def draw_helicopter_stage(self):
        screen.fill(COLOR_BG)
        pygame.draw.line(screen, COLOR_TEXT, (0, 490), (SCREEN_WIDTH, 490), 2)
        
        draw_spaceship(screen, self.spaceship_x, self.spaceship_y, self.heli_frame)
        if self.heli_frame % 10 < 5:
            pygame.draw.circle(screen, COLOR_RED, (self.spaceship_x + 30, self.spaceship_y + 15), 25)
            pygame.draw.circle(screen, COLOR_ORANGE, (self.spaceship_x + 15, self.spaceship_y + 10), 15)
            
        draw_helicopter(screen, self.heli_x, self.heli_y, self.heli_frame)
        draw_dino(screen, self.dino_x, self.dino_y, self.dino_frame, False)
        
        if not self.dino_falling_from_ship and pygame.time.get_ticks() % 600 < 300:
            jump_msg = self.font_medium.render("DİREKT HELİKOPTERE DOKUNUP IŞINLAN!", True, COLOR_RED)
            screen.blit(jump_msg, (SCREEN_WIDTH // 2 - jump_msg.get_width() // 2, 250))
            
        self.draw_hud()

    def draw_mars_travel_stage(self):
        screen.fill(COLOR_SPACE_BG)
        
        for i in range(15):
            random.seed(i * 999)
            sx = random.randint(0, SCREEN_WIDTH)
            sy = (random.randint(0, SCREEN_HEIGHT) + self.mars_travel_distance * 2) % SCREEN_HEIGHT
            pygame.draw.circle(screen, COLOR_WHITE, (sx, sy), 2)
            
        draw_helicopter(screen, self.dino_x, self.dino_y, self.heli_frame)
        draw_dino(screen, self.dino_x + 5, self.dino_y - 5, self.dino_frame, False)
        
        for obs in self.space_obstacles:
            pygame.draw.circle(screen, COLOR_GRAY, obs.center, 12)
            pygame.draw.circle(screen, COLOR_DARK_GRAY, (obs.x + 6, obs.y + 6), 4)
            
        self.draw_hud()

    def draw_mars_battle_stage(self):
        screen.fill(COLOR_MARS_BG)
        pygame.draw.line(screen, COLOR_WHITE, (0, 490), (SCREEN_WIDTH, 490), 2)
        
        draw_dino(screen, self.dino_x, self.dino_y, self.dino_frame, False)
        pygame.draw.rect(screen, COLOR_BLUE, (self.dino_x + self.dino_width - 5, self.dino_y + 15, 15, 6)) 
        
        for proj in self.projectiles:
            pygame.draw.line(screen, COLOR_YELLOW, (proj["x"], proj["y"]), (proj["x"] + 15, proj["y"]), 4)
            
        for martian in self.martians:
            draw_martian(screen, martian.x, martian.y, self.heli_frame)
            
        self.draw_hud()

    def draw_mars_king_stage(self):
        screen.fill(COLOR_MARS_BG)
        
        pygame.draw.rect(screen, COLOR_YELLOW, (SCREEN_WIDTH // 2 - 40, 380, 80, 110), border_radius=5)
        pygame.draw.rect(screen, COLOR_RED, (SCREEN_WIDTH // 2 - 25, 395, 50, 95))
        
        draw_dino(screen, SCREEN_WIDTH // 2 - 22, 360, 0, False)
        draw_crown(screen, SCREEN_WIDTH // 2 - 25, 335)
        
        draw_martian(screen, SCREEN_WIDTH // 2 - 150, 430, 20)
        draw_martian(screen, SCREEN_WIDTH // 2 + 110, 430, 40)
        
        win_title = self.font_large.render("MARS'IN TEK HAKİMİ: DİNO KRAL!", True, COLOR_YELLOW)
        score_text = self.font_medium.render("Tüm zorlukları aştın, Marslıları yendin ve tacı taktın!", True, COLOR_WHITE)
        restart_text = self.font_small.render("[ YENİDEN OYNAMAK İÇİN EKRANA DOKUNUN ]", True, COLOR_BLUE)
        
        screen.blit(win_title, (SCREEN_WIDTH // 2 - win_title.get_width() // 2, 80))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 160))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 240))

    def draw_game_over(self):
        screen.fill(COLOR_BG)
        fail_title = self.font_large.render("OYUN BİTTİ", True, COLOR_RED)
        reason = "BOMBA PATLADI! Zamanınız tükendi." if self.time_remaining <= 0 else "Dinozor görevini tamamlayamadan elendi!"
        reason_text = self.font_medium.render(reason, True, COLOR_TEXT)
        restart_text = self.font_small.render("[ BAŞTAN BAŞLAMAK İÇİN EKRANA DOKUNUN ]", True, COLOR_BLUE)
        screen.blit(fail_title, (SCREEN_WIDTH // 2 - fail_title.get_width() // 2, 150))
        screen.blit(reason_text, (SCREEN_WIDTH // 2 - reason_text.get_width() // 2, 250))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

# --- OYUNU BAŞLAT ---
if __name__ == "__main__":
    game = Game()
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)
