# random appearance with animation
import random
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Colors we want to use
pink = (255,157,195)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)
brown = (76,43,32)
orange = (200,71,0)
darkorange = (140,50,0)

# Sounds we want to use
pygame.mixer.init()
hitsound = pygame.mixer.Sound(resource_path("Resources//hit.wav"))
menumusic = pygame.mixer.Sound(resource_path("Resources//mainMenuMusic.mp3"))

musicplaying = menumusic

# set up the display
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Mole Adventures")
menumusic.play(loops=-1)
levelbackground = pygame.image.load(resource_path("Resources//oneBackground.png")).convert()
levelbackground = pygame.transform.scale(levelbackground, (screen_width, screen_height))
menubackground = pygame.image.load(resource_path("Resources//menuBackground.png")).convert()
menubackground = pygame.transform.scale(menubackground, (screen_width, screen_height))
settingsbackground = pygame.image.load(resource_path("Resources//settingsBackground.png")).convert_alpha()
settingsbackground = pygame.transform.smoothscale(settingsbackground, (1152, 768))

#mis images
xbutton = image.load(resource_path("Resources//xButton.png")).convert_alpha()
xbutton = pygame.transform.scale(xbutton, (75, 75))
xbuttonRect = xbutton.get_rect(center=(1085, 225))

moleabsent = image.load(resource_path("Resources//molehole.png")).convert_alpha()
moleabsent = pygame.transform.scale(moleabsent, (125, 125))
normalmole = image.load(resource_path("Resources//normalMole.png")).convert_alpha()
normalmole = pygame.transform.scale(normalmole, (125, 125))
armoredmole = image.load(resource_path("Resources//armoredMole.png")).convert_alpha()
armoredmole = pygame.transform.scale(armoredmole, (125, 125))
speedymole = image.load(resource_path("Resources//speedyMole.png")).convert_alpha()
speedymole = pygame.transform.scale(speedymole, (125, 125))
molehit = image.load(resource_path("Resources//hitMole.png")).convert_alpha()
molehit = pygame.transform.scale(molehit, (125, 125))
moledead = image.load(resource_path("Resources//deadMole.png")).convert_alpha()
moledead = pygame.transform.scale(moledead, (125, 125))

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = moleabsent
        self.rect = self.image.get_rect(center=(x, y))
        self.status = 'absent'
        self.kind = None
        self.timer = 0
        self.duration = 0
        self.health = 0
        self.hit_timer = 0
        self.hit_duration = 2
    
    # creates different moles
    def activate(self):
        r = random.randint(1, 100)
        if r == 1:
            self.status = 'normal'
            self.image = normalmole
            self.duration = 15
            self.health = 1
            self.kind = 'normal'
        elif r == 2:
            self.status = 'armored'
            self.image = armoredmole
            self.duration = 25
            self.health = 3
            self.kind = 'armored'
        elif r == 3:
            self.status = 'speedy'
            self.image = speedymole
            self.duration = 12
            self.health = 1
            self.kind = 'speedy'
        self.timer = 0

    # controls when the mole goes out and back in
    def update(self):
        if self.status == 'absent':
            self.activate()
        elif self.status == 'hit':
            self.hit_timer += 1
            if self.hit_timer >= self.hit_duration:
                if self.health <= 0:
                    self.status = 'absent'
                    self.image = moleabsent
                else:
                    if self.kind == 'armored':
                        self.image = armoredmole
                        self.status = 'armored'
                    elif self.kind == 'normal':
                        self.image = normalmole
                        self.status = 'normal'
                    elif self.kind == 'speedy':
                        self.image = speedymole
                        self.status = 'speedy'
        else:
            self.timer += 1
            if self.timer >= self.duration:
                self.status = 'absent'
                self.image = moleabsent

    def hit(self):
        if self.status in ['normal', 'armored', 'speedy']:
            hitsound.play()
            self.health -= 1
            if self.health == 0:
                self.image = moledead
            else:
                self.image = molehit
            self.status = 'hit'
            self.hit_timer = 0



# for timing
framerate = 200  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

