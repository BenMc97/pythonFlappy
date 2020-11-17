import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 720))
    screen.blit(floor_surface, (floor_x_pos+576, 720))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=800:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 720:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(288,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score = {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score = {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 100))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score
    if pipe_list:
        for pipe in pipe_list:
            if 95< pipe.centerx <105:
                score += 0.5
                score_sound.play()



pygame.init()
pygame.display.set_caption('Flappy')
screen = pygame.display.set_mode((576,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Flappy-font/04B_19.TTF',25)
welcome_font = pygame.font.Font('Flappy-font/04B_19.TTF',60)
press_play_font = pygame.font.Font('Flappy-font/04B_19.TTF',40)


#Game variables
playing='menu'
gravity = 0.3
bird_movement = 0
game_active = True
score = 0
high_score = 0

menu_surface=pygame.image.load('Flappy-imgs/background-night.png')
menu_surface=pygame.transform.scale2x(menu_surface)

bg_surface=pygame.image.load('Flappy-imgs/background-night.png')
bg_surface=pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('Flappy-imgs/base.png')
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bluebird_downflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/bluebird-downflap.png'))
bluebird_midflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/bluebird-midflap.png'))
bluebird_upflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/bluebird-upflap.png'))

yellowbird_downflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/yellowbird-downflap.png'))
yellowbird_midflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/yellowbird-midflap.png'))
yellowbird_upflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/yellowbird-upflap.png'))


redbird_downflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/redbird-downflap.png'))
redbird_midflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/redbird-midflap.png'))
redbird_upflap = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/redbird-upflap.png'))
bird_frames = [redbird_downflap,redbird_midflap, redbird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100,400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('Flappy-imgs/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height=[400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/gameover.png'))
game_over_rect = game_over_surface.get_rect(center=(288,400))

flap_sound = pygame.mixer.Sound('Flappy-sounds/sfx_wing.wav')
flap_sound.set_volume(0.05)

hit_sound = pygame.mixer.Sound('Flappy-sounds/sfx_hit.wav')
hit_sound.set_volume(0.05)

score_sound = pygame.mixer.Sound('Flappy-sounds/sfx_point.wav')
score_sound.set_volume(0.01)

menu_sound = pygame.mixer.Sound('Flappy-sounds/background_music.wav')
menu_sound.set_volume(0.025)


while True:
    while playing == 'menu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = 'choose_bird'

        screen.blit(menu_surface, (0, 0))

        menu_sound.play()



        bluebird_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/bluebird-midflap.png'))
        bluebird_rect = bluebird_surface.get_rect(center=(288, 100))
        screen.blit(bluebird_surface, bluebird_rect)

        redbird_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/redbird-midflap.png'))
        redbird_rect = redbird_surface.get_rect(center=(144, 200))
        screen.blit(redbird_surface, redbird_rect)

        yellowbird_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/yellowbird-midflap.png'))
        yellowbird_rect = yellowbird_surface.get_rect(center=(432, 200))
        screen.blit(yellowbird_surface, yellowbird_rect)

        welcome_surface = welcome_font.render('Welcome', True, (255, 255, 255))
        welcome_rect = welcome_surface.get_rect(center=(300, 300))
        screen.blit(welcome_surface, welcome_rect)

        press_play_surface = press_play_font.render('Press Space Bar To Play', True, (255, 255, 255))
        press_play_rect = welcome_surface.get_rect(center=(175, 400))
        screen.blit(press_play_surface, press_play_rect)

        pygame.display.update()
        clock.tick(70)

    while playing == 'choose_bird':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    bird_frames[0] = redbird_downflap
                    bird_frames[1] = redbird_midflap
                    bird_frames[2] = redbird_upflap

                if event.key == pygame.K_b:
                    bird_frames[0] = bluebird_downflap
                    bird_frames[1] = bluebird_midflap
                    bird_frames[2] = bluebird_upflap

                if event.key == pygame.K_c:
                    bird_frames[0] = yellowbird_downflap
                    bird_frames[1] = yellowbird_midflap
                    bird_frames[2] = yellowbird_upflap
                playing = 'play_game'

        screen.blit(menu_surface, (0, 0))

        bluebird_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/bluebird-midflap.png'))
        bluebird_rect = bluebird_surface.get_rect(center=(288, 400))
        screen.blit(bluebird_surface, bluebird_rect)

        bluebird_play_surface = press_play_font.render('B', True, (255, 255, 255))
        bluebird_play_rect = bluebird_play_surface.get_rect(center=(288, 500))
        screen.blit(bluebird_play_surface, bluebird_play_rect)

        redbird_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/redbird-midflap.png'))
        redbird_rect = redbird_surface.get_rect(center=(144, 400))
        screen.blit(redbird_surface, redbird_rect)

        redbird_play_surface = press_play_font.render('A', True, (255, 255, 255))
        redbird_play_rect = redbird_play_surface.get_rect(center=(144, 500))
        screen.blit(redbird_play_surface, redbird_play_rect)

        yellowbird_surface = pygame.transform.scale2x(pygame.image.load('Flappy-imgs/yellowbird-midflap.png'))
        yellowbird_rect = yellowbird_surface.get_rect(center=(432, 400))
        screen.blit(yellowbird_surface, yellowbird_rect)

        yellowbird_play_surface = press_play_font.render('C', True, (255, 255, 255))
        yellowbird_play_rect = yellowbird_play_surface.get_rect(center=(432, 500))
        screen.blit(yellowbird_play_surface, yellowbird_play_rect)

        welcome_surface = welcome_font.render('Pick Your Bird', True, (255, 255, 255))
        welcome_rect = welcome_surface.get_rect(center=(315, 300))
        screen.blit(welcome_surface, welcome_rect)

        pygame.display.update()
        clock.tick(70)

    while playing == 'play_game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 7
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 400)
                    bird_movement = 0
                    score = 0
                if event.key == pygame.K_x and game_active == False:
                    game_active = True
                    playing = 'menu'
                    pipe_list.clear()
                    bird_rect.center = (100, 400)
                    bird_movement = 0
                    score = 0
                    high_score = high_score

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

                bird_surface, bird_rect = bird_animation()

        screen.blit(bg_surface, (0, 0))

        menu_sound.stop()

        if game_active:
            # Bird
            bird_movement += gravity
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)

            # Pipes
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            pipe_score_check()
            score_display('main_game')

        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')

            play_on_surface = game_font.render('Press Space Bar To Play Again', True, (255, 255, 255))
            play_on_rect = play_on_surface.get_rect(center=(280, 500))
            screen.blit(play_on_surface, play_on_rect)

            back_to_menu_surface = game_font.render('Or Press x To Return To Menu', True, (255, 255, 255))
            back_to_menu_rect = back_to_menu_surface.get_rect(center=(280, 600))
            screen.blit(back_to_menu_surface, back_to_menu_rect)

        # Floor
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(70)


