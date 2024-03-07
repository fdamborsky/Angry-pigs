import pygame
import random

from pygame.sprite import Group

# - GAME START
pygame.init()

# - SCREEN
width = 1200
height = 800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Angry Pigs")
# - GAME SETTINGS
fps = 60
clock = pygame.time.Clock()

# - CLASS
class Game():

    def __init__(self, our_player, group_of_enemies):
        self.score = 0
        self.round_number = 0
        
        self.round_time = 0
        self.slowdown_cycle = 0

        self.our_player = our_player
        self.group_of_enemies = group_of_enemies

    # - Theme music
        pygame.mixer.music.load(r"music\maintheme.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1,0.0)

    # - Fonts
        self.angrybirds_font_40 = pygame.font.Font(r"fonts\AngryBirds.ttf",40)
        self.angrybirds_font_20 = pygame.font.Font(r"fonts\AngryBirds.ttf",20)

    # - Background image
        self.background_image = pygame.image.load("images/background.jpg")

    # - Images
        bluepig_img = pygame.image.load(r"images\Blue pig.png")
        greenpig_img = pygame.image.load(r"images\Green pig.png")
        pinkpig_img = pygame.image.load(r"images\Pink pig.png")
        yellowpig_img = pygame.image.load(r"images\Yellow pig.png")
        # - 0 = blue, 1 = green, 2 = pink, 3 = yellow
        self.enemies_images = [bluepig_img, greenpig_img, pinkpig_img, yellowpig_img]

    # - Creating pig we want to catch
        self.enemypig_type = random.randint(0,3)
        self.enemypig_image = self.enemies_images[self.enemypig_type]

        self.enemypig_image_rect = self.enemypig_image.get_rect()
        self.enemypig_image_rect.top = 50
        self.enemypig_image_rect.centerx = width//2

    # - Cycle code
    def update(self):
        self.slowdown_cycle +=1
        if self.slowdown_cycle == 120:
            self.round_time += 1
            self.slowdown_cycle = 0
        
        # Check collision
        self.collision_checker()

    # - Showing up objects
    def draw(self):
        darkred = (220,0,0)
        # - 0 = blue, 1 = green, 2 = pink, 3 = yellow
        blue = (0,128,255)
        green = (0,153,0)
        pink = (255,153,204)
        yellow = (255,255,0)

        colors = [blue,green,pink,yellow]

        # Text settings
        title_text = self.angrybirds_font_40.render("catch this pigger", True,colors[self.enemypig_type])
        title_rect = title_text.get_rect()
        title_rect.centerx = width//2
        title_rect.top = 10

        score_text = self.angrybirds_font_20.render(f"score: {self.score}", True, colors[self.enemypig_type])
        score_rect = score_text.get_rect()
        score_rect.topleft = (10,10)

        lives_text = self.angrybirds_font_20.render(f"lives: {self.our_player.lives}",True, colors[self.enemypig_type])
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (10,50)

        round_text = self.angrybirds_font_20.render(f"round: {self.round_number}", True, colors[self.enemypig_type])
        round_rect = round_text.get_rect()
        round_rect.topleft = (10,90)

        time_text = self.angrybirds_font_20.render(f"round time: {self.round_time}", True, colors[self.enemypig_type])
        time_rect = time_text.get_rect()
        time_rect.topright = (width-10, 10)

        safe_zone_count_text = self.angrybirds_font_20.render(f"Safe zones left: {one_player.safezones}",True,colors[self.enemypig_type])
        safe_zone_count_rect = safe_zone_count_text.get_rect()
        safe_zone_count_rect.topright = (width-10, 30)

        # Blitting text
        screen.blit(title_text,title_rect)
        screen.blit(score_text,score_rect)
        screen.blit(lives_text,lives_rect)
        screen.blit(round_text,round_rect)
        screen.blit(time_text,time_rect)
        screen.blit(safe_zone_count_text,safe_zone_count_rect)
        # Enemy pig type we want to catch
        screen.blit(self.enemypig_image,self.enemypig_image_rect)

        # Frame where can enemies move
        pygame.draw.rect(screen, colors[self.enemypig_type], (0,130,width,height-250), 4)

    # - Collision check (player / pig)
    def collision_checker(self):
        # With which enemies we collided
        collided_pig = pygame.sprite.spritecollideany(self.our_player, self.group_of_enemies)
        
        if collided_pig:
            if collided_pig.type == self.enemypig_type:
                # Score rises
                self.score += 10 * self.round_number
                # Removal of right enemy pig
                collided_pig.remove(self.group_of_enemies)
                # Sound
                self.our_player.catch_sound.play(0)
                # Do exist any other enemies of same time?
                if self.group_of_enemies:
                    self.target_selection()
                else:
                    # Round is finished
                    self.our_player.reset()
                    self.start_new_round()
            
            else:
                self.our_player.wrongcatch_sound.play(0)
                self.our_player.lives -=1
                # Is player alive?
                if self.our_player.lives <=0:
                    self.pause(f"your score: {self.score}, press enter if you want to play again", "press ENTER to continue")
                    self.reset()
                    self.our_player.reset()


    # - Starting new round with more pigs
    def start_new_round(self):
        # When is round finished, player will be awarded with extra points, rewards depends on round time
        self.score += int((100 * self.round_number) //1 + self.round_time)

        # Reseting values
        self.round_time = 0
        self.slowdown_cycle = 0
        self.round_number += 1
        self.our_player.safezones += 1

        # Deleting enemies, so we can fill it with new enemies
        for deleted_enemy in self.group_of_enemies:
            self.group_of_enemies.remove(deleted_enemy)

        for _ in range(self.round_number):
            self.group_of_enemies.add(Enemy(random.randint(72,width-72), random.randint(130,height-250),self.enemies_images[0],0))
            self.group_of_enemies.add(Enemy(random.randint(72,width-72), random.randint(130,height-250),self.enemies_images[1],1))
            self.group_of_enemies.add(Enemy(random.randint(72,width-72), random.randint(130,height-250),self.enemies_images[2],2))
            self.group_of_enemies.add(Enemy(random.randint(72,width-72), random.randint(130,height-250),self.enemies_images[3],3))

        # Selection of new target 
            self.target_selection()
    # - Choose new target
    def target_selection(self):
        new_enemy = random.choice(self.group_of_enemies.sprites())
        self.enemypig_type = new_enemy.type
        self.enemypig_image = new_enemy.image

    # - Pause - pause before starting new game
    def pause(self, main_text, subhead_text):

        global letsplay
        # colors settings
        darkred = (220,0,0)

        # Main text
        maintext = self.angrybirds_font_40.render(main_text, True, darkred)
        maintext_rect = maintext.get_rect()
        maintext_rect.center = (width//2, height//2)

        # Subtext
        subhead = self.angrybirds_font_20.render(subhead_text, True, darkred)
        subhead_rect = subhead.get_rect()
        subhead_rect.center = (width//2, height//2 + 50)

        # Main text and subtext blit
        screen.fill("black")
        screen.blit(maintext,maintext_rect)
        screen.blit(subhead,subhead_rect)
        pygame.display.update()

        # Stopping game
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                         paused = False
                if event.type == pygame.QUIT:
                    paused = False
                    letsplay = False

    # - Game reset
    def reset(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"images\Red.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width//2, height-80)

        self.lives = 5
        self.safezones = 3
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound(r"music\hitsound.wav")
        self.catch_sound.set_volume(0.1)

        self.wrongcatch_sound = pygame.mixer.Sound(r"music\lifelost.wav")
        self.wrongcatch_sound.set_volume(0.1)

    # - Code cycle
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= self.speed

        if keys[pygame.K_d] and self.rect.right <= width:
            self.rect.x += self.speed

        if keys[pygame.K_w] and self.rect.top >= 0:
            self.rect.y -= self.speed

        if keys[pygame.K_s] and self.rect.bottom <= height:
            self.rect.y += self.speed

    # - Return to safe zone
    def safe_zone(self):
        if self.safezones > 0:
            self.safezones -=1
            self.rect.center = (width//2, height-80)

    #  - Reset player position back to safe zone
    def reset(self):
        self.rect.center = (width//2, height-80)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x,y, image, enemy_type):
        super().__init__()

        # Image load
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        # Enemy type - 0 = blue, 1 = green, 2 = pink, 3 = yellow
        self.type = enemy_type

        # Setting of random enemy direction
        self.x = random.choice([-1,1])
        self.y = random.choice([-1,1])
        self.speed = random.randint(1,5)

    # Code cycle
    def update(self):
        # Movement of enemy
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        # Bounce of enemy
        if self.rect.left <= 0:
            self.x = -1* self.x
            
        if self.rect.right >= width:
            self.x = -1* self.x
            
        if self.rect.top <= 130:
            self.y = -1*self.y

        if self.rect.bottom >= height-120:
            self.y = -1*self.y

# TEST group of enemy
enemy_group = pygame.sprite.Group()

# TEST player group
player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

# Object Game()
letsplay = True
my_game = Game(one_player,enemy_group)
my_game.pause("Welcome to Angry Pigs", "pres ENTER to start")
my_game.start_new_round()
# Main cycle
while letsplay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            letsplay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                one_player.safe_zone()

    # - Screen fill
    screen.fill("black")
            
    # - Text draw
    my_game.update()
    my_game.draw()

    # - Update player group
    player_group.draw(screen)
    player_group.update()

    # - Update enemy group
    enemy_group.draw(screen)
    enemy_group.update()

    # - Update object Game()
    my_game.update()

    # - screen update
    pygame.display.update()

    # - cycle slow down
    clock.tick(fps)

# - GAME ENDING
pygame.quit()