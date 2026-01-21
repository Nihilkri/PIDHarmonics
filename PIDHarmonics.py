import numpy as np
import pygame as pg
import matplotlib as plt

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

def sinplot():
  x = np.linspace(0, 0.01, 10)
  y = np.sin(x)
  plt.plot()
  
def pid(goal):
  pass
  
def robot():
  steady = False
  mode = 0
  for t in range(100):
    if steady:
      mode += 1
      steady = not steady
    pid(100 * mode)