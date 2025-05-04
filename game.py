import pygame, texts, buttons
from sys import exit
from random import choice, choices, randint

# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 125))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = (15, w_h/2))
        self.speed = 5
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
    
    def outofWIndow(self):
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > w_h - 10:
            self.rect.bottom = w_h - 10
              
    def update(self):
        self.movement()
        self.outofWIndow()
        
pygame.init()

w_w = 1000
w_h = 500
icon = pygame.image.load("sprites/icon.png")
screen = pygame.display.set_mode((w_w, w_h))
pygame.display.set_caption("Ping-Pong")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# SPRITES GROUPS
playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(Player())

# OTHER ELEMENTS
section = pygame.transform.scale_by(pygame.image.load("sprites/section.png"), 1.7)
section_rect = section.get_rect(center = (w_w/2, w_h/2))

# BUTTONS
gameMode_points_button = buttons.makeButtons("sprites/points.png", (300, 300), screen, 3)
gameMode_survive_button = buttons.makeButtons("sprites/survive.png", (700, 300), screen, 3)
pause_button = buttons.makeButtons("sprites/pause.png", (30, 30), screen, 1.5)
return_button = buttons.makeButtons("sprites/return.png", (w_w/2 - 100, 380), screen, 2.5)

# TEXTS
gameTitle = texts.makeText("PYPONG!", 150, (w_w/2, 70), screen)
selectMode_text = texts.makeText("Selecione o modo de jogo!", 72, (w_w/2, 160), screen)
gameMode_points_text = texts.makeText("Points", 60, (gameMode_points_button.rect.centerx, 380), screen)
gameMode_survive_text = texts.makeText("Survive", 60, (gameMode_survive_button.rect.centerx, 380), screen)
pause_text = texts.makeText("PAUSADO", 100, (w_w/2, 100), screen)
return_text = texts.makeText("Retomar", 35, (return_button.rect.centerx, return_button.rect.bottom + 17), screen)

# GAMESTATES
home = True
gameMode_points = False
in_points = False
gameMode_survive = False
in_survive = False
pause = False

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    if home:
        screen.fill("black") 
        gameTitle.showText()
        selectMode_text.showText()
        gameMode_points_button.showButton()
        gameMode_survive_button.showButton()
        gameMode_points_text.showText()
        gameMode_survive_text.showText()
        
        if gameMode_points_button.isClicked() == True:
            home = False
            gameMode_points = True
            in_points = True     
        if gameMode_survive_button.isClicked() == True:
            home = False
            gameMode_survive = True
            in_survive = True
    
    if gameMode_points:
        screen.fill("black") 
        pause_button.showButton()
        pygame.draw.line(screen, "white", (w_w/2, 0), (w_w/2, w_h), 3)
        playerGroup.draw(screen)
        playerGroup.update()
        if pause_button.isClicked() == True:
            gameMode_points = False
            pause = True
        
    if gameMode_survive:
        screen.fill("black") 
        pause_button.showButton()
        pygame.draw.line(screen, "white", (w_w/2, 0), (w_w/2, w_h), 3)
        playerGroup.draw(screen)
        playerGroup.update()
        if pause_button.isClicked() == True:
            gameMode_survive = False
            pause = True
        
    if pause:
        screen.blit(section, section_rect)
        pause_text.showText()
        return_text.showText()
        pause_button.showButton()
        return_button.showButton()
        if pause_button.isClicked() == True or return_button.isClicked() == True:
            pause = False
            if in_points:
                gameMode_points = True
            if in_survive:
                gameMode_survive = True
    
    pygame.display.update()
    clock.tick(60)
        