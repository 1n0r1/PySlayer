import sys, pygame, random, math

from pygame import mouse
from pygame.constants import BUTTON_LEFT, MOUSEBUTTONDOWN
from pygame.key import get_pressed

pygame.init()
size = width, height = 1366, 768
screen = pygame.display.set_mode(size)
speed = [0,0]
shooting = False
last_shoot = pygame.time.get_ticks()
last_slash = pygame.time.get_ticks()

main_sprite = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
sword_sprite = pygame.sprite.Group()

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mc.png")
        self.rect = self.image.get_rect()

        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill((0,0,0))
        self.image.blit(colorImage, (0,0))

        self.rect.center = (683,384)

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
        for e in enemy_sprites:
            if (self.rect.colliderect(e.rect)):
                e.hit(1)
                self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__() 
        self.image = pygame.image.load("wall.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Enemy1(pygame.sprite.Sprite):
    health = 0
    last_hit = 0
    def __init__(self, pos):
        self.health = 10
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mc.png")
        self.rect = self.image.get_rect()
        
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill((150,150,150))
        self.image.blit(colorImage, (0,0))

        self.rect.center = pos
    def update(self):
        a = main.rect.center[0] - self.rect.center[0]
        b = main.rect.center[1] - self.rect.center[1]
        
        if ((a**2 + b**2) != 0):
            aa = a*3 / (a**2 + b**2)**(1/2)
            bb = b*3 / (a**2 + b**2)**(1/2)

            inc = 0.0
            if (aa > 0):
                inc = 1
            if (aa < 0):
                inc = -1
            for i in range(abs(int(aa))):
                prepos = self.rect.center
                self.rect = self.rect.move([inc,0])
                for wall in wall_sprites:
                    if (self.rect.colliderect(wall.rect)):
                        self.rect.center = prepos

            inc = 0.0
            if (bb > 0):
                inc = 1
            if (bb < 0):
                inc = -1
            for i in range(abs(int(bb))):
                prepos = self.rect.center
                self.rect = self.rect.move([0,inc])
                for wall in wall_sprites:
                    if (self.rect.colliderect(wall.rect)):
                        self.rect.center = prepos
            t = pygame.time.get_ticks()
            if (t - self.last_hit >= 50):
                colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
                colorImage.fill((150,150,150))
                self.image.blit(colorImage, (0,0))

    def hit(self, a):
        self.last_hit = pygame.time.get_ticks()
        self.health -= a
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill((255,0,0))
        self.image.blit(colorImage, (0,0))
        if (self.health <= 0):
            self.kill()

class Sword(pygame.sprite.Sprite):
    original_image = pygame.image.load("Sword.png")
    original_image = pygame.transform.scale(original_image,[25,100])
    original_rect = original_image.get_rect()
    angle = 0.0
    end_angle = 0.0
    def __init__(self, pos, a):
        super().__init__() 
        self.surf = self.original_image
        self.rect = self.surf.get_rect()

        colorImage = pygame.Surface(self.surf.get_size()).convert_alpha()
        colorImage.fill((0,0,0))
        self.surf.blit(colorImage, (0,0), special_flags = pygame.BLEND_MULT)
        self.angle = a
        self.rect.center = pos
        self.original_rect.center = pos
        self.end_angle = a + 160
    def update(self, pos):
        self.angle += 10
        self.surf, self.rect = rot_center(self.original_image, self.original_rect, self.angle - 90)
        self.rect.center = [pos[0] + 50.00*math.cos(self.angle/180*math.pi), pos[1] + 50.00*math.sin(-self.angle/180*math.pi)]
        if (self.angle >= self.end_angle):
            self.kill()

def handle_movement():
    key = pygame.key.get_pressed()
    if (key[pygame.K_a]):
        if (speed[0] > -10):
            speed[0] -= 1.5
    if (key[pygame.K_d]):
        if (speed[0] < 10):
            speed[0] += 1.5
    if (key[pygame.K_w]):
        if (speed[1] > -10):
            speed[1] -= 1.5
    if (key[pygame.K_s]):
        if (speed[1] < 10):
            speed[1] += 1.5
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

def slash():
    t = pygame.time.get_ticks()
    global last_slash
    if (t - last_slash > 500):
        k = 0.0
        if (pygame.mouse.get_pos()[0] - main.rect.center[0] != 0):
            k =- math.atan2(pygame.mouse.get_pos()[1] - main.rect.center[1], pygame.mouse.get_pos()[0] - main.rect.center[0])/math.pi*180
        k = k - 80
        s = Sword(main.rect.center, k)
        sword_sprite.add(s)
        last_slash = pygame.time.get_ticks()

def handle_event():
    for event in pygame.event.get():
        global shooting
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shooting = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shooting = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            slash()

def shoot():
    t = pygame.time.get_ticks()
    global last_shoot
    if (t - last_shoot > 200):
        face = [0.0,0.0]
        face[0] = pygame.mouse.get_pos()[0] - main.rect.center[0]
        face[1] = pygame.mouse.get_pos()[1] - main.rect.center[1]
        if ((face[0]**2 + face[1]**2) != 0):
            f =[0.0,0.0]
            f[0] = face[0]*20 / (face[0]**2 + face[1]**2)**(1/2)
            f[1] = face[1]*20 / (face[0]**2 + face[1]**2)**(1/2)
            bullet = Bullet(pygame.Color(0,0,0,255), main.rect.center, f)
            bullet_sprites.add(bullet)
            last_shoot = pygame.time.get_ticks()

def refresh():
    screen.fill((255, 255, 255))
    d1 = 683 - main.rect.center[0] 
    d2 = 384 - main.rect.center[1] 
    d1 /= 4
    d2/= 4

    for bullet in bullet_sprites:
        bullet.rect = bullet.rect.move(d1,d2)
    for wall in wall_sprites:
        wall.rect = wall.rect.move(d1,d2)
    for e in enemy_sprites:
        e.rect = e.rect.move(d1,d2)
    for s in sword_sprite:
        s.rect = s.rect.move(d1,d2)

    main.rect = main.rect.move(d1,d2)

    bullet_sprites.draw(screen)
    wall_sprites.draw(screen)
    
    for s in sword_sprite:
        screen.blit(s.surf, s.rect)
    main_sprite.draw(screen)
    enemy_sprites.draw(screen)
    pygame.display.flip()

def generate_room(a,b,c,d):
    for i in range(a, c+1):
        w = Wall([i*50,b*50])
        wall_sprites.add(w)
    for i in range(a, c+1):
        w = Wall([i*50,d*50])
        wall_sprites.add(w)
    for i in range(b, d+1):
        w = Wall([a*50,i*50])
        wall_sprites.add(w)
    for i in range(b, d+1):
        w = Wall([c*50,i*50])
        wall_sprites.add(w)

main = MainCharacter()
main_sprite.add(main)

generate_room(0,0,25,25)

e1 = Enemy1([300,300])
enemy_sprites.add(e1)

e2 = Enemy1([500,500])
enemy_sprites.add(e2)

while 1:
    pygame.time.Clock().tick(120)

    if (shooting == True):
        shoot()
    
    refresh()
    handle_event()
    handle_movement()
    bullet_sprites.update()
    enemy_sprites.update()
    sword_sprite.update(main.rect.center)