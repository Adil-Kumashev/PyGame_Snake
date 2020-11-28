import pygame   # grants access to PyGame framework 
import time     # setting pause in game
import sys
import random    # generates food for our snake
import pygame_menu  # for creating menu of the game


screenWIDTH = 440
screenHEIGHT = 490

RED = (255, 0, 0)   # preparing some colour codes
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
FILLING_COLOUR = (255,210,230)
SNAKE_COLOUR = (240,230,140)
APPLE_COLOUR = (220,20,60)
HEAD_COLOUR = (205,133,63)

x1 = 0     # assigning starting position of the  character
y1 = 30
x2 = 15
y2 = 15

vel = 5     # assigning speed of the character

row_num = 20  # fixing the number, size and margin between blocks on field
column_num = 20
block_size = 20
margin_width = 1
SCORE_TABLOID = 60





pygame.init()   # initialize all modules we need

back_ground = pygame.image.load("theme.jpg")

timer = pygame.time.Clock()

font = pygame.font.SysFont('Times New Roman', 20)

screen = pygame.display.set_mode((screenWIDTH, screenHEIGHT)) # here launches a window, where is displayed all content
pygame.display.set_caption("Snake") # sets caption of window

def start_the_game():

    scores = 0
    speed = 1

    class SNAKE:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def borders(self):
            return 0 <= self.x < block_size and 0 <= self.y < block_size

        def __eq__(self, other):
            return isinstance(other, SNAKE) and self.x == other.x and self.y == other.y

    SNAKE_COORDINATE = [SNAKE(1, 1), SNAKE(1,2), SNAKE(1,3)]

    def DRAWING_BLOCK(WHITE, row, column):
        pygame.draw.rect(screen, WHITE, 
        (10 + column*block_size + margin_width*(column + 1), 
        SCORE_TABLOID + row*block_size + margin_width*(row + 1), 
        block_size, 
        block_size))   

    def random_apple_block():
        x = random.randint(0, row_num - 1)
        y = random.randint(0, row_num - 1)
        empty_block = SNAKE(x, y)
        
        while empty_block in SNAKE_COORDINATE:
            empty_block.x = x = random.randint(0, row_num - 1)
            empty_block.y = y = random.randint(0, row_num - 1)

        return empty_block


    apple = random_apple_block()

    x_axis_move = 0
    y_axis_move = 1



    while True:
        for event in pygame.event.get():    # empty event queue in very iteration, in order to prevent game crashing
            if event.type == pygame.QUIT: 
                exit()    # this event shutdown the window, when "X" button is pressed

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    x_axis_move = 1
                    y_axis_move = 0
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    x_axis_move = -1
                    y_axis_move = 0
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    y_axis_move = -1
                    x_axis_move = 0
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    y_axis_move = 1
                    x_axis_move = 0

        screen.fill(FILLING_COLOUR)  # fills background in white colour

        pygame.draw.rect(screen, FILLING_COLOUR, (0, 0, 440, 60))

        points = font.render(f"Points:{scores}", 10, RED)
        screen.blit(points, (20, 20))

        velocity =  font.render(f"Speed:{speed}", 10, RED)
        screen.blit(velocity, (160, 20))

        for row in range(row_num):    # creates playing field
            for column in range(column_num):
                DRAWING_BLOCK(WHITE, row, column)

        head = SNAKE_COORDINATE[-1]

        if not head.borders():
            print('GAME OVER')
            break

        DRAWING_BLOCK(APPLE_COLOUR, apple.x, apple.y)

        for block in SNAKE_COORDINATE:
            DRAWING_BLOCK(SNAKE_COLOUR, block.x, block.y)

        DRAWING_BLOCK(HEAD_COLOUR, block.x, block.y)

            
        pygame.display.flip()   # need to be called, in order to make all updates om the screen visible 


        if apple == head:
            SNAKE_COORDINATE.append(apple)
            apple = random_apple_block()
            scores += 1
            speed = scores // 10 + 1

        one_more_head = SNAKE(head.x + x_axis_move, head.y + y_axis_move)

        if one_more_head in SNAKE_COORDINATE:
            print('snakes do not eat themselves')
            break

        SNAKE_COORDINATE.append(one_more_head)
        SNAKE_COORDINATE.pop(0)


        timer.tick(5 + speed)




        # Do the job here !
    
main_theme = pygame_menu.themes.THEME_SOLARIZED.copy()

main_theme.set_background_color_opacity(0.0)
menu = pygame_menu.Menu(300, 400, 'Snake',
                       theme = main_theme)

menu.add_text_input('Name :', default='Player1')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)


while True:

    screen.blit(back_ground, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()