# create our moles
moles = [[None for _ in range(3)] for _ in range(3)]
x = screen_width // 4
y = screen_height // 4
for i in range(3):
    for j in range(3):
        moles[i][j] = Mole(x,y)
        x += screen_width // 4
    x = screen_width // 4
    y += screen_height // 4

# intital boot up
game_state = 'menu'
cursor_image = None
cursor_rect = None
allmoles = Group(moles)
allmoles.draw(screen)
gameStarted = False

# create some fonts
headerfont = pygame.font.SysFont('comicsansms',48)
headerfont.set_bold(True)
menubuttonfont = pygame.font.SysFont('impact',48)
buttonfont = pygame.font.SysFont('impact',32)

# create level text
headerText = headerfont.render("Mole Meadows", True, brown)
headerRect = headerText.get_rect()
headerRect.center = (screen_width // 2, 125)

#menu buttons
menuQuitButtonRect = pygame.Rect(0, 0, 250, 85)
menuQuitButtonRect.center = (screen_width - 350, screen_height - 200)
menuStartButtonRect = pygame.Rect(0, 0, 250, 85)
menuStartButtonRect.center = (screen_width - 350, screen_height - 400)
menuSettingsButtonRect = pygame.Rect(0, 0, 250, 85)
menuSettingsButtonRect.center = (screen_width - 350, screen_height - 300)
menuQuitButtonText = menubuttonfont.render(" Quit ", True, black)
menuStartButtonText = menubuttonfont.render(" Start ", True, black)
menuSettingsButtonText = menubuttonfont.render(" Settings ", True, black)

# level buttons
levelQuitButtonRect = pygame.Rect(0, 0, 200, 60)
levelQuitButtonRect.center = (300, screen_height - 50)
levelMenuButtonRect = pygame.Rect(0, 0, 200, 60)
levelMenuButtonRect.center = (screen_width - 300, screen_height - 50)
levelQuitButtonText = buttonfont.render(" Quit ", True, black)
levelMenuButtonText = buttonfont.render(" Menu ", True, black)
sfxCondition = True
musicCondition = True

# settings buttons
sfxButtonRect = pygame.Rect(0, 0, 550, 100)
sfxButtonRect.center = (screen_width // 2 - 10, 400)
musicButtonRect = pygame.Rect(0, 0, 550, 100)
musicButtonRect.center = (screen_width // 2 - 10, 550)
sfxButtonText = menubuttonfont.render(" SFX: ON ", True, black)
musicButtonText = menubuttonfont.render(" Music: ON ", True, black)

def draw_menu(mousex, mousey):
    screen.blit(menubackground, (0, 0))
    #quit button
    quit_bg = darkorange if menuQuitButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, quit_bg, menuQuitButtonRect)
    pygame.draw.rect(screen, black, menuQuitButtonRect, 5)
    text_rect = menuQuitButtonText.get_rect(center=menuQuitButtonRect.center)
    screen.blit(menuQuitButtonText, text_rect)
    #play button
    start_bg = darkorange if menuStartButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, start_bg, menuStartButtonRect)
    pygame.draw.rect(screen, black, menuStartButtonRect, 5)
    text_rect = menuQuitButtonText.get_rect(center=menuStartButtonRect.center)
    screen.blit(menuStartButtonText, text_rect)
    #settings button
    settings_bg = darkorange if menuSettingsButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, settings_bg, menuSettingsButtonRect)
    pygame.draw.rect(screen, black, menuSettingsButtonRect, 5)
    text_rect = menuSettingsButtonText.get_rect(center=menuSettingsButtonRect.center)
    screen.blit(menuSettingsButtonText, text_rect)
    pygame.event.set_grab(True)

def draw_level():
    screen.blit(levelbackground, (0, 0))
    screen.blit(headerText, headerRect)
    allmoles.draw(screen)
    quit_bg = darkorange if levelQuitButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, quit_bg, levelQuitButtonRect)
    pygame.draw.rect(screen, black, levelQuitButtonRect, 5)
    text_rect = levelQuitButtonText.get_rect(center=levelQuitButtonRect.center)
    screen.blit(levelQuitButtonText, text_rect)
    menu_bg = darkorange if levelMenuButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, menu_bg, levelMenuButtonRect)
    pygame.draw.rect(screen, black, levelMenuButtonRect, 5)
    text_rect = levelMenuButtonText.get_rect(center=levelMenuButtonRect.center)
    screen.blit(levelMenuButtonText, text_rect)
    if cursor_image and cursor_rect:
        cursor_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_image, cursor_rect)

