import pygame


SHADOW_BLACK = (30, 30, 30)
YETI_BLUE = (150, 150, 255)
YETI_BLUE_LIT = (180, 180, 255)
WHITE = (255, 255, 255)

shadow_offset = 1

class Button:
    def __init__(self, x, y, w, h, text, execute_function):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.text = text
        self.execute_function = execute_function

    def display_inactive_mode (self, win):
        pygame.draw.rect(win, SHADOW_BLACK, (self.x, self.y, self.width + shadow_offset, self.height + shadow_offset))
        pygame.draw.rect(win, YETI_BLUE, (self.x, self.y, self.width, self.height))

        font = pygame.font.SysFont ('', 17)
        text = font.render(self.text, True, (0, 0, 0))
        win.blit (text, (self.x + 20, self.y + self.height/2 - 5))

    def display_active_mode (self, win):
        pygame.draw.rect(win, SHADOW_BLACK, (self.x, self.y, self.width + shadow_offset, self.height + shadow_offset))
        pygame.draw.rect(win, YETI_BLUE_LIT, (self.x, self.y, self.width, self.height))

        font = pygame.font.SysFont('', 17)
        text = font.render(self.text, True, (0, 0, 0))
        win.blit(text, (self.x + 20, self.y + self.height / 2 - 5))

    def display_clicked_mode (self, win):
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.width + shadow_offset, self.height + shadow_offset))
        pygame.draw.rect(win, YETI_BLUE,(self.x + shadow_offset, self.y + shadow_offset, self.width, self.height))

        font = pygame.font.SysFont('', 17)
        text = font.render(self.text, True, (0, 0, 0))
        win.blit(text, (self.x+1 + 20, self.y+1 + self.height / 2 - 5))