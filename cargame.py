import pygame
from pygame.locals import * 
import pygame.freetype
import time 
import random
import math


# Game Constants
GAME_DIMESIONS = (700,750)
BACK_GROUND_COLOR = (145,145,145)
CLOCK = pygame.time.Clock()
FRAME_RATE = 60
DIRECTION_CHANGE_BY = 30
TIME_FOR_GAME = 60000

VEHICLES = ["bluecar.png" ,"bus.png" ,"danfo.png" ,"motorbike.png" ,"tanker.png" ,"tricycle.png" ,"whitecar.png" ,"whitevan.png" ,"yellowtaxi.png"]
ACTORS = ["danfo.png","tricycle.png" , "motorbike.png" ]
ROAD_SIDE= ['grass.jpg']

class Road: 
    def __init__(self, parent_screen : pygame.surface , roadtype : int = 0) -> None:
        self.roadtype = roadtype
        self.road_side = pygame.image.load(f"assets/{ROAD_SIDE[roadtype]}")
        self.lane_divide = pygame.image.load("assets/lane_divide_1.png")
        self.parent_screen = parent_screen
    # function to draw road
    def draw(self) -> None: 
        self.parent_screen.blit(self.road_side,(-50,0)) # -50 , 0
        self.parent_screen.blit(self.road_side,(650,0)) #750 , 0
        for i in range(math.floor(GAME_DIMESIONS[1] / self.lane_divide.get_height())):
            self.parent_screen.blit(self.lane_divide,(250 - (self.lane_divide.get_width()/2), ( ( self.lane_divide.get_height() + 20) * i) ))
            self.parent_screen.blit(self.lane_divide,(450 - (self.lane_divide.get_width()/2), ( ( self.lane_divide.get_height() + 20) * i) ))
        pass

class Vehicle: 
    def __init__(self, parent_screen : pygame.surface , vechileid: int = 0 , x = GAME_DIMESIONS[0]/2) -> None:
        self.actor = pygame.image.load(f"assets/{VEHICLES[vechileid]}")
        self.parent_screen = parent_screen
        self.width = self.actor.get_width()
        self.height = self.actor.get_height()
        self.x = x
        self.y = GAME_DIMESIONS[1] - self.height - 10
    # function to draw case
    def draw(self) -> None: 
        self.parent_screen.blit(self.actor,(self.x , self.y))
         # pygame.display.flip()
        pass
    #Move car left 
    def move_right(self) -> None:
        if(self.x + DIRECTION_CHANGE_BY < GAME_DIMESIONS[0] - 50 - self.width):
            self.x += DIRECTION_CHANGE_BY
        self.draw()
        pass
    # Move car right 
    def move_left(self) -> None:
        if(self.x - DIRECTION_CHANGE_BY > 50):
            self.x -= DIRECTION_CHANGE_BY
        self.draw()
        pass
    
    #move car to random position 
    def move_random(self) -> None:
        random_number = random.randint(50,GAME_DIMESIONS[0] - 50 - self.width)
        # while random_number == self.x: 
        #     random_number = random.randint(50,GAME_DIMESIONS[0] - 50 - self.width)
        self.x = random_number
        pass


