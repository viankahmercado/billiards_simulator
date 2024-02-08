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
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# colors
background = (50, 50, 50)

# images path
table_image = pygame.image.load("images/table.png").convert_alpha()

# function for creating balls
def create_ball(radius, pos):
  body = pymunk.Body()
  body.position = pos
  shape = pymunk.Circle(body, radius)
  shape.mass = 5
  # to add friction use pivot joint
  pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
  pivot.max_bias = 0 # disable joint correction
  pivot.max_force = 1000 # emulate linear friction

  space.add(body, shape, pivot)
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
  
  #draw pool table
  screen.blit(table_image, (0, 0))

  
  # events handler
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      cue_ball.body.apply_impulse_at_local_point((-1500, 0),(0,0))
    if event.type == pygame.QUIT:
      run = False
      
space.debug_draw(draw_options)
pygame.display.update()
      
pygame.quit()



