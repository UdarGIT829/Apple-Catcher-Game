#Import Standard libraries
import os, sys, math, time, pygame, pygame.mixer
import random
from pygame.locals import *
import euclid
#Import selfmade files
import appleClass

#Define Colors
black = 0, 0, 0
white = 255, 255, 255
red = 230, 25, 0
green = 0, 255, 0
blue = 0, 0, 255
#Define custom colors
green_skin = 10, 235, 10
stemColor = 175, 105, 0
goldenrod = 218,165,32
applecolors = red, green_skin, goldenrod

#Define Screen Size
screen_size = screen_width, screen_height = 600, 400

#Initialize Pygame
pygame.init()
#Set Display
screen = pygame.display.set_mode(screen_size)
#Define background image
bg = pygame.image.load("bg.png")
#Define Title image-text
titleIm = pygame.image.load("Title.png")
titleIm_width, titleIm_height = titleIm.get_size()
title_location = ((screen_width//2)-titleIm_width//2,screen_height//4-titleIm_height//2)
#Define Start image-text
startIm = pygame.image.load("Start.png")
startIm_width, startIm_height = startIm.get_size()
startIm_location = ((screen_width//2)-startIm_width//2,(screen_height//2)+startIm_height//(3/2))
#Define Initialization image-text
initializingIm = pygame.image.load("Initializing.png")
initializingIm_width, initializingIm_height = initializingIm.get_size()
initializingIm_location = ((screen_width//2)-initializingIm_width//2,(screen_height//4)-initializingIm_height//(3/2))
#Define quit button
quitButton = pygame.image.load("bitApple.png")
quitButton_width, quitButton_height = quitButton.get_size()
quitButton_location = (screen_width-(1.4*quitButton_width),2)
#Define Quit image-text
quitLabel = pygame.image.load("Quit.png")
quitLabel_width, quitLabel_height = quitLabel.get_size()
quitLabel_location = (screen_width-quitLabel_width, 2*quitLabel_height -5)
#Define Help buttons
help_button_image = pygame.image.load("Help.png")
title_help_image = pygame.image.load("TitleHelpMessage.png")
game_help_image = pygame.image.load("GameHelpMessage.png")
post_help_image = pygame.image.load("PostHelpMessage.png")
win_help_image = pygame.image.load("WinHelpMessage.png")
help_button_width, help_button_height = help_button_image.get_size()
help_button_location = (2,screen_height-(help_button_height+2))
display_help_location = (50,250)
title_help_button = appleClass.helpButton(help_button_location,help_button_width,help_button_image, title_help_image, display_help_location)
game_help_button = appleClass.helpButton(help_button_location,help_button_width,help_button_image, game_help_image, display_help_location)
post_help_button = appleClass.helpButton(help_button_location,help_button_width,help_button_image, post_help_image, display_help_location,win_help_image)

#Get clock
clock = pygame.time.Clock()
#Set Window Title
pygame.display.set_caption('Apple Catcher!')
#Set audio track
pygame.mixer.init()
pygame.mixer.music.load("The Calling - Angelwing.ogg")
def play_music():
    pygame.mixer.music.play(-1)

#Define FPS and when to stay open
fps_limit = 1000
run_me = True

#Limit the framerate
dtime_ms = clock.tick(fps_limit)
dtime = dtime_ms/1000.0

#Set general vars for apples
initial_velocity = 1

#Define randomness functions for apple
def get_random_velocity():
    new_angle = random.uniform((31*math.pi/16),(33*math.pi/16))
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = euclid.Vector2(new_x,new_y)
    new_vector.normalize()
    new_vector *= 20
    return new_vector

#Define function for playbutton to be an apple
def playbutton_apple_generator():
    uid = -1
    size = 14
    x = screen_width//2
    y = screen_height//2
    location = (x,y)
    color = applecolors[random.randint(0,len(applecolors)-1)]
    velocity = 0
    playbutton = appleClass.MyApple(euclid.Vector2(x,y),(x,y),size,dtime,uid,color,stemColor,velocity,0)
    return playbutton

def quitbutton_apple_generator(location):
    uid = -3
    size = 14
    x = location[0]+int(size*1.5) +3
    y = location[1]+int(size*1.5) +3
    color = applecolors[random.randint(0,len(applecolors)-1)]
    velocity = 0
    quitbutton = appleClass.MyApple(euclid.Vector2(x,y),(x,y),size,dtime,uid,color,stemColor,velocity,0)
    return quitbutton

#Define function to generate a random apple
def drop_random_apple(uid):
    size = random.randint(7,14)
    x = random.randint(size*5, screen_width-(size*5))
    y = random.randint(size,3*size)
    location = (x,y)
    color = applecolors[random.randint(0,len(applecolors)-1)]
    velocity = get_random_velocity()
    new_rand_apple = appleClass.MyApple(euclid.Vector2(x,y),(x,y),size,dtime,uid,color,stemColor,velocity,0)
    return new_rand_apple

#Define initialization timing system so it doesnt run too fast or slow
def timing_system_begin():
    timing_apple = drop_random_apple(-2)
    return timing_apple

#Add certain amount of apples randomly using above function
rand_apples = []
amount_of_apples = 2
counter = 1
def setup_apples_to_drop(amount_of_apples,rand_apples,counter):
    for n in range(amount_of_apples):
        new_apple = drop_random_apple(counter)
        rand_apples.append(new_apple)
        counter += 1
    return rand_apples,counter

# Define scenes here, as well as assorted scene-based variables
screen_fill = black
scene = 1
play_button = playbutton_apple_generator()
quitButton_apple = quitbutton_apple_generator(quitButton_location)
timing_apple = play_button
last_time = time.time()
last_position = drop_random_apple(-2).position.y
timing_mod = 1000.0
speed_range = (0,0)
ready_to_play = False
gameEndCounter = 0
show_help_flag = False

def timing_scene(timing_mod,curr_position, last_position,last_time,scene, optimal_range):
    now_time = time.time()
    time_diff = int((now_time - last_time)*1000)
    position_diff = int((curr_position - last_position)*100)
    
    if(position_diff < optimal_range[0]):
        timing_mod -= 3
        print(position_diff, " too slow for ", optimal_range[0])
    elif(position_diff > optimal_range[1]):
        timing_mod += 3
        print(position_diff, " too fast for ", optimal_range[1])
    if((position_diff >= optimal_range[0]) and (position_diff <= optimal_range[1])):
        scene = 2
        print("Try change scene")
    return timing_mod, curr_position,now_time, scene

def title_scene(scene, show_help_flag):
    speed_range = (25,25)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run_me = False
        mouse = pygame.mouse.get_pressed()
        if(mouse != (0,0,0)):
            mouse_loc = pygame.mouse.get_pos()
            if(quitButton_apple.would_catch(mouse_loc)):
                sys.exit()
            elif(play_button.would_catch(mouse_loc)):
                scene = -1
                print("Timing scene start")
                if(mouse == (1,0,0)):
                    speed_range = (25,60)
                else:
                    speed_range = (85, 120)
            elif(title_help_button.would_show(mouse_loc)):
                if(show_help_flag == True):
                    show_help_flag = False
                else:
                    show_help_flag = True
            
    return scene, speed_range, show_help_flag

def main_game_scene(rand_apples, amount_of_apples, first_click, scene, show_help_flag, counter):
    #Start music
    if(pygame.mixer.music.get_busy() == False):
        play_music()
    #Check if apples are ready to drop, if not populate
    if(len(rand_apples) == 0 and counter == 1):
        counter = 1
        rand_apples, counter = setup_apples_to_drop(amount_of_apples,rand_apples, counter)
    
    #Click event loop
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pressed()
        #Help button takes priority
        if(mouse == (1,0,0) and game_help_button.would_show(pygame.mouse.get_pos())):
            if(show_help_flag == True):
                show_help_flag = False
            else:
                show_help_flag = True
        #Do not start until player clicks onscreen once
        elif(mouse == (1,0,0) and first_click == False):
            first_click = True
        #For all left clicks after first...
        elif(mouse == (1,0,0) and first_click):
            #Get location of mouse
            mouse_loc = pygame.mouse.get_pos()
            #Use a variable to track down closest apple
            greedyMinDist = sys.maxsize


            #Loop through apples
            for apple in rand_apples:
                #Check if this apple would be caught
                will_catch = apple.would_catch(mouse_loc)
                
                if(will_catch and show_help_flag == False):
                    # Get distance to closest apple
                    appleDist = apple.distance_to_point(mouse_loc)
                    #Compare with variable and cycle through apples to find closest one to click
                    if(appleDist < greedyMinDist):
                        closestApple = apple
                        greedyMinDist = appleDist
                    #Remove the closest catchable apple
                    print("Caught Apple # ", closestApple.uid)
                    rand_apples.remove(closestApple)
                    #Finish game when all apples caught
                    if(len(rand_apples) == 0):
                        scene = 3
                        first_click = False
                        while(pygame.mouse.get_pressed() == (1,0,0)):
                            pygame.event.get()
                            pygame.mouse.get_pressed()
                    break
            # If left-click noticed at any time, after checking apples wait until left click no longer seen
            while(pygame.mouse.get_pressed()==(1,0,0)):
                pygame.event.get()
                pygame.mouse.get_pressed()
    return first_click, scene, show_help_flag

def post_game_scene(scene, amount_of_apples, speed_range, gameEndCounter):
    new_speed_range = speed_range
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run_me = False
        mouse = pygame.mouse.get_pressed()
        if(mouse == (1,0,0)):
            mouse_loc = pygame.mouse.get_pos()
            if(quitButton_apple.would_catch(mouse_loc)):
                sys.exit()
            if(gameEndCounter == 7):
                scene = 1
                gameEndCounter = 0
            else:
                scene = -1
                low_end_speed, high_end_speed = speed_range
                if(low_end_speed < 165):
                    new_low_end_speed = low_end_speed + 10
                    new_high_end_speed = high_end_speed + 10
                    new_speed_range = (new_low_end_speed, new_high_end_speed)
                else:
                    amount_of_apples += 1
                gameEndCounter += 1
                amount_of_apples += 1
    return scene, amount_of_apples, new_speed_range, gameEndCounter

#Define Scene switcher
current_scene = title_scene
def scene_switcher(scene):
    scene_dictionary = {
        -1: timing_scene,
        1: title_scene,
        2: main_game_scene,
        3: post_game_scene
    }
    function = scene_dictionary.get(scene, "nothing")
    if(current_scene != function):
        pygame.time.wait(1)
    return function

current_scene = scene_switcher(scene)

# Game Loop here
while run_me:
    current_scene = scene_switcher(scene)
    #Set background
    screen.blit(bg,(0,0))

    #Clear the screen
    if current_scene == title_scene:
        scene, speed_range, show_help_flag = current_scene(scene, show_help_flag)
        #Display Title, Quit button, and Start-Label
        screen.blit(titleIm,title_location)
        screen.blit(quitButton,quitButton_location)
        screen.blit(quitLabel, quitLabel_location)
        screen.blit(startIm,startIm_location)
        title_help_button.display(screen)
        if(show_help_flag):
            title_help_button.display_help(screen)
    elif current_scene == main_game_scene:
        ready_to_play, scene, show_help_flag = current_scene(rand_apples, amount_of_apples, ready_to_play, scene, show_help_flag, counter)
        game_help_button.display(screen)
        if(show_help_flag):
            game_help_button.display_help(screen)
    elif current_scene == timing_scene:
        #Display Initializing-Label
        screen.blit(initializingIm,initializingIm_location)
        timing_mod, last_position,last_time, scene = current_scene(timing_mod,timing_apple.position.y,last_position,last_time,scene, speed_range)
        dtime = dtime_ms/timing_mod
        timing_apple.dtime = dtime
    elif current_scene == post_game_scene:
        scene, amount_of_apples, speed_range, gameEndCounter = current_scene(scene, amount_of_apples, speed_range, gameEndCounter)
        post_help_button.display(screen)
        screen.blit(quitButton,quitButton_location)
        screen.blit(quitLabel, quitLabel_location)
        if(gameEndCounter < 7):
            post_help_button.display_help(screen)
        else:
            post_help_button.display_sec_help(screen)

    
    #Lock screen for memory things
    screen.lock()

    #Put display calls here before the display flip call

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run_me = False
    if(current_scene == title_scene):
        play_button.display(screen)
    elif(current_scene == timing_scene):
        if(timing_apple == play_button):
            timing_apple = timing_system_begin()
            timer = int(time.time())
        else:
            timing_apple.display(screen)
            timing_apple.move()
            if(timing_apple.position.y > screen_height):
                timing_apple.position.y = drop_random_apple(timing_apple.uid).position.y
    elif(current_scene == main_game_scene):
        for apple in rand_apples:
            apple.display(screen)
            if(apple.position.y > screen_height):
                new_apple = drop_random_apple(apple.uid)
                rand_apples.append(new_apple)
                rand_apples.remove(apple)
                break
            if(ready_to_play and show_help_flag == False):
                apple.move()

    #Display everything in the screen
    screen.unlock()
    pygame.display.flip()

#Quit the game
pygame.quit()
sys.exit()