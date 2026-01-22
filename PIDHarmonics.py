import pygame.key
from Graphics import *
import Robot

'''
TO LEARN:
Framework:
  Pygame
  Scrum timer app
    SNHU dates
      4+ hours DAILY
Undamped/Damped Harmonic Oscillators
PID Controllers
LRC Circuits (opamps?)
Dual pendulums (zz* = 2|z|)

'''

running = True
paused = False
step = False
keys = pygame.key.get_pressed()
holdkeys = [pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN]
hold = {_:0 for _ in holdkeys}
holdrate = 30
bots: list[Robot.Robot] = []
sel = 0

def press(key) -> bool:
  if key in holdkeys:
    return keys[key] and hold[key] % holdrate == 0
  else:
    return keys[key]

def getkeyinput(dt):
  global running
  global paused
  global step
  global keys
  global hold
  global bots
  global sel

  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      pass

  # Keep this from the tutorial for when I need to have input
  # pygame.draw.circle(screen, "red", player_pos, 40)
  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
    running = False
  if press(pygame.K_SPACE):
    paused = not paused
  
  sel          = (sel + 1 * press(pygame.K_UP) - 1 * press(pygame.K_DOWN) + len(bots)) % len(bots)
  ctrlrate, pgkeycomma = 0.01 + 0.99 * (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]), pygame.K_COMMA
  bots[sel].ix = 0.0 if press(pygame.K_z) else (bots[sel].ix + (1 * press(pygame.K_q) - 1 * press(pygame.K_a)) * ctrlrate)
  bots[sel].iv = 0.0 if press(pygame.K_x) else (bots[sel].iv + (1 * press(pygame.K_w) - 1 * press(pygame.K_s)) * ctrlrate)
  bots[sel].p  = 1.0 if press(pygame.K_c) else (bots[sel].p  + (1 * press(pygame.K_e) - 1 * press(pygame.K_d)) * ctrlrate)
  bots[sel].i  = 0.0 if press(pygame.K_v) else (bots[sel].i  + (1 * press(pygame.K_r) - 1 * press(pygame.K_f)) * ctrlrate)
  bots[sel].d  = 0.0 if press(pygame.K_b) else (bots[sel].d  + (1 * press(pygame.K_t) - 1 * press(pygame.K_g)) * ctrlrate)
  bots[sel].m  = 1000.0 if press(pygame.K_n) else max((bots[sel].m  + (1 * press(pygame.K_y) - 1 * press(pygame.K_h)) * ctrlrate), 0.01)
  bots[sel].mu = 0.0 if press(pygame.K_m) else (bots[sel].mu + (1 * press(pygame.K_u) - 1 * press(pygame.K_j)) * ctrlrate)
  bots[sel].mf = 0.0 if press(pgkeycomma) else (bots[sel].mf + (1 * press(pygame.K_i) - 1 * press(pygame.K_k)) * ctrlrate)

  for key in holdkeys:
    hold[key] = 0 if not keys[key] else hold[key] + 1
  return None

def drawrobot(self: Robot.Robot, sp):
  dat = [self.x, self.v, self.f, self.g]
  l = range(len(dat))
  pts = [[] for _ in dat]
  for t in range(sx):
    for i in l:
      x, y = xy2s(t / skl, dat[i][t], sp)
      pts[i].append((x, y))
  for i in l:
    pygame.draw.lines(screen, self.c[i], False, pts[i])
  return None

def fmttime(t):
  h = int(t // 36000) % 24
  m = int(t // 60) % 60
  s = t % 60
  return f"{h:02}:{m:02}:{s:07.4f}"

def drawhud(clock):
  if not running:
    text("Goodbye", 10, 10, (255, 0, 0))
  elif paused:
    text("Waiting", 10, 10, (255, 255, 0))
  else:
    text(str(f"{clock.get_fps():05.2f} fps"), 10, 10, "green")
  text(str(fmttime(sp)), 110, 10, "gray")
  text("ix : Q / A, iv : W / S, p : E / D, i : R / F, d : T / G, m : Y / H, mu : U / J, mf : I / K", 320, 10, "white")
  for bot in bots:
    c = "green" if bot.id == sel else "gray"
    y = 30 + 20 * bot.id
    text(f"Bot {bot.id}", 10, y, c)
    text("Pos", 80, y, bot.c[0])
    text("Vel", 130, y, bot.c[1])
    text("Force", 180, y, bot.c[2])
    text("Goal", 250, y, bot.c[3])
    text(bot.info(), 320, y, c)

def main():
  global bots
  global sel
  clock = pygame.time.Clock()
  dt = 0
  sp = 0
  i = (0.00, 0.01, 0.10, 0.00, 0.00, 1000.00, 0.00, 0.01)
  #i = (0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 0.00, 0.01)
  bots.append(Robot.Robot(0, i, sx, ["Red", "Yellow", "Green", "RoyalBlue"], "PID"))
  bots.append(Robot.Robot(1, i, sx, ["Red", "Yellow", "Green", "RoyalBlue"], "PID"))
  # bots[0].mu = 0.85

  # player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

  while running:
    # Main loop
    if not paused:
      #sp += dt
      drawgrid(sp)
      #drawsin(sp)
      for bot in bots:
        drawrobot(bot, sp)
    getkeyinput(dt)
    drawhud(clock)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

  pygame.quit()  
  return None

main()