class Obstacles: 
    def __init__(self , parent_screen : pygame.surface , game_speed : int = 0.5) -> None:
        self.obstacles: list[tuple[float,float,float,float]] = []
        self.game_speed = game_speed
        self.parent_screen = parent_screen
        for i in range(3):
            obstacle_x = random.randint(50, GAME_DIMESIONS[0] - 70)
            obstacle_y = random.randint(-1000, -50)
            obstacle_speed = self.game_speed #random.randint(1, 3)
            obstacle_image_id = random.randint(0,len(VEHICLES) - 1)
            obstacle_image_height = 0
            obstacle_image_width = 0
            self.obstacles.append((obstacle_x, obstacle_y, obstacle_image_id , obstacle_speed , obstacle_image_width , obstacle_image_height  ))

    def draw(self) -> None: 
        # for obstacle_x, obstacle_y, obstacle_image_id , *rest in self.obstacles:
        for i, item in enumerate(self.obstacles):
            obstacle_x, obstacle_y, obstacle_image_id , *rest = item
            obstacle_image = pygame.image.load(f"assets/{VEHICLES[obstacle_image_id]}")
            self.obstacles[i] = self.obstacles[i][:-2] + (obstacle_image.get_width() , obstacle_image.get_height())
            self.parent_screen.blit(obstacle_image, (obstacle_x, obstacle_y))
         # pygame.display.flip()
        pass

    def move(self) -> None: 
        for i in range(len(self.obstacles)):
            obstacle_x, obstacle_y, obstacle_image_id , obstacle_speed , *rest  = self.obstacles[i]
            obstacle_y += obstacle_speed
            if obstacle_y > GAME_DIMESIONS[1]:
                obstacle_x = random.randint(50, GAME_DIMESIONS[0]-70)
                obstacle_y = random.randint(-1000, -50)
                obstacle_speed = self.game_speed #round(random.uniform(0.5, 3), 2) #random.randint(1, 3)
                obstacle_image_id = random.randint(0,len(VEHICLES) - 1)
            self.obstacles[i] = (obstacle_x, obstacle_y, obstacle_image_id , obstacle_speed) + self.obstacles[i][-2:]
        self.draw()
        pass

    
        
    pass


# creating the mathoperators
class Mathoperator: 
    def __init__(self , parent_screen : pygame.surface ,game: any, game_speed : int = 0.5 ,  ) -> None:

        self.mathoperators : list[tuple[float,float,float,float, bool]] = []
        self.game_speed = game_speed
        self.parent_screen = parent_screen
        self.font = pygame.font.SysFont(None, 40)
        self.radius = 25
        self.game = game
        self.color = (255, 0, 0) #change to gradient of the score
        self.list_operators_numbers = [str(i) for i in random.sample(range(self.game.target_number + 1),9)] + ['+','x','-', '÷']
        print(self.list_operators_numbers)
        for i in range(2):
            mathoperator_x = random.randint(50, GAME_DIMESIONS[0] - 70)
            mathoperator_y = random.randint(-1000, -50)
            mathoperator_speed = self.game_speed #random.randint(1, 3)
            mathoperator_id = random.randint(0,len(self.list_operators_numbers) - 1)
            mathoperator_value = self.list_operators_numbers[mathoperator_id]
            mathoperator_iscollided = False

            self.mathoperators.append((mathoperator_x, mathoperator_y, mathoperator_value  , mathoperator_speed , mathoperator_iscollided ))

    def draw(self) -> None: 
        temp_value = 'circle' #  'record'
        red = pygame.image.load(f"assets/{temp_value}-red.png")
        green = pygame.image.load(f"assets/{temp_value}-green.png")
        gray = pygame.image.load(f"assets/{temp_value}-gray.png")

        
        green = pygame.transform.scale(green,(50,50))
        red = pygame.transform.scale(red,(50,50))
        gray = pygame.transform.scale(gray,(50,50))


        for mathoperator_x, mathoperator_y ,mathoperator_value,  mathoperator_speed , mathoperator_iscollided in self.mathoperators:
            text_surface = self.font.render(mathoperator_value, True, (255,255,255))
            circle_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            
            pygame.draw.circle(circle_surface, self.color, (self.radius, self.radius), self.radius)
            
            if not mathoperator_value.isdigit(): 
                circle_surface.blit(gray,(0,0))
            # elif abs(self.game.target_number - self.game.my_number - int(mathoperator_value) ) > 5  :
            elif mathoperator_iscollided  :
                circle_surface.blit(green,(0,0))
            else:
                circle_surface.blit(red,(0,0))

            text_rect = text_surface.get_rect(center=(self.radius, self.radius))
            circle_surface.blit(text_surface, text_rect)

            self.parent_screen.blit(circle_surface, (mathoperator_x - self.radius, mathoperator_y - self.radius))
            
            pass

        pass

    def move(self) -> None: 
        for i in range(len(self.mathoperators)):
            mathoperator_x, mathoperator_y , mathoperator_value, mathoperator_speed , mathoperator_iscollided   = self.mathoperators[i]
            mathoperator_y += mathoperator_speed
            if mathoperator_y > GAME_DIMESIONS[1]:
                mathoperator_x = random.randint(50, GAME_DIMESIONS[0]-70)
                mathoperator_y = random.randint(-1000, -50)
                mathoperator_speed = self.game_speed  
                mathoperator_id = random.randint(0,len(self.list_operators_numbers) - 1)
                mathoperator_value = self.list_operators_numbers[mathoperator_id]
                mathoperator_iscollided = False
            self.mathoperators[i] = (mathoperator_x, mathoperator_y , mathoperator_value , mathoperator_speed , mathoperator_iscollided )
        self.draw()
        pass
    
    def update_operator_list(self) -> None:
        self.list_operators_numbers = [str(i) for i in random.sample(range(self.game.target_number + 1),9)] + ['+','x','-', '÷']

    
      
    

