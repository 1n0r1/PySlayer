import sys, pygame, random

from pygame import mouse
from pygame.constants import BUTTON_LEFT, MOUSEBUTTONDOWN
from pygame.key import get_pressed

pygame.init()
size = width, height = 1366, 768
screen = pygame.display.set_mode(size)
speed = [0,0]
shooting = False
last_shoot = pygame.time.get_ticks()



class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mc.png")
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)

class Bullet(pygame.sprite.Sprite):
    facing = [0,0]
    def __init__(self, color, pos, face):
        super().__init__() 
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill(color)
        self.image.blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)
        self.rect.center = pos
        self.facing = face
    def update(self):
        self.rect = self.rect.move(self.facing)
def handle_movement():
    key = pygame.key.get_pressed()
    if (key[pygame.K_a]):
        if (speed[0] > -20):
            speed[0] -= 2
    if (key[pygame.K_d]):
        if (speed[0] < 20):
            speed[0] += 2
    if (key[pygame.K_w]):
        if (speed[1] > -20):
            speed[1] -= 2
    if (key[pygame.K_s]):
        if (speed[1] < 20):
            speed[1] += 2
    if (speed[0] > 0):
        speed[0] -= 1
    elif (speed[0] < 0):
        speed[0] += 1
    if (speed[1] > 0):
        speed[1] -= 1
    elif (speed[1] < 0):
        speed[1] += 1
    main.rect = main.rect.move(speed)

def handle_event():
    for event in pygame.event.get():
        global shooting
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shooting = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shooting = False

def shoot():
    t = pygame.time.get_ticks()
    global last_shoot
    if (t - last_shoot > 50):
        face = [0.0,0.0]
        face[0] = pygame.mouse.get_pos()[0] - main.rect.center[0]
        face[1] = pygame.mouse.get_pos()[1] - main.rect.center[1]
        f =[0.0,0.0]
        f[0] = face[0]*20 / (face[0]**2 + face[1]**2)**(1/2)
        f[1] = face[1]*20 / (face[0]**2 + face[1]**2)**(1/2)
        bullet = Bullet(pygame.Color(255,0,0,255), main.rect.center, f)
        bullet_sprites.add(bullet)
        last_shoot = pygame.time.get_ticks()

def refresh():
    screen.fill((255, 255, 255))
    main_sprite.draw(screen)
    bullet_sprites.draw(screen)
    bullet_sprites.update()
    pygame.display.flip()


main = MainCharacter()
main_sprite = pygame.sprite.Group()
main_sprite.add(main)

bullet_sprites = pygame.sprite.Group()

while 1:
    pygame.time.Clock().tick(60)

    if (shooting == True):
        shoot()
    
    refresh()
    handle_event()
    handle_movement()