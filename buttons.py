import pygame

class makeButtons(pygame.sprite.Sprite):
    def __init__(self, image:str, pos:tuple, surface:pygame.surface, scale:float = 1) -> None:
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(image), scale)
        self.rect = self.image.get_rect(center = pos)
        self.click = True
        self.surface = surface
    
    def isClicked(self) -> bool:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mousePos) and mousePressed[0]:
            if self.click:
                self.click = False
                return True   
        else:
            self.click = True
            return False
    
    def showButton(self) -> None:
        self.surface.blit(self.image, self.rect)

# EXAMPLE
if __name__ == "__main__":
    from sys import exit
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    test = makeButtons("sprites/return.png", (200, 200), screen, 2)
    a = makeButtons("sprites/restart.png", (600, 200), screen, 2)
    
    state1 = True
    state2 = False
    
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        screen.fill("black")
        
        if state1:
            test.showButton()
            if test.isClicked() == True:
                print("Hello World!")
                state1 = False
                state2 = True
        
        if state2:
            a.showButton()
            if a.isClicked() == True:
                print("Olá mundo!")
                state2 = False
                state1 = True
        
        pygame.display.update()
        # WORKS!