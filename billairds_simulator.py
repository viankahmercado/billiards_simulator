"""
Final Project:
# Create an exciting python program. Find an existing python project on YouTube that piques your interest. 
# Make that program from scratch, with a demo afterwards. 
# Push the code to your GitHub account, then put the youTube link to give credit.
"""

import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

# screen height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678

# game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Billards Simulator")

# pymunk space
space = pymunk.Space()
space.gravity = (0, 5000)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# colors
background = (50, 50, 50)

# function for creating balls
def create_ball(radius, pos):
  body = pymunk.Body()
  body.position = pos
  shape = pymunk.Circle(body, radius)
  shape.mass = 5

  space.add(body, shape)
  return shape 

new_ball = create_ball(25, (300, 100))

cue_ball = create_ball(25, (300, 310))

# create game loop
run = True
while run:
  
  clock.tick(FPS)
  space.step(1 / FPS)
  
  # color fill background
  screen.fill(background)
  
  # events handler
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      cue_ball.body.apply_impulse_at_local_point((-1500, 0),(0,0))
    if event.type == pygame.QUIT:
      run = False
      
space.debug_draw(draw_options)
pygame.display.update()
      
pygame.quit()



