import sys
import pygame

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino: Moon Operation - Python Edition")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (11, 15, 26)
GRID_COLOR = (31, 42, 68)
PLAYER_COLOR = (76, 175, 80)
OBSTACLE_COLOR = (141, 110, 99)
TEXT_COLOR = (183, 208, 240)

# Game States
STATE_STAGE1 = 1
STATE_STAGE2 = 2
current_stage = STATE_STAGE1

# Player
player_x, player_y = 80, 380
player_w, player_y_size = 28, 32
player_vy = 0
on_ground = True
score = 0
god_mode = False
super_laser = False

obstacles = []
frame_count = 0

running = True
while running:
  screen.fill(BG_COLOR)
  frame_count += 1

  # Retro Grid lines
  for x in range(0, WIDTH, 40):
    pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
  for y in range(0, HEIGHT, 40):
    pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)

  # Event Handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_c:
        cheat = input("Enter cheat code: ")
        if cheat in ["30", "ölü30", "afşdvçypc"]:
          god_mode = not god_mode
          print("God Mode:", god_mode)
        elif cheat in ["50", "ateş50"]:
          super_laser = not super_laser
          print("Super Laser:", super_laser)

  keys = pygame.key.get_pressed()

  # Stage 1 Logic
  if current_stage == STATE_STAGE1:
    if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]) and on_ground:
      player_vy = -9
      on_ground = False

    player_vy += 0.5
    player_y += player_vy
    if player_y >= 380:
      player_y = 380
      player_vy = 0
      on_ground = True

    # Obstacles spawning
    if frame_count % 70 == 0:
      obstacles.append(
          pygame.Rect(WIDTH, 380, 18, 28)
      )  # Python Rect for physics

    for obs in obstacles[:]:
      obs.x -= 4
      if obs.x < -30:
        obstacles.remove(obs)
        score += 10

      player_rect = pygame.Rect(player_x, player_y, player_w, player_y_size)
      if not god_mode and player_rect.colliderect(obs):
        print("Game Over! Restarting stage...")
        player_y = 380
        obstacles.clear()

      pygame.draw.rect(screen, OBSTACLE_COLOR, obs)

  # Draw Player
  pygame.draw.rect(
      screen, PLAYER_COLOR, (player_x, player_y, player_w, player_y_size)
  )

  # HUD Display
  font = pygame.font.SysFont(None, 24)
  score_text = font.render(f"🏆 Score: {score} | STAGE 1", True, TEXT_COLOR)
  screen.blit(score_text, (16, 16))

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()
