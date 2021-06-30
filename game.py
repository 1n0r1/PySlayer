import sys, pygame, random


pygame.init()
size = width, height = 1366, 768
screen = pygame.display.set_mode(size)
speed = [0,0]


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # image
        # rect
        self.image = pygame.image.load("mc.png")

        self.rect = self.image.get_rect()
        self.rect.center = (250,250)



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


main = MainCharacter()
main_sprite = pygame.sprite.Group()
main_sprite.add(main)

clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    handle_movement()
    
    screen.fill((255, 255, 255))
    main_sprite.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()