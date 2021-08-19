import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound("shot.wav")
numaliens = 0

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # intermediate temporary image that will be a slice of the spritesheet
        image = pygame.Surface((32, 32))
        image.blit(spritesheet_img, (0, 0), (0, 0, 32, 32)) # green gun which is 32x32 pixels at 0,0 on the sheet

        self.image = image
        self.image.set_colorkey((0, 0, 0)) # have to say that the color black is rendered as transparent

        self.rect = self.image.get_rect()
        self.rect.center = (gunX, gunY)

    def update(self):
        self.rect.x = gunX
        self.rect.y = gunY

    def gunshoot(self):
        image = pygame.Surface((32, 32))
        image.blit(spritesheet_img, (0, 0), (32, 0, 32, 32)) # yellow gun

        self.image = image
        self.image.set_colorkey((0, 0, 0))

        mybullet = Bullet()
        all_sprites.add(mybullet)
        #sound.play()

    def reset(self):
        image = pygame.Surface((32, 32))
        image.blit(spritesheet_img, (0, 0), (0, 0, 32, 32))  # green gun

        self.image = image
        self.image.set_colorkey((0, 0, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # intermediate temporary image that will be a slice of the spritesheet
        image = pygame.Surface((8, 8))
        image.blit(spritesheet2_img, (0, 0), (0, 0, 8, 8))  # bullet

        self.image = image
        self.image.set_colorkey((0, 0, 0))  # have to say that the color black is rendered as transparent

        self.rect = self.image.get_rect()
        self.rect.center = (gunX + 16, gunY)  # have to add 16 pixels so it comes out teh center of the gun
        bullets.add(self)

    def update(self):

        self.rect.y -= 10  # bullet floats up

class Alien(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        global numaliens
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.dir = "right"
        self.speed = 6
        # intermediate temporary image that will be a slice of the spritesheet
        image = pygame.Surface((32, 32))

        if type == "mothership":
            image.blit(aliensprite_img, (0, 0), (0, 0, 32, 32))  # pink alien
            self.speed = 10
        else:
            image.blit(aliensprite_img, (0, 0), (32, 0, 32, 32))  # alien

        self.image = image
        self.image.set_colorkey((0, 0, 0))  # have to say that the color black is rendered as transparent

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        numaliens = numaliens + 1

    def update(self):
        #print("XY",self.x,self.y)
        #print("RECTXY",self.rect.x, self.rect.y)

        if self.rect.x > 400-32:
            self.dir = "left"
        if self.rect.x < 0:
            self.dir = "right"

        if self.dir == "right":
            self.rect.x += self.speed  # alien float right
        if self.dir == "left":
            self.rect.x -= self.speed  # alien float left
        self.x, self.y = self.rect.x, self.rect.y



pygame.init()
screen = pygame.display.set_mode([400,  400])
pygame.display.set_caption("space invaderz")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group() # a group to hold all teh sprites
bullets = pygame.sprite.Group() # a group to hold all teh bullets
aliens = pygame.sprite.Group() # a group to hold all teh aliens

#set up spritesheet and rectangle
spritesheet_img = pygame.image.load("spritesheet.png")
spritesheet2_img = pygame.image.load("spritesheet2.png")
aliensprite_img = pygame.image.load("alien-sprites.png")

# set up and create Gun
gunX = 200
gunY = 400 - 32 - 10
moveLeft  = False
moveRight = False
mygun = Gun() # uses the class Gun
all_sprites.add(mygun)  #add it to all sprites group

# set up and create 8 aliens
for i in range(8):
    pos = (50*i)+10
    print(pos)
    myalien = Alien(pos, 20, "normal")
    aliens.add(myalien)  # add to the group aliens
# create special Mothership alien
myalien2 = Alien(20, 50, "mothership")
aliens.add(myalien2)  # add to the group aliens

score = 0


# start event loop
done = False
while not done:
    # detect events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
                moveRight = False
            if event.key == pygame.K_RIGHT:
                moveLeft = False
                moveRight = True
            if event.key == pygame.K_SPACE:
                mygun.gunshoot() # runs the gun's gunshoot method

        if event.type == pygame.KEYUP:
            moveLeft = False
            moveRight = False
            mygun.reset()

    if moveLeft:
        gunX -= 10
    if moveRight:
        gunX += 10
    #  updates the sprite groups
    all_sprites.update()
    aliens.update()
    bullets.update()
    #print(bullets)
    hits = pygame.sprite.groupcollide(bullets, aliens, False, True)  #  the 2nd True removes the alien that gets hit
    for h in hits:
        print(h)
        # score is being shown in the window title for now
        score = score + 1
        pygame.display.set_caption("You have shot " + str(score) + " aliens out of a total of " + str(numaliens) + "!")

    #print(hits)
    #drawing stuff

    # dark grey blue background
    screen.fill((12, 34, 56))

    # draws all the spite groups
    all_sprites.draw(screen)
    aliens.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
