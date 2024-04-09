import pygame as pyg
import random
import math

def set_speed(score, speed):

       
    if score == 0:
        speed = 7

    speed_change_thresholds = list(range(20, 10000, 40))

    for threshold in speed_change_thresholds:
        if score == threshold:
            speed += 1

    #speed += score / 0.5   #initialize speed

    #if speed > 12:  #set max speed
    #    speed = 12

    return speed

def draw_meteors(met_list, met_dim, screen, yellow):
    '''
    This function draws new meteors for each position
    inside of met_list. This is done every time the 
    screen is refreshed.
    '''
    for i in range(len(met_list)):
        print("met_list[i]", met_list[i], "length", len(met_list))  #delete later
        pyg.draw.rect(screen, yellow, (met_list[i][0], met_list[i][1], met_dim, met_dim)) #draw meteors at each position in met_list

def drop_meteors(met_list, met_dim, width, score):
    '''
   This function determines the locatoion of new meteors
   spawning it at the top of the screen. A random location
   on the x axis is generated with random module and the 
   coordinate pair is appened to met_list after checking
   if meteors overalp.
    '''

    sky_position = random.randrange(0, 800, 21) #get random sky position at top of board
    
    
    
    
    if score < 50:
        spawn_probability = .2  # 20% chance to spawn a meteor when score < 100
    else:
        spawn_probability = .3  # 50% chance to spawn a meteor when score >= 100

    # Determine whether to spawn a meteor based on the probability
    if random.random() > spawn_probability:
        return
      

    for i in range(len(met_list)):  #don't place meteors over each other
        if met_list[i][1] == sky_position:
           return    
    
    met_list.append([sky_position, 0])    #add new metor at that x position in the sky
    

def update_meteor_positions(met_list, height, score, speed):
    '''
    This function updates the position of the
    meteors y axis each frame by the pixel amount
    specified in the speed variable. It also checks
    if the meteors have reached the ground and if
    they have they are removed form the met_list 
    and a point of score is added.
    '''
    for i in range(len(met_list)):
        met_list[i][1] += speed #update y position of all meteors by speed

    for i, meteor in enumerate(met_list[:]):
        if meteor[1] > 600:
            del met_list[i] #remove meteor is it hits the ground
            score += 1      #plus one point for dodging meteor
  
    return score

def detect_collision(met_list, player_pos, player_dim, met_dim):
    '''
    This function is called within collision_check() and
    tests whether any meteors have collided with the 
    player. If yes it returns True, otherwise it returns 
    False.
    '''
    for i in range(len(met_list)):   #at this moment the function is checking if the corner of the player and the corner of the function are at the exact same location. We need to fix this so that it checks all locations of the drawn rectancgle are in contact with the locations of the metor. Perhaps we could do this with the outline of the meteor.
        
        met_position_list_x = []
        for j in range(met_dim):
            met_position_list_x.append(met_list[i][0] + j)  #list with all the x positions of the meteor
            #print(len(met_position_list))

        player_position_list_x = []
        for j in range(player_dim):
            player_position_list_x.append(player_pos[0] + j)  #list with all the x positions of the player0  [x, y]

        met_position_list_y = []
        for j in range(met_dim):
            met_position_list_y.append(met_list[i][1] + j)  #list with all the x positions of the meteor
            #print(len(met_position_list))

        player_position_list_y = []
        for j in range(player_dim):
            player_position_list_y.append(player_pos[1] + j)  #list with all the x positions of the player0  [x, y]

        x_collide = 'no'
        for j in player_position_list_x:  
            if j in met_position_list_x:  
                x_collide = 'yes'

        y_collide = 'No'
        for j in player_position_list_y:  
            if j in met_position_list_y:
                y_collide = 'yes'

        if x_collide == y_collide:
            return True

    return False

def collision_check(met_list, player_pos, player_dim, met_dim):
    '''
    This function calls detect_collison for every 
    position in met_list. detect_collision will either
    return True or False. This info is sent back to main
    to determine if game_over should remain false. 
    '''
    if detect_collision(met_list, player_pos, player_dim, met_dim):
        return True
    else:
        return False

def main():
    '''
    Initialize pygame and pygame parameters.  Note that both player and meteors
    are square.  Thus, player_dim and met_dim are the height and width of the
    player and meteors, respectively.  Each line of code is commented.
    '''
    pyg.init()                # initialize pygame

    width = 800               # set width of game screen in pixels
    height = 600              # set height of game screen in pixels

    red = (255,0,0)           # rgb color of player
    yellow = (244,208,63)     # rgb color of meteors
    background = (0,0,156)    # rgb color of sky (midnight blue)

    player_dim = 35           # player size in pixels
    player_pos = [width/2, height-2*player_dim]  # initial location of player
                                                 # at bottom middle; height
                                                 # never changes

    met_dim = 20              # meteor size in pixels
    met_list = []             # initialize list of two-element lists
                              # giving x and y meteor positions

    screen = pyg.display.set_mode((width, height)) # initialize game screen

    game_over = False         # initialize game_over; game played until
                              # game_over is True, i.e., when collision
                              # is detected

    score = 0                 # initialize score

    clock = pyg.time.Clock()  # initialize clock to track time

    my_font = pyg.font.SysFont("monospace", 35) # initialize system font

    speed = 0
    speed_add_accumulator = 0  
    
    while not game_over:                       # play until game_over == True
        speed_add_accumulator += 1
        for event in pyg.event.get():          # loop through events in queue
            if event.type == pyg.KEYDOWN:      # checks for key press
                x = player_pos[0]              # assign current x position
                y = player_pos[1]              # assign current y position
                if event.key == pyg.K_LEFT:    # checks if left arrow;
                    x -= player_dim            # if true, moves player left
                elif event.key == pyg.K_RIGHT: # checks if right arrow;
                    x += player_dim            # else moves player right
                player_pos = [x, y]            # reset player position
            
        screen.fill(background)                # refresh screen bg color
        drop_meteors(met_list, met_dim, width, score) # read PA prompt
        speed = set_speed(score, speed)               # read PA prompt
        score = update_meteor_positions(met_list, height, score, speed)
                                               # read PA prompt
        text = "Score: " + str(score)              # create score text
        label = my_font.render(text, 1, yellow)    # render text into label
        screen.blit(label, (width-250, height-40)) # blit label to screen at
                                                   # given position; for our 
                                                   # purposes, just think of
                                                   # blit to mean draw
        draw_meteors(met_list, met_dim, screen, yellow) # self-explanatory;
                                                        # read PA prompt

        pyg.draw.rect(screen, red, (player_pos[0], player_pos[1], player_dim, player_dim))# draw player

        if collision_check(met_list, player_pos, player_dim, met_dim):
            game_over = True                       # read PA prompt
    
        clock.tick(30)                             # set frame rate to control
                                                   # frames per second (~30); 
                                                   # slows down game

        pyg.display.update()                       # update screen characters
    # Outside while-loop now.
    print('Final score:', score)                   # final score
    pyg.quit()                                     # leave pygame

main()

