import numpy as np
import pygame

# Constants
#sx, sy, skl, sp = 1280, 720, 100.0, 0.0
sx, sy, skl, sp = 3840, 720, 100.0, 0.0
hsx, hsy = sx // 2, sy // 2
# pygame setup
pygame.init()
screen = pygame.display.set_mode((sx, sy))
font = pygame.font.Font(None, 32)
  
def text(txt: str, x: int, y: int, c: tuple, bg : tuple | None = "Black"):
  pygame.Surface.blit(screen, font.render(txt, True, c, bg), (x, y))
  return None

def xy2s(x, y, sp):
  return (x - sp) * skl, hsy - y * skl
def s2xy(x, y, sp):
  return (x + sp) / skl, (-y + hsy) / skl

def drawgrid(sp):
  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")
  for i in range((int)(sp), (int)(sx // skl + sp + 2)):
    x, y = xy2s(i, 0, sp)
    pygame.draw.line(screen, "gray", (x, 0), (x, sy))
    text(str(i), x + 10, hsy + 10, (64, 64, 64))
  for i in range((int)(-hsy // skl), (int)(hsy // skl + 1)):
    x, y = xy2s(0, i, sp)
    pygame.draw.line(screen, "gray", (0, y), (sx, y))
    text(str(i), 10, y + 10, (64, 64, 64))
  pygame.draw.line(screen, "white", (0, hsy), (sx, hsy))
  return None

def drawsin(sp):
  pts = []
  for t in range(sx):
    x, y = xy2s(t / skl, np.sin(t / skl), sp)
    pts.append((x, y))
  pygame.draw.lines(screen, "blue", False, pts)
  #print(pts[0:20])
  return None

