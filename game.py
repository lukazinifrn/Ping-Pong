import pygame, texts, buttons
from sys import exit
from random import choice

# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 100))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = (15, w_h/2))
        self.speed = 5
    
    def movement(self):
        keys = pygame.key.get_pressed()
        ball = ballGroup.sprite
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if ball.isCollidingPlayer:
                ball.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if ball.isCollidingPlayer:
                ball.rect.y += self.speed
    
    def outofWIndow(self):
        ball = ballGroup.sprite
        if self.rect.top < 10:
            self.rect.top += self.speed
            if ball.isCollidingPlayer:
                ball.rect.y += self.speed
        if self.rect.bottom > w_h - 10:
            self.rect.bottom -= self.speed
            if ball.isCollidingPlayer:
                ball.rect.y -= self.speed
    
    def update(self):
        self.movement()
        self.outofWIndow()
    
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load("sprites/ball.png"), 0.45)
        self.rect = self.image.get_rect(center = (w_w/2, w_h/2))
        self.speedX = 5
        self.speedY = 5
        self.playerHoldTimer = 0
        self.botHoldTimer = 0
        self.collide = False
        self.pointCollidedY = 0
        self.isCollidingPlayer = False
        self.isCollidingBot = False
        self.speedMultiplierX = 1
        self.speedMultiplierY = 1
        self.DirectionX = choice([1, -1])
        self.DirectionY = choice([1, -1])
    
    def movement(self):
        self.rect.x += self.speedX * self.DirectionX * self.speedMultiplierX
        if not(self.isCollidingPlayer) and not(self.isCollidingBot):
            self.rect.y += self.speedY * self.DirectionY * self.speedMultiplierY
    
    def collisions(self):
        if self.rect.top < 0 or self.rect.bottom > w_h:
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > w_h:
                self.rect.bottom = w_h
            self.DirectionY *= -1
            self.speedMultiplierX += 0.01
            self.speedMultiplierY += 0.012
        
        if self.rect.left < 0 or self.rect.right > w_w:
            self.DirectionX *= -1
            
        player = playerGroup.sprite
        bot = botGroup.sprite
        
        if self.rect.colliderect(player.rect):
            if not(self.collide):
                self.collide = True
                self.pointCollidedY = self.rect.centery
            self.isCollidingPlayer = True
            collision_player = self.rect.clip(player.rect)
            self.playerHoldTimer += 1
            self.rect.midleft = collision_player.midright
            if self.playerHoldTimer == 6:       
                self.speedX *= -1
                self.playerHoldTimer = 0
                self.speedMultiplierX += 0.015
                self.speedMultiplierY += 0.012 
                
        else:
            self.isCollidingPlayer = False
            if not(self.isCollidingBot):
                self.collide = False
        
        if self.rect.colliderect(bot.rect):
            if not(self.collide):
                self.pointCollidedY = self.rect.centery
                self.collide = True
            self.isCollidingBot = True
            collision_bot = self.rect.clip(bot.rect)
            self.botHoldTimer += 1
            self.rect.midright = collision_bot.midleft
            if self.botHoldTimer == 6:       
                self.speedX *= -1
                self.botHoldTimer = 0
                self.speedMultiplierX += 0.015
                self.speedMultiplierY += 0.012
        else:
            self.isCollidingBot = False
            if not(self.isCollidingPlayer):
                self.collide = False
    
    def changeSide(self):
        if self.isCollidingBot or self.isCollidingPlayer:
            if self.rect.y < self.pointCollidedY:
                self.DirectionY = -1
            if self.rect.y > self.pointCollidedY:
                self.DirectionY = 1
    
    def update(self):
        self.movement()
        self.collisions()
        self.changeSide()

class Bot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 100))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = (w_w-15, w_h/2)) 
        self.speed = 5
        self.side = choice([-1, 1])
        
    def movement(self):
        ball = ballGroup.sprite
        if ball.rect.centery != self.rect.centery and not(ball.isCollidingBot):
            if ball.rect.centery - self.rect.centery > 30:
                self.rect.centery += self.speed

            if ball.rect.centery - self.rect.centery < 30:
                self.rect.centery -= self.speed

        if ball.isCollidingBot:
            self.rect.y += self.speed * self.side
            ball.rect.y += self.speed * self.side
        else:
            self.side = choice([-1, 1])
    
    def outofWIndow(self):
        ball = ballGroup.sprite
        if self.rect.top < 10:
            self.rect.top += self.speed
            if ball.isCollidingBot:
                ball.rect.y += self.speed
        if self.rect.bottom > w_h - 10:
            self.rect.bottom -= self.speed
            if ball.isCollidingBot:
                ball.rect.y -= self.speed
    
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

ballGroup = pygame.sprite.GroupSingle()
ballGroup.add(Ball())

botGroup = pygame.sprite.GroupSingle()
botGroup.add(Bot())

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
            
        if gameMode_survive_button.isClicked() == True:
            home = False
            gameMode_survive = True
    
    if gameMode_points:
        in_points = True
        screen.fill("black") 
        pause_button.showButton()
        pygame.draw.line(screen, "white", (w_w/2, 0), (w_w/2, w_h), 3)
        playerGroup.draw(screen)
        playerGroup.update()
        ballGroup.draw(screen)
        ballGroup.update()
        botGroup.draw(screen)
        botGroup.update()
        if pause_button.isClicked() == True:
            gameMode_points = False
            pause = True
        
    if gameMode_survive:
        in_survive = True
        screen.fill("black") 
        pause_button.showButton()
        pygame.draw.line(screen, "white", (w_w/2, 0), (w_w/2, w_h), 3)
        playerGroup.draw(screen)
        playerGroup.update()
        ballGroup.draw(screen)
        ballGroup.update()
        botGroup.draw(screen)
        botGroup.update()
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
        