def draw_settings():
    rect = settingsbackground.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(settingsbackground, rect)
    screen.blit(xbutton, xbuttonRect)
    # SFX Button
    sfx_bg = darkorange if sfxButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, sfx_bg, sfxButtonRect)
    pygame.draw.rect(screen, black, sfxButtonRect, 5)
    text_rect = sfxButtonText.get_rect(center=sfxButtonRect.center)
    screen.blit(sfxButtonText, text_rect)
    # Music Button
    music_bg = darkorange if musicButtonRect.collidepoint(mousex, mousey) else orange
    pygame.draw.rect(screen, music_bg, musicButtonRect)
    pygame.draw.rect(screen, black, musicButtonRect, 5)
    text_rect = musicButtonText.get_rect(center=musicButtonRect.center)
    screen.blit(musicButtonText, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.event.set_grab(False)
            pygame.quit()
            sys.exit()

        if event.type == TIMEREVENT and game_state == 'level':
            for row in moles:
                for mole in row:
                    mole.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()

            if game_state == 'menu':
                
                if menuQuitButtonRect.collidepoint(mousex, mousey):
                    pygame.quit(); sys.exit(); pygame.event.set_grab(False)
                if menuStartButtonRect.collidepoint(mousex, mousey):
                    game_state = 'level'
                    pygame.mouse.set_visible(False)
                    cursor_image = pygame.image.load(resource_path("Resources//defaultHammer.png"))
                    cursor_image = pygame.transform.scale(cursor_image, (50, 50))
                    cursor_rect = cursor_image.get_rect()
                if menuSettingsButtonRect.collidepoint(mousex, mousey):
                    game_state = 'settings'
                    pygame.mouse.set_visible(True)
                    draw_settings()

            elif game_state == 'level':
                for row in moles:
                    for mole in row:
                        if mole.rect.collidepoint(mousex, mousey):
                            mole.hit()
                if levelQuitButtonRect.collidepoint(mousex, mousey):
                    pygame.quit(); sys.exit(); pygame.event.set_grab(False)
                if levelMenuButtonRect.collidepoint(mousex, mousey):
                    game_state = 'menu'
                    moles = [[None for _ in range(3)] for _ in range(3)]
                    x = screen_width // 4; y = screen_height // 4
                    for i in range(3):
                        for j in range(3):
                            moles[i][j] = Mole(x, y)
                            x += screen_width // 4
                        x = screen_width // 4
                        y += screen_height // 4
                    allmoles = Group([m for row in moles for m in row])

            elif game_state == 'settings':
                if xbuttonRect.collidepoint(mousex, mousey):
                    game_state = 'menu'
                    pygame.mouse.set_visible(True)
                if sfxButtonRect.collidepoint(mousex, mousey):
                    if sfxCondition == True:
                        sfxButtonText = menubuttonfont.render(" SFX: OFF ", True, black)
                        sfxCondition = False
                    else:
                        sfxButtonText = menubuttonfont.render(" SFX: ON ", True, black)
                        sfxCondition = True
                if musicButtonRect.collidepoint(mousex, mousey):
                    if musicCondition == True:
                        musicButtonText = menubuttonfont.render(" Music: OFF ", True, black)
                        musicCondition = False
                        musicplaying.stop()
                    else:
                        musicButtonText = menubuttonfont.render(" Music: ON ", True, black)
                        musicCondition = True
                        musicplaying.play()
                    

    mousex, mousey = pygame.mouse.get_pos()

    if game_state == 'menu':
        pygame.mouse.set_visible(True)
        draw_menu(mousex, mousey)

    elif game_state == 'level':
        draw_level()

    elif game_state == 'settings':
        pygame.mouse.set_visible(True)
        draw_settings()

    pygame.display.update()
