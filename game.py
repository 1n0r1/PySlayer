import sys, pygame, random, math
from pprint import pprint
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

map = [["0" for i in range(9)] for i in range(9)]
islands = [[0 for i in range(9)] for i in range(9)]
paths = []
room_sprites = [[pygame.sprite.Group() for i in range(9)] for i in range(9)]
visited = [[0 for i in range(9)] for i in range(9)]
camera = [0.0000,0.000]

def rot_center(image, rect, angle):
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

        self.rect.center = (5500,5500)

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
        self.type = "wall"

    def displace_teleport(self,a,b):
        self.rect = self.rect.move([a,b])

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
        self.type = "enemy"
    
    def move(self, aa, bb):

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
            for e in enemy_sprites:
                if (e != self and self.rect.colliderect(e.rect)):
                    self.rect.center = prepos
                    e.move(inc,0)
            if (self.rect.colliderect(main.rect)):
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
            for e in enemy_sprites:
                if (e != self and self.rect.colliderect(e.rect)):
                    self.rect.center = prepos
                    e.move(0,inc)
            if (self.rect.colliderect(main.rect)):
                self.rect.center = prepos
    
    def update(self):
        a = main.rect.center[0] - self.rect.center[0]
        b = main.rect.center[1] - self.rect.center[1]
        
        if ((a**2 + b**2) != 0):
            aa = a*3 / (a**2 + b**2)**(1/2)
            bb = b*3 / (a**2 + b**2)**(1/2)
            self.move(aa,bb)

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

    def displace_teleport(self,a,b):
        self.rect = self.rect.move([a,b])

class Pathh:
    def __init__(self,a,b,c,d):
        self.x1 = a
        self.y1 = b
        self.x2 = c
        self.y2 = d
    def get(self):
        return [self.x1,self.y1,self.x2,self.y2]

def slash():
    t = pygame.time.get_ticks()
    global last_slash
    if (t - last_slash > 500):
        k = 0.0
        angle = -math.atan2(pygame.mouse.get_pos()[1] - main.rect.center[1], pygame.mouse.get_pos()[0] - main.rect.center[0])/math.pi*180
        if (pygame.mouse.get_pos()[0] - main.rect.center[0] != 0):
            k = angle
        k = k - 80
        s = Sword(main.rect.center, k)
        sword_sprite.add(s)
        last_slash = pygame.time.get_ticks()
        for e in enemy_sprites:
            dis = [e.rect.center[1] - main.rect.center[1], e.rect.center[0] - main.rect.center[0]]
            angle_enemy = -math.atan2(dis[0], dis[1])/math.pi*180
            dist = (dis[0]**2 + dis[1]**2)**(1/2)
            if abs(angle_enemy -80 - k ) <80 and dist<150:
                e.hit(3)
                
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
        for e in enemy_sprites:
            if (main.rect.colliderect(e.rect)):
                main.rect.center = prepos
                e.move(speed[0],0)

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
        for e in enemy_sprites:
            if (main.rect.colliderect(e.rect)):
                main.rect.center = prepos
                e.move(0,speed[1])

def refresh():
    screen.fill((255, 255, 255))
    d1 = 683 - main.rect.center[0] 
    d2 = 384 - main.rect.center[1] 
    d1 = int(d1/5)
    d2 = int(d2/5)

    for bullet in bullet_sprites:
        bullet.rect = bullet.rect.move(d1,d2)
    for wall in wall_sprites:
        wall.rect = wall.rect.move(d1,d2)
    for e in enemy_sprites:
        e.rect = e.rect.move(d1,d2)
    for s in sword_sprite:
        s.rect = s.rect.move(d1,d2)
    camera[0] += d1
    camera[1] += d2
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

def adjacent(a, b):
    re = []
    if (a + 1 < 9) and (map[a+1][b] =="0"): 
        tup = [a+1,b]
        re.append(tup)
    if (a - 1 >= 0) and (map[a-1][b] =="0"): 
        tup = [a-1,b]
        re.append(tup)
    if (b + 1 < 9) and (map[a][b+1] =="0"): 
        tup = [a,b+1]
        re.append(tup)
    if (b - 1 >= 0) and (map[a][b-1] =="0"):
        tup = [a,b-1]
        re.append(tup)
    return re

def adjacent_nonzero(a, b):
    re = []
    if (a + 1 < 9) and (islands[a+1][b] !=0): 
        tup = [a+1,b]
        re.append(tup)
    if (a - 1 >= 0) and (islands[a-1][b] !=0): 
        tup = [a-1,b]
        re.append(tup)
    if (b + 1 < 9) and (islands[a][b+1] !=0): 
        tup = [a,b+1]
        re.append(tup)
    if (b - 1 >= 0) and (islands[a][b-1] !=0):
        tup = [a,b-1]
        re.append(tup)
    return re

def random_map():
    map[4][4] = "S"
    for i in range(5):
        empty_list = []
        for j in range(9):
            for k in range(9):
                if (map[j][k] != "0"):
                    empty_list.append(adjacent(j,k))
        temp = []
        while (temp == []):
            temp = random.choice(empty_list)
        temp1 = random.choice(temp)
        map[int(temp1[0])][int(temp1[1])] = "R"
    pprint(map)

def generate_map():
    for i in range(9):
        for j in range(9):
            if (map[i][j] != "0"):
                generate_room(25*j,25*i,25*j+20,25*i+20)