# Class for the game itself
class CarGame : 
    def __init__(self) -> None:
        # starting pygame
        pygame.init()
        pygame.mixer.init()
        self.CLOCK = pygame.time.Clock()
        # set caption 
        pygame.display.set_caption("9JA MATH RIDE")

        #score 
        self.score = 0

        #target number 
        self.target_number = random.randint(10,40)

        #my number
        self.my_number = 0

        # Set the initial time
        self.start_time = pygame.time.get_ticks()
        self.countdown_time = TIME_FOR_GAME  # 10 seconds in milliseconds
        self.time_left = TIME_FOR_GAME

        #scoring 
        self.last_update_time = pygame.time.get_ticks()
        
        
        # instance attributes 
        self.isrunning : bool = True

        # creating the surface of the game
        self.surface: pygame.surface = pygame.display.set_mode(GAME_DIMESIONS)
        
        #setting road 
        self.Road = Road(self.surface)

        #creating background
        self.render_background()


        #variables for math calculations 
        self.last_operator = '+'


        #Game State 
        self.gamestate = 0 # 0 : main menu ,  1 : game running , 2 : game ended , 3: game paused 

        

        #creating your vehicle
        self.vehicle = Vehicle(self.surface , 2)
        self.vehicle.draw()


        #creating math operators
        self.mathoperator = Mathoperator(self.surface, self)
        self.mathoperator.draw()

        #creating obstacles
        self.obstacles = Obstacles(self.surface)
        self.obstacles.draw()

        
        
        
       
        pass

    # reset game 

    def reset_game(self): 
        self.score = 0

        #target number 
        self.target_number = random.randint(10,40)

        #my number
        self.my_number = 0

        # Set the initial time
        self.start_time = pygame.time.get_ticks()
        self.countdown_time = TIME_FOR_GAME  # 10 seconds in milliseconds
        self.time_left = TIME_FOR_GAME

        #scoring 
        self.last_update_time = pygame.time.get_ticks()
        
        
        # instance attributes 
        self.isrunning : bool = True

        # creating the surface of the game
        self.surface: pygame.surface = pygame.display.set_mode(GAME_DIMESIONS)
        
        #setting road 
        self.Road = Road(self.surface)

        #creating background
        self.render_background()


        #variables for math calculations 
        self.last_operator = '+'


        #Game State 
        self.gamestate = 0 # 0 : main menu ,  1 : game running , 2 : game ended , 3: game paused 

        

        #creating your vehicle
        self.vehicle = Vehicle(self.surface , 2)
        self.vehicle.draw()


        #creating math operators
        self.mathoperator = Mathoperator(self.surface, self)
        self.mathoperator.draw()

        #creating obstacles
        self.obstacles = Obstacles(self.surface)
        self.obstacles.draw()

       
            

        pass

    # play game background music 
    def play_background_music(self) -> None:
        if not pygame.mixer.music.get_busy() and self.gamestate == 1:
            pygame.mixer.music.load("assets/sounds/urbansound.wav")
            pygame.mixer.music.play()

        pass

    # play sound 

    def playsound(self,sound) -> None:
        sound = pygame.mixer.Sound(f"assets/sounds/{sound}.wav")
        pygame.mixer.Sound.play(sound)
        pass

    def pause_background_music(self) -> None:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()


    # Rendering the background
    def render_background(self) -> None:
        self.surface.fill(BACK_GROUND_COLOR)
        self.Road.draw()
        
        pass

    #
    
    
    # if collision with obstacle 
    def is_collision(self , x1:float , y1:float , h1:float , w1:float , x2:float , y2:float , h2:float , w2:float) -> None:

        max_width = max(w1,w2)
        # if x1 >= x2 and (x1 < x2 + max_width or x2 < x1 + max_width):
        if (max_width == w1 and x2 >= x1 and x2 < x1 + w1 ) or (max_width == w2 and x1 >= x2 and x1 < x2 + w2 ):
            if y1 < y2 + h2:
                return True
        return False

    # display score

    def display_score(self) -> None:
        # font = pygame.font.SysFont('arial',30)
        font = pygame.freetype.Font(None, 32)
        image = pygame.image.load("assets/high-score.png")

        # Render the text with the emoji using the font object
        score, rect = font.render(f"{self.score}", (0,0,0))
        
        
        self.surface.blit(image,(GAME_DIMESIONS[0] -  score.get_width() - 140 ,20))
        self.surface.blit(score, (GAME_DIMESIONS[0] - score.get_width() - 100, 22))


    # display target score vs my score
    def display_target_my_score(self) -> None:
    
        font = pygame.freetype.Font(None, 32)

        target_image = pygame.image.load("assets/target.png")
        my_image = pygame.image.load("assets/smile.png")
        current_operator_image = pygame.image.load("assets/calculate.png")

        # Render the text with the emoji using the font object
        target, target_rect = font.render(f"{self.target_number}", (0,0,0))
        my, my_rect = font.render(f"{self.my_number}", (0,0,0))
        current_operator , current_operator_rect = font.render(f"{self.last_operator}", (0,0,0))
        divide, divide_rect = font.render(f":", (0,0,0))
        
        
        self.surface.blit(target_image,(50,20))
        self.surface.blit(target, (90, 22))

        self.surface.blit(divide, (90 + target.get_width() + 10, 24))

        self.surface.blit(my_image,(90 + target.get_width() + divide.get_width() + 20,20))
        self.surface.blit(my, ( 90 + target.get_width() + divide.get_width() +  60 , 22))
        
        self.surface.blit(current_operator_image,(50,60))
        self.surface.blit(current_operator, (90, 68))



    # display Landing page:

    def display_landing_page(self) -> None:
        bg = pygame.image.load('assets/mainBG.png')
        self.surface.blit(bg,(0,0))
        button = pygame.image.load('assets/greenbutton.png')
        font = pygame.font.SysFont('arial',30)
        buttonText = font.render("START",True , (0,0,0))
        self.surface.blit(button,(260,340))
        self.surface.blit(buttonText,(
            260 + (button.get_width()/2 - buttonText.get_width()/2),
            335 + (button.get_height()/2 - buttonText.get_height()/2)
        ))

        # Create a rectangle object manually
        button_rect = pygame.Rect(260, 340, button.get_width(), button.get_height())

        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_click == (1,0,0) and button_rect.colliderect(pygame.Rect(*mouse_pos, 1, 1)) and self.gamestate == 0:
            self.gamestate = 1

    # display gameover page
    def display_gameover_page(self) -> None:
        bg = pygame.image.load('assets/gameOver.png')
        self.surface.blit(bg,(0,0))

        score_font = pygame.font.SysFont('arial',50)

        score_text = score_font.render(f"Your Score : {self.score}",True , (0,0,0))

        self.surface.blit(score_text,(GAME_DIMESIONS[0]/2 - score_text.get_width()/2,240))

        button = pygame.image.load('assets/greenbutton.png')
        font = pygame.font.SysFont('arial',30)
        buttonText = font.render("RESTART",True , (0,0,0))
        self.surface.blit(button,(260,340))
        self.surface.blit(buttonText,(
            260 + (button.get_width()/2 - buttonText.get_width()/2),
            335 + (button.get_height()/2 - buttonText.get_height()/2)
        ))


        # Create a rectangle object manually
        button_rect = pygame.Rect(260, 340, button.get_width(), button.get_height())

        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_click == (1,0,0) and button_rect.colliderect(pygame.Rect(*mouse_pos, 1, 1)) and self.gamestate == 2:
            self.reset_game()
            self.gamestate = 1
            
    
    
    

        



    # tick timer 

    def tick_timer(self):
        self.time_left = self.countdown_time - (pygame.time.get_ticks() - self.start_time)
        # self.time_left = self.time_left - (pygame.time.get_ticks() - self.start_time)
        if self.time_left < 0:
            self.time_left = 0
        if self.time_left == 0: 
            self.gamestate = 2

        pass
   


    # display Timer

    def display_timer(self):
        # font = pygame.font.SysFont('arial',30)
        font = pygame.freetype.Font(None, 32)
        image = pygame.image.load("assets/stopwatch.png")

        # Render the text with the emoji using the font object
        timer, rect = font.render(f"{str(int(self.time_left / 1000))}", (0,0,0))
        
        
        self.surface.blit(image,(GAME_DIMESIONS[0]/2 - 40,20))
        self.surface.blit(timer, (GAME_DIMESIONS[0]/2, 22))
        pass

    
    # generate target number
    def generate_target_number(self) -> None:
        self.target_number = random.randint(10,40)
        pass

    
    # helper to update tuple 

    def update_tuple(self,old_tuple: tuple , index: int , value: any)-> tuple:
        temp_list = list(old_tuple)
        temp_list[index] = value 
        return tuple(temp_list)

    # update score 
    def update_score(self, score_addition ) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 3000:
            if (self.score + score_addition) < 1 :
                self.score = 0
            else: 
                self.score += score_addition
            
            self.last_update_time = current_time

    # decrease score 
    def  decrease_score(self, score_decrease) -> None:
        self.score -= score_decrease
        pass

    
    #pause Game 

    # display gameover page
    def display_pause_button(self) -> None:

        font = pygame.freetype.Font(None, 28)
        pause_image = pygame.image.load("assets/pause.png")
        pause, pause_rect = font.render("Pause", (0,0,0))

        self.surface.blit( pause_image,(GAME_DIMESIONS[0] -  pause.get_width() - 140 ,60))
        self.surface.blit( pause, (GAME_DIMESIONS[0] - pause.get_width() - 100, 65))

        

        # self.surface.blit(score_text,(GAME_DIMESIONS[0]/2 - score_text.get_width()/2,240))

        # button = pygame.image.load('assets/greenbutton.png')
        # font = pygame.font.SysFont('arial',10)
        # buttonText = font.render("Pause",True , (0,0,0))
        # self.surface.blit(button,(260,340))
        # self.surface.blit(buttonText,(
        #     260 + (button.get_width()/2 - buttonText.get_width()/2),
        #     335 + (button.get_height()/2 - buttonText.get_height()/2)
        # ))


        # Create a rectangle object manually
        pause_rect = pygame.Rect(
            (GAME_DIMESIONS[0] - pause.get_width() - 140)
            , 60, pause_image.get_width() + 40 + pause.get_width(),  pause_image.get_height() + 40 + pause.get_height())

        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_click == (1,0,0) and pause_rect.colliderect(pygame.Rect(*mouse_pos, 1, 1)) and self.gamestate == 1: 
            print('paused')
            self.gamestate = 3




    # display pause screen

    def display_pause_page(self) -> None:
        bg = pygame.image.load('assets/gamePause.png')
        self.surface.blit(bg,(0,0))

        score_font = pygame.font.SysFont('arial',50)

        score_text = score_font.render(f"Your Score : {self.score}",True , (0,0,0))

        self.surface.blit(score_text,(GAME_DIMESIONS[0]/2 - score_text.get_width()/2,240))

        button = pygame.image.load('assets/greenbutton.png')
        font = pygame.font.SysFont('arial',30)
        buttonText = font.render("UNPAUSE",True , (0,0,0))
        self.surface.blit(button,(260,340))
        self.surface.blit(buttonText,(
            260 + (button.get_width()/2 - buttonText.get_width()/2),
            335 + (button.get_height()/2 - buttonText.get_height()/2)
        ))


        # Create a rectangle object manually
        button_rect = pygame.Rect(260, 340, button.get_width(), button.get_height())

        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_click == (1,0,0) and button_rect.colliderect(pygame.Rect(*mouse_pos, 1, 1)) and self.gamestate == 3:
            self.gamestate = 1
            print("working")



    # start game 
    def play (self) -> None: 
        self.play_background_music()
        if self.gamestate == 0 :
            self.display_landing_page()
        elif self.gamestate == 2: 
            self.pause_background_music()
            self.display_gameover_page()
        elif self.gamestate == 3:
            self.display_pause_page()
        else:
            self.render_background()
            self.tick_timer()
            self.vehicle.draw()
            self.mathoperator.move()
            self.obstacles.move()
            self.display_score()
            self.display_target_my_score()
            self.display_timer()
            self.display_pause_button()
            self.update_score(1)
            for item in self.obstacles.obstacles:
                if(self.is_collision(self.vehicle.x, self.vehicle.y , self.vehicle.height , self.vehicle.height,item[0], item[1], item[5],item[4])):
                    # display that you have been hit 
                    self.playsound("carhit")
                    self.vehicle.move_random()
                    self.decrease_score(3)
                    pass
                pass
            for index , item in enumerate(self.mathoperator.mathoperators):
                if( self.is_collision(self.vehicle.x, self.vehicle.y , self.vehicle.height , self.vehicle.height,item[0], item[1], self.mathoperator.radius,self.mathoperator.radius) and not item[4] ):
                    self.mathoperator.mathoperators[index] =  self.update_tuple(item,4,True)
                    self.playsound("bubbletouch")
                    if item[2].isdigit():
                        #update score 
                        self.score += 5
                        # update timer 
                        self.countdown_time += 5000
                        if self.last_operator == "+":
                            self.my_number += int(item[2])
                            pass
                        elif self.last_operator == "x":
                            self.my_number = int(self.my_number * int(item[2]))
                            pass 
                        elif self.last_operator == "-":
                            self.my_number -= int(item[2])
                            pass 
                        elif self.last_operator == "÷":
                            self.my_number = int(self.my_number / int(item[2]))
                            pass
                        else: 
                            pass 
                    else: 
                        #update score 
                        self.score += 2
                        self.last_operator = item[2]

                    pass 
                    self.mathoperator.update_operator_list()
                pass
            if self.my_number == self.target_number: 
                self.generate_target_number()
        pygame.display.flip()

        pass
    
    
    
    # the runn function for the game (the event loop)

    def run(self) -> None: 
        while self.isrunning: 
            for event in pygame.event.get():
                # quiting the game 
                if event.type == pygame.QUIT:
                    self.isrunning = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                #movement 
                    if event.key == K_LEFT and self.gamestate == 1:
                        self.vehicle.move_left()
                        
                    if event.key == K_RIGHT and self.gamestate == 1:
                        self.vehicle.move_right()  
            self.play()   
            pass
        self.CLOCK.tick(FRAME_RATE)
        pass

if __name__  == "__main__":
    game = CarGame()
    game.run()
    pass