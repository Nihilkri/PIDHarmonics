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
holdkeys = [pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_BACKQUOTE, pygame.K_BACKSPACE, 
            pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, 
            pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS]
hold = {_:0 for _ in holdkeys}
holdrate = 30
bots: list[Robot.Robot] = []
sel = 0
mouseinfo = ""
omx, omy = 0, 0

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
  global mouseinfo
  global omx, omy

  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      pass
    elif event.type == pygame.MOUSEBUTTONUP:
      bots[sel].sim()

  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
    running = False
  if press(pygame.K_SPACE):
    paused = not paused

  mx, my, mb = *pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)
  sel = (sel + 1 * press(pygame.K_UP) - 1 * press(pygame.K_DOWN) + len(bots)) % len(bots)
  klen = len(bots[sel].linevis)
  for k in range(klen):
    if press(holdkeys[k - klen]) or press(pygame.K_BACKQUOTE):
      bots[sel].linevis[k] = not bots[sel].linevis[k]
  if press(pygame.K_BACKSPACE) and not mb[0]:
    bots[sel].goal()
    bots[sel].sim()

  
  ctrlrate, pgkeycomma, pgkeyperid = 0.25 * dt, pygame.K_COMMA, pygame.K_PERIOD
  ctrlrate *= 100 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 1.0
  ctrlrate *= 0.01 if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) else 1.0
  bots[sel].ix = 0.0 if press(pygame.K_z) else (bots[sel].ix + (1 * press(pygame.K_q) - 1 * press(pygame.K_a)) * ctrlrate)
  bots[sel].iv = 0.0 if press(pygame.K_x) else (bots[sel].iv + (1 * press(pygame.K_w) - 1 * press(pygame.K_s)) * ctrlrate)
  bots[sel].p  = 0.0 if press(pygame.K_c) else (bots[sel].p  + (1 * press(pygame.K_e) - 1 * press(pygame.K_d)) * ctrlrate)
  bots[sel].i  = 0.0 if press(pygame.K_v) else (bots[sel].i  + (1 * press(pygame.K_r) - 1 * press(pygame.K_f)) * ctrlrate)
  bots[sel].d  = 0.0 if press(pygame.K_b) else (bots[sel].d  + (1 * press(pygame.K_t) - 1 * press(pygame.K_g)) * ctrlrate)
  bots[sel].k  = 1.0 if press(pygame.K_n) else (bots[sel].k  + (1 * press(pygame.K_y) - 1 * press(pygame.K_h)) * ctrlrate)
  bots[sel].m  = 1.0 if press(pygame.K_m) else (bots[sel].m  + (1 * press(pygame.K_u) - 1 * press(pygame.K_j)) * ctrlrate)
  bots[sel].mu = 0.0 if press(pgkeycomma) else (bots[sel].mu + (1 * press(pygame.K_i) - 1 * press(pygame.K_k)) * ctrlrate)
  bots[sel].mf = 1.0 if press(pgkeyperid) else (bots[sel].mf + (1 * press(pygame.K_o) - 1 * press(pygame.K_l)) * ctrlrate)

  for key in holdkeys:
    hold[key] = 0 if not keys[key] else hold[key] + 1

  if mb[0]:
    mx = 0 if mx < 0 else sx if mx > sx else mx
    my = 0 if my < 0 else sy if my > sy else my
    dx, dy = mx - omx, my - omy
    for t in range(0, dx, 1 if dx > 0 else -1):
      x = omx + t
      y = omy + t * dy / dx
      y = s2xy(x, y, 0)[1] 
      bots[sel].g[x] = y
  omx, omy = mx, my

  mouseinfo = "ix: Q / A        iv: W / S           p: E / D      i: R / F      d: T / G     "
  mouseinfo += "k: Y / H      m: U / J         mu: I / K       mf: O / L       "
  mouseinfo += f"Mouse at {mx:4n}, {my:4n}: FFT = {bots[sel].fftr[mx]:09.4f} + {bots[sel].ffti[mx]:09.4f}j"
  return None

def drawrobot(self: Robot.Robot, sp):
  dat = [self.g, self.e, self.x, self.v, self.f, self.fp, self.fi, self.fd, self.fk, self.fftr, self.ffti]
  l, tr = range(len(dat)), range(sx)
  pts = [[0 for t in tr] for _ in dat]
  for t in tr:
    cx, cy = xy2s(t / skl, 0, sp)
    for i in l:
      if i == 2 or self.linevis[i]:
        x, y = xy2s(t / skl, dat[i][t], sp)
        pts[i][t] = (x, y)
    if self.linevis[-1]:
      if self.atgoal[t] and self.overshooting[t]:
        pygame.draw.line(screen, (0,0,64), (cx, cy), pts[2][t])
      elif self.atgoal[t]:
        pygame.draw.line(screen, (0,64,0), (cx, cy), pts[2][t])
      elif self.overshooting[t]:
        pygame.draw.line(screen, (64,0,0), (cx, cy), pts[2][t])
  for i in l:
    if self.linevis[i]:
      pygame.draw.lines(screen, self.c[i], False, pts[i], 2)
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
  text(mouseinfo, 800, 10, "gray")
  for bot in bots:
    c = "green" if bot.id == sel else "gray"
    y = 30 + 40 * bot.id
    text(f"Bot {bot.id}", 10, y, c)
    btxt = ["Goal", "Error", "Pos", "Vel", "Force", "F(p)", "F(i)", "F(d)", "F(k)", "FFTr", "FFTi"]
    for i, txt in enumerate(btxt):
      text(txt, 80 + 60 * i, y, bot.c[i] if bot.linevis[i] else "gray")
    text(bot.info, 800, y + 00, c)
    text(f"Bot {bot.id}", 10, y + 20, c)
    text(bot.stats, 80, y + 20, c)

def main():
  global bots
  global sel
  clock = pygame.time.Clock()
  dt = 0
  sp = 0
  i = (1.0 / skl, 0.000, 1.000, 1.000, 0.000, 0.000, 0.000, 1.000, 0.000, 1.000)
  c = ["RoyalBlue", "Blue", "Red", "Yellow", "Green", "Green", "Green", "Green", "Green", "Violet", "Orange"]
  #def goal(self, t):
  #  return np.sin(t / 100.0)
  bots.append(Robot.Robot(0, i, sx, c))
  bots.append(Robot.Robot(1, i, sx, c))
  # bots[0].mu = 0.85
  #bots[0].goal = goal

  # player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

  while running:
    # Main loop
    if not paused:
      #sp += dt
      drawgrid(sp)
      #drawsin(sp)
      for bot in bots:
        drawrobot(bot, sp)
      #showcolors()
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