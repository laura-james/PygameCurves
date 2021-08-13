import pygame
pygame.init()

def gunshoot():
    global gun_rect, yellow_gun_rect
    gun_rect = yellow_gun_rect
    print("shoot")

screen = pygame.display.set_mode([400,400])
pygame.display.set_caption("space invaderz")
clock = pygame.time.Clock()
#set up spritesheet and rectangle
gun_img = pygame.image.load("spritesheet.png")
green_gun_rect = pygame.Rect(0, 0, 32, 32)
yellow_gun_rect = pygame.Rect(32, 0, 32, 32)
gun_rect =  green_gun_rect #this might get changed in the shoot() function
gunX = 200
gunY = 400 - 32 - 10
done = False

moveLeft  = False
moveRight = False
while not done:
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
                gunshoot()

        if event.type == pygame.KEYUP:
            moveLeft = False
            moveRight = False
            gun_rect = green_gun_rect

    if moveLeft:
        gunX -= 5
    if moveRight:
        gunX += 5
    #drawing stuff
    screen.fill((12, 34, 56))
    #draw a gun here

    screen.blit(gun_img, (gunX, gunY), gun_rect)
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
