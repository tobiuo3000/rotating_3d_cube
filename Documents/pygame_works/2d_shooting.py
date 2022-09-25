import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PLAYER_SPEED = 15
MISSILE_SPEED = 20
PATH = "Documents\pygame_works"
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        """
        PLAYER_IMAGE = pygame.image.load( PATH + "\player_image.png").convert()
        self.surf = pygame.transform.scale(PLAYER_IMAGE, (40, 20))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        """
        self.surf = pygame.Surface((40, 25))
        self.surf.fill((200, 200, 255)) 
        
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -PLAYER_SPEED)
            #move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, PLAYER_SPEED)
            #move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((random.randint(30, 40), random.randint(20, 25)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 12)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Missile(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, move_x, move_y):
        super(Missile, self).__init__()
        self.surf = pygame.Surface((10, 7))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                player_x,
                player_y
            )
        )
        self.speed = (move_x, move_y)
    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
    
    
pygame.init()

#pygame.mixer.music.load(PATH + "\background.mp3")
#pygame.mixer.music.play(loops=-1)
#move_up_sound = pygame.mixer.Sound(PATH + "\moveup_sound.mp3")
#move_down_sound = pygame.mixer.Sound(PATH + "\movedown_sound.mp3")
#missile_sound = pygame.mixer.Sound(PATH + "\missile_sound.mp3")
#collision_sound = pygame.mixer.Sound(PATH + "\collision_sound.mp3")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

missiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                    
            elif event.key == K_SPACE:
                right_missile = Missile(player.rect.right, player.rect.bottom, MISSILE_SPEED, 0)
                upright_missile = Missile(player.rect.right, player.rect.bottom, MISSILE_SPEED, -5)
                upleft_missile = Missile(player.rect.right, player.rect.bottom, MISSILE_SPEED, 5)
                missile_list = [right_missile, upright_missile, upleft_missile]
                #missile_sound.play()
                for new_missile in missile_list:
                    missiles.add(new_missile)
                    all_sprites.add(new_missile)
                
                 
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    pressed_keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    player.update(pressed_keys)
    enemies.update()
    missiles.update()
    
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        running = False
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
    for each_enemy in enemies:
        if pygame.sprite.spritecollideany(each_enemy, missiles):
            each_enemy.kill()   

    pygame.display.flip()
    clock.tick(30)