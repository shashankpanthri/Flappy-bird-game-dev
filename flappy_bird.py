# the main imports
import pygame, random



# some important functions



# for creating pipe rectangles which will store the pipe images
def create_pipe():
    height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350, height))
    top_pipe = pipe_surface.get_rect(midbottom = (350, height-150))
    return bottom_pipe, top_pipe

# to move pipes from right to left of the screen
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes


# drawing the pipes with rectanges
def draw_pipes(pipes):
    for pipe in pipes:
        # only the bottom pipe can have the bottom point going below the screen 
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            # flip the surface using inbuilt function
            # takes the surface and two bool values corresponding to the flip across x axis and flip through y axis
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            
            
# detecting collisions
def check_collision(pipes):
    for pipe in pipes:
        # if bird rectangle collides with any of the pipe rectangle 
        if bird_rect.colliderect(pipe):
            collision_sound.play()
            return False
    #we also want collision when the bird is too high or too low
    if bird_rect.bottom >= 450 or bird_rect.top <=-50:
        return False
    return True                

# bird movement animation
def rotate_bird(bird):
    # the first is the bird surface you want to rotate
    # the angle of the rotation - value is added so that is rotated in the right direction
    # to see the rotation is more visible it is multiplied by 3
    # the scale is not used and is kept the default i.e.1
    # the bird_movement will control where the angle of the rotation will be
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird


# flap animation
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

# base movement from right to left
def base_animation():
    # just one image was not doing the right thing, it was moving to the left and
    #going off the screen and then coming back to make up for that
    # we add another image at the end of the first one
    screen.blit(base_surface, (base_x_position,450))
    screen.blit(base_surface, (base_x_position+288 , 450))
    
# see the score
def display_score(game_state):
    # if game is running
    if game_state == 'current_game':
        # now we render the font in the screen
        # first the text to be displayed
        # anti aliasing - characters of the characters will be smooth edges if it is set to true
        # color of the text
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)
    
    # if game has ended
    if game_state == 'game_over':
        # normal score
        score_surface = game_font.render(f'Score:{int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)
        
        #highest score
        high_score_surface = game_font.render(f'High Score:{int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface, high_score_rect)
    
    
# updating the score 
def update_score(score, high_score):
    if score> high_score:
        high_score = score
    return high_score



# initializations



# we initialize the mixer module to get rid of the delay in the processing of the sound 
# when we want to play the sound
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

# initialize the module
pygame.init()


# variable initializations and main screen display



# the main display surface with its size
screen = pygame.display.set_mode((288, 512))
#module to make the frame rate even
clock = pygame.time.Clock()
# game font
game_font = pygame.font.Font('04B_19.TTF', 40)

#convert at the end makes the image a little
#more friendly for pygame to run and it will be faster

# the background image for the game
bg_surface = pygame.image.load('assets/background-day.png').convert()
# the base image for the background (the little part at the bottom)
base_surface = pygame.image.load('assets/base.png').convert()

# game over surface
game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

# for the birds with their different flap positions 
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50,256))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collision_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# if I wanted to make a bigger screen and fit the smaller image in it, I would have to 
# rescale the image to be twice of what it is
# basically uncomment this if you make the display screen any bigger
# bg_surface = pygame.transform.scale2x(bg_surface)

BIRDFLAP = pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP, 200)

# for pipes
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()

# we are going to create a new pipe list which will contain a number of rectangles 
# containing the pipes 
pipe_list = []
# user event is not triggered by a button but is triggered by a timer
SPAWNPIPE = pygame.USEREVENT
# the timer
pygame.time.set_timer(SPAWNPIPE, 1200)
# for random height
pipe_height = [200,300,400,250,350]

run = True
# for the base image position, to make it move to the left
base_x_position = 0
# for the bird to fall down
gravity = 0.1
bird_movement = 0
# the game state
game_active = True
# for scores
score = 0
high_score = 0



# the main game loop



while run:
    # checks for any event happening and gets it from the event queue
    for event in pygame.event.get():
        # if the event is pressing the X button on top of the window
        if event.type == pygame.QUIT:
                #get out of the while loop
                run = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
                
            if event.key == pygame.K_SPACE and game_active==False:
                # get the game to start again
                game_active = True
                # clear the previous game pipes
                pipe_list.clear()
                # set the bird to the original default position
                bird_rect.center = (50, 256)
                # set the movement to be default too
                bird_movement = 0
                # set the score to be 0
                score = 0
                
        if event.type == SPAWNPIPE:
            # a function to make rectangles with pipes and put them into list
            pipe_list.extend(create_pipe())
            
        if event.type == BIRDFLAP:
            if bird_index<2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
            
    # set the frame rate 
    clock.tick(120)
    
    # a function to put any image on the surface
    # takes the image, and the position on where to put the image on
    # 0,0 is the top left corner of the screen
    screen.blit(bg_surface, (0,0))
   
    # if game is running
    if game_active == True:
        # make the bird fall
        bird_movement += gravity
        # bird animation
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        #place the bird 0n the surface
        screen.blit(rotated_bird, bird_rect)
        #check for collisions
        game_active = check_collision(pipe_list)
        # for pipe movement
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        # increase the score
        score += .01
        # sound for score
        score_sound_countdown -= 1
        # the main score sound
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
        display_score('current_game')
        
    # game has ended and the game over screen is shown
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        display_score('game_over')

    # for the base animation to constantly move backwards we implement a funtion
    base_animation()
    # make the base_x_position to go -1 everytime the loop is called again
    base_x_position -= 1
    # if it goes out of the screen then reset the value
    if base_x_position<= -288:
        base_x_position = 0
    
    # update the display window and add anything that was done in the main game loop
    pygame.display.update()    
    
# if the main loop is over then quit the pygame module
# without this the X button on top of the window will not work 
pygame.quit()    