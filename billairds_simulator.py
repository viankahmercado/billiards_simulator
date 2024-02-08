"""
Final Project:
# Create an exciting python program. Find an existing python project on YouTube that piques your interest. 
# Make that program from scratch, with a demo afterwards. 
# Push the code to your GitHub account, then put the youTube link to give credit.
"""

import pygame
import pymunk
import pymunk.pygame_util
import math

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

#game variables
diameter = 36
force = 0
max_force = 10000
force_direction = 1
taking_shot = True
powering_up = False


# colors
background = (50, 50, 50)

# images path
cue_image = pygame.image.load("images/cue.png").convert_alpha()
table_image = pygame.image.load("images/table.png").convert_alpha()
ball_images = []
for i in range(1, 17):
  ball_image = pygame.image.load(f"images/ball_{i}.png").convert_alpha()
  ball_images.append(ball_image)

# function for creating balls
def create_ball(radius, pos):
  body = pymunk.Body()
  body.position = pos
  shape = pymunk.Circle(body, radius)
  shape.mass = 5
  shape.elasticity = 0.8
  # to add friction use pivot joint
  pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
  pivot.max_bias = 0 # disable joint correction
  pivot.max_force = 1000 # emulate linear friction

  space.add(body, shape, pivot)
  return shape 

# set up position of the balls
balls = []
rows = 5
# potting balls
for col in range(5):
  for row in range(rows):
    pos = (250 + (col * (diameter + 1)), 267 + (row * (diameter + 1)) + (col * diameter / 2))
    new_ball = create_ball(diameter / 2, pos)
    balls.append(new_ball)
  rows -= 1

  
new_ball = create_ball(25, (300, 100))

cue_ball = create_ball(25, (300, 310))

# corner coordinates of each cushions
cushions = [
  [(88, 56), (109, 77), (555, 77), (564, 56)],
  [(621, 56), (630, 77), (1081, 77), (1102, 56)],
  [(89, 621), (110, 600),(556, 600), (564, 621)],
  [(622, 621), (630, 600), (1081, 600), (1102, 621)],
  [(56, 96), (77, 117), (77, 560), (56, 581)],
  [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

#function for creating cushions
def create_cushion(poly_dims):
  body = pymunk.Body(body_type = pymunk.Body.STATIC)
  body.position = ((0, 0))
  shape = pymunk.Poly(body, poly_dims)
  shape.elasticity = 0.8
  
  space.add(body, shape)

for c in cushions:
  create_cushion(c)

#create pool cue
class Cue():
  def __init__(self, pos):
    self.original_image = cue_image
    self.angle = 0
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = pos

  def update(self, angle):
    self.angle = angle

  def draw(self, surface):
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    surface.blit(self.image,
      (self.rect.centerx - self.image.get_width() / 2,
      self.rect.centery - self.image.get_height() / 2)
)

cue = Cue(balls[-1].body.position)

# create game loop
run = True
while run:
  
  clock.tick(FPS)
  space.step(1 / FPS)
  
  # color fill background
  screen.fill(background)
  
  #draw pool table
  screen.blit(table_image, (0, 0))

  #draw pool balls
  for i, ball in enumerate(balls):
    screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

  #check if all the balls have stopped moving
  taking_shot = True
  for ball in balls:
    if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
      taking_shot = False

  #draw pool cue
  if taking_shot == True:

  #calculate pool cue angle
    mouse_pos = pygame.mouse.get_pos()
    cue.rect.center = balls[-1].body.position
    x_dist = balls[-1].body.position[0] - mouse_pos[0]
    y_dist = -(balls[-1].body.position[1] - mouse_pos[1]) # -ve because pygame y coordinates increase down the screen
    cue_angle = math.degrees(math.atan2(y_dist, x_dist))
    cue.update(cue_angle)
    cue.draw(screen)

# power up pool cue
if powering_up == True:
    force += 100 * force_direction
    if force >= max_force or force <= 0:
      force_direction *= -1
    print(force)
elif powering_up == False and taking_shot == True:
    x_impulse = math.cos(math.radians(cue_angle))
    y_impulse = math.sin(math.radians(cue_angle))
    balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse))
    force = 0
    force_direction = 1
  
# events handler
for event in pygame.event.get():
  if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
      powering_up = True
  if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
      powering_up = False
  if event.type == pygame.QUIT:
      run = False
      
space.debug_draw(draw_options)
pygame.display.update()
      
pygame.quit()



