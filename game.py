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

main_sprite = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()


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
        for wall in wall_sprites:
            if (self.rect.colliderect(wall.rect)):
                self.kill()

class Wall(pygame.sprite.Sprite):
    facing = [0,0]
    def __init__(self, pos):
        super().__init__() 
        self.image = pygame.image.load("wall.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mc.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300,300)

def handle_movement():
    key = pygame.key.get_pressed()
    if (key[pygame.K_a]):
        if (speed[0] > -10):
            speed[0] -= 1
    if (key[pygame.K_d]):
        if (speed[0] < 10):
            speed[0] += 1
    if (key[pygame.K_w]):
        if (speed[1] > -10):
            speed[1] -= 1
    if (key[pygame.K_s]):
        if (speed[1] < 10):
            speed[1] += 1
    if (speed[0] > 0):
        speed[0] -= 0.5
    elif (speed[0] < 0):
        speed[0] += 0.5
    if (speed[1] > 0):
        speed[1] -= 0.5
    elif (speed[1] < 0):
        speed[1] += 0.5
    
    inc = 0.0
    if (speed[0] > 0):
        inc = 1
    if (speed[0] < 0):
        inc = -1
    for i in range(abs(int(speed[0]))):
        prepos = main.rect.center
        main.rect = main.rect.move([inc,0])
        for wall in wall_sprites:
            if (main.rect.colliderect(wall.rect)):
                main.rect.center = prepos

    inc = 0.0
    if (speed[1] > 0):
        inc = 1
    if (speed[1] < 0):
        inc = -1
    for i in range(abs(int(speed[1]))):
        prepos = main.rect.center
        main.rect = main.rect.move([0,inc])
        for wall in wall_sprites:
            if (main.rect.colliderect(wall.rect)):
                main.rect.center = prepos

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
    if (t - last_shoot > 100):
        face = [0.0,0.0]
        face[0] = pygame.mouse.get_pos()[0] - main.rect.center[0]
        face[1] = pygame.mouse.get_pos()[1] - main.rect.center[1]
        if ((face[0]**2 + face[1]**2) != 0):
            f =[0.0,0.0]
            f[0] = face[0]*20 / (face[0]**2 + face[1]**2)**(1/2)
            f[1] = face[1]*20 / (face[0]**2 + face[1]**2)**(1/2)
            bullet = Bullet(pygame.Color(255,0,0,255), main.rect.center, f)
            bullet_sprites.add(bullet)
            last_shoot = pygame.time.get_ticks()

def refresh():
    screen.fill((255, 255, 255))
    bullet_sprites.draw(screen)
    wall_sprites.draw(screen)
    main_sprite.draw(screen)
    pygame.display.flip()



main = MainCharacter()
main_sprite.add(main)

w1 = Wall([400,400])
w2 = Wall([450,400])
wall_sprites.add(w1)
wall_sprites.add(w2)

while 1:
    pygame.time.Clock().tick(120)

    if (shooting == True):
        shoot()
    
    refresh()
    handle_event()
    handle_movement()
    bullet_sprites.update()