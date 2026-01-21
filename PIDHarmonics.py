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
hold = None
bots = []

def getkeyinput(dt):
  global running
  global paused
  global step
  global hold
  global bots

  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Keep this from the tutorial for when I need to have input
  # pygame.draw.circle(screen, "red", player_pos, 40)
  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
    running = False
  if keys[pygame.K_w]:
    bots[0].ix -= 0.25
  if keys[pygame.K_s]:
    bots[0].ix += 0.25
  if keys[pygame.K_a]:
    bots[0].iv -= 0.25
  if keys[pygame.K_d]:
    bots[0].iv += 0.25
  if keys[pygame.K_UP]:
    bots[0].ix -= 0.25
  if keys[pygame.K_DOWN]:
    bots[0].ix += 0.25
  if keys[pygame.K_LEFT]:
    bots[0].iv -= 0.25
  if keys[pygame.K_RIGHT]:
    bots[0].iv += 0.25
  if keys[pygame.K_SPACE] and not hold[pygame.K_SPACE]:
    paused = not paused
  # Todo: Only PID() on parameter change
  hold = keys
  return None

def drawrobot(self: Robot.Robot, sp):
  pts = []
  steady = False
  mode = 1
  # self.__init__()
  self.pid()
  for t in range(sx):
    if steady:
      mode += 1
      steady = not steady
    x, y = xy2s(t / skl, self.x[t], sp)
    pts.append((x, y))
  pygame.draw.lines(screen, self.c, False, pts)
  return None

def fmttime(t):
  h = int(t // 36000) % 24
  m = int(t // 60) % 60
  s = t % 60
  return f"{h:02}:{m:02}:{s:07.4f}"

def main():
  global bots
  clock = pygame.time.Clock()
  dt = 0
  sp = 0
  bots.append(Robot.Robot(1, 0, sx))
  bots[0].mu = 0.85
  bots[0].feq = bots[0].feq_spring

  # player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

  while running:
    # Main loop
    if not paused:
      #sp += dt
      drawgrid(sp)
      drawsin(sp)
      for bot in bots:
        drawrobot(bot, sp)
    getkeyinput(dt)

    # Run once
    #running = False

    if not running:
      text("Goodbye", 10, 10, (255, 0, 0))
    elif paused:
      text("Waiting", 10, 10, (255, 255, 0))
    else:
      text(str(f"{clock.get_fps():05.2f} fps"), 10, 10, (0, 255, 0))
    text(str(fmttime(sp)), 10, 30, (0, 255, 0))
    text(bots[0].info(), 10, 50, (0, 255, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

  pygame.quit()  
  return None

main()