def update_islands():
    for k in paths:
        p = k.get()
        smaller = min(int(islands[p[0]][p[1]]),int(islands[p[2]][p[3]]))
        larger = max(int(islands[p[0]][p[1]]),int(islands[p[2]][p[3]]))
        if (smaller != larger):
            for i in range(9):
                for j in range(9):
                    if (islands[i][j] == larger):
                        islands[i][j] = smaller

def random_path():
    k = 1
    for i in range(9):
        for j in range(9):
            if (map[i][j] != "0"):
                islands[i][j] = k
                k+=1
    
    while True:
        update_islands()
        addable_paths = []
        for i in range(9):
            for j in range(9):
                if (map[i][j] != "0"):
                    adj = adjacent_nonzero(i,j)
                    for pos in adj:
                        if islands[i][j] != islands[pos[0]][pos[1]]:
                            p = Pathh(i,j,pos[0],pos[1])
                            addable_paths.append(p)
        if (len(addable_paths)==0):
            break
        to_be_addded_path = random.choice(addable_paths)
        paths.append(to_be_addded_path)

def remove_wall_at(a,b):
    for wall in wall_sprites:
        if wall.rect.center == (a*50, b*50):
            wall.kill()

def generate_path():

    for p in paths:
        pos = p.get()

        if (pos[0] == pos[2]):
            if (pos[1] < pos[3]):
                generate_room(pos[1]*25 + 20,pos[0]*25 + 12, pos[3]*25,pos[2]*25 + 8)
                for i in range(pos[0]*25 + 9, pos[0]*25 + 12):
                    remove_wall_at(pos[1]*25 + 20, i)
                    remove_wall_at(pos[3]*25, i)
                
            else:
                generate_room(pos[3]*25 + 20,pos[2]*25 + 12, pos[1]*25,pos[0]*25 + 8)
                for i in range(pos[0]*25 + 9, pos[0]*25 + 12):
                    remove_wall_at(pos[3]*25 + 20, i)
                    remove_wall_at(pos[1]*25, i)
        else:
            if (pos[0] < pos[2]):
                generate_room(pos[1]*25 + 12,pos[0]*25 + 20, pos[3]*25 + 8,pos[2]*25)
                for i in range(pos[1]*25 + 9, pos[1]*25 + 12):
                    remove_wall_at(i, pos[0]*25 + 20)
                    remove_wall_at(i, pos[2]*25)
            else:
                generate_room(pos[3]*25 + 12,pos[2]*25 + 20, pos[1]*25 + 8,pos[0]*25)
                for i in range(pos[1]*25 + 9, pos[1]*25 + 12):
                    remove_wall_at(i, pos[2]*25 + 20)
                    remove_wall_at(i, pos[0]*25)

def random_stuffs_in_room():
    re = [[0]*19 for i in range(19)]
    for i in range(7):
        while(True):
            x = random.randrange(17) + 1
            y = random.randrange(17) + 1
            if (re[x][y] == 0):
                re[x][y] = 1
                break
    for i in range(3):
        while(True):
            x = random.randrange(17) + 1
            y = random.randrange(17) + 1
            if (re[x][y] == 0 and x+1 < 19 and re[x+1][y] == 0):
                re[x][y] = 2
                re[x+1][y] = 2
                break
    for i in range(3):
        while(True):
            x = random.randrange(17) + 1
            y = random.randrange(17) + 1
            if (re[x][y] == 0 and y+1 < 19 and re[x][y+1] == 0):
                re[x][y] = 2
                re[x][y+1] = 2
                break
    return re

def generate_stuffs_in_room(a, xx, yy):
    pprint(a)
    for i in range(19):
        for j in range(19):
            if (a[i][j] == 1):
                e = Enemy1((25*50*yy + (j+1)*50, 25*50*xx + (i+1)*50))
                room_sprites[xx][yy].add(e)
            if (a[i][j] == 2):
                w = Wall((25*50*yy + (j+1)*50, 25*50*xx + (i+1)*50))
                room_sprites[xx][yy].add(w)

def random_generate():
    random_map()
    generate_map()
    random_path()
    generate_path()
    for i in range(9):
        for j in range(9):
            if (map[i][j] =="R"):
                generate_stuffs_in_room(random_stuffs_in_room(),i,j)

def activate_stuffs_in_room(xx,yy):
    sprites = room_sprites[xx][yy]
    for s in sprites:
        if s.type == "wall":
            s.displace_teleport(camera[0],camera[1])
            wall_sprites.add(s)
        elif s.type =="enemy":
            s.displace_teleport(camera[0],camera[1])
            enemy_sprites.add(s)

def current_in_room():
    xx = main.rect.center[0] - camera[0]
    yy = main.rect.center[1] - camera[1]
    rex = int(xx/25/50)
    rey = int(yy/25/50)
    return (rey, rex)

main = MainCharacter()
main_sprite.add(main)

random_generate()

while 1:
    pygame.time.Clock().tick(120)

    if (shooting == True):
        shoot()
    posx, posy = current_in_room()

    if (visited[posx][posy] == 0 and map[posx][posy] == "R"):
        visited[posx][posy] = 1
        print("activated", posx,posy)
        activate_stuffs_in_room(posx,posy)


    refresh()
    handle_event()
    handle_movement()
    bullet_sprites.update()
    enemy_sprites.update()
    sword_sprite.update(main.rect.center)