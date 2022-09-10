from email.mime import base
import pygame
from copy import deepcopy
from random import shuffle


pygame.init()
text_font = pygame.font.Font("assets/font.ttf", 35)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

leftover = 0

class InputBox:

    def __init__(self, x, y, w, h, text='', i=None, j=None):
        self.index_one= i
        self.index_two = j
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255,255,255)
        self.text = text
        self.txt_surface = text_font.render(self.text, True, self.color)
        self.active = False
        self.score = 1
        # Cursor declare
        self.txt_rect = self.txt_surface.get_rect()
        self.cursor = pygame.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))

    def handle_event(self, event):
        global board_stuff
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    
                    global leftover
                    leftover += self.score
                    self.score = 0
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    try:
                        self.text = self.text[:-1]
                        board_stuff.grid[self.index_one][self.index_two] = 0
                    except TypeError:
                        pass
                else:
                    try:
                        
                        number= int(event.unicode)
                        self.text = event.unicode
                        if int(self.text) > 0 and int(self.text) < 9 and board_stuff.validate(self.index_one, self.index_two, number):
                            board_stuff.grid[self.index_one][self.index_two] = number
                        else:
                            self.text = self.text[:-1]
                            print("invalid")
                        # if not self.valid(sudoku_board, self.index_one, self.index_two, number):
                        #     print("Invalid")
                        # if int(self.text) > 9 or int(self.text) == 0 or not self.valid(sudoku_board, self.index_one, self.index_two, number):
                        #     self.text = self.text[:-1]      
                        
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    # Cursor

                    self.txt_rect.size = self.txt_surface.get_size()
                    self.cursor.topleft = self.txt_rect.topright

                    # Limit characters           -20 for border width
                    if self.txt_surface.get_width() > self.rect.w - 15:
                        self.text = self.text[:-1]
    
    def draw(self, screen):
        # Blit the text.
    
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 1)
        # Blit the  cursor
        import time
        if time.time() % 1 > 0.5:
            text_rect = self.txt_surface.get_rect(topleft = (self.rect.x + 5, self.rect.y + 10))

            # set cursor position
            self.cursor.midleft = text_rect.midright
            if self.active:
                pygame.draw.rect(screen, self.color, self.cursor)

    def update(self):
        # Re-render the text.
        self.txt_surface = text_font.render(self.text, True, self.color)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


#Input box Reqs:
#name = InputBox(x, y, w, h)
#name.handle_event(event, screen)
#name.draw(screen)
#name.update()

class Solver():
    def __init__(self, grid=None):
        self.grid = grid

    def validate(self, i, j, val):
        for iterator in range(9):
            if self.grid[i][iterator] == val or self.grid[iterator][j] == val:
                return False
        row_start = i // 3
        col_start = j // 3
        for x in range(row_start * 3, row_start * 3 + 3):
            for w in range(col_start*3, col_start*3+3):
                if self.grid[x][w] == val:
                    return False
        return True
    def solver(self, i, j):
        

        if i==8 and j == 9:
            print(self.grid)
            return True
        if j == 9:
            j = 0
            i += 1
        if self.grid[i][j] > 0:
            return self.solver(i, j+1)
        for number in range(1, 10):
            if self.validate(i, j, number):
                self.grid[i][j] = number
                if self.solver(i, j+1):
                    return True
            self.grid[i][j] = 0

        return False
    

 

from dokusan import generators

arr = list(str(generators.random_sudoku()))
sudoku_board = []
lines = []
print((arr))
print(len(arr))
for i in range(len(arr)):
    if len(lines) == 9:
        sudoku_board.append(lines)
        lines = []
    lines.append(int(arr[i]))
sudoku_board.append(lines)


for j in range(len(sudoku_board)):
    print(sudoku_board[j])

class Hint():
    def __init__(self, grid):
        self.grid = grid
    

    def give_hint(self):
        solver = Solver(self.grid)
        solver.solver(0,0)
        import random
        row_index = random.randint(0, 8)
        col_index = random.randint(0, 8)
        # if previous_grid[row_index][col_index] > 0:
        #     return self.give_hint()
        return solver.grid[row_index][col_index], row_index, col_index

        


background_colour = (0, 0, 0)
(width, height) = (1280, 1280)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sudoko Game')
pygame.display.flip()

sudoku_board =[
         [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]




board_stuff = Solver(sudoku_board) #sudoku_board
copy_of_board = deepcopy(sudoku_board)
hint_giver = Hint(copy_of_board)



def main():
    
    lives = 5
    global board_stuff  


    running = True
    map_of_inputs = []
    for i in range(9):
        j_list = []
        for j in range(9):
            j_list.append(InputBox(100+j*100, 100+i*100, 100, 100, text=str(board_stuff.grid[i][j]), i=i, j=j))
        map_of_inputs.append(j_list)
    solver_button = Button(image=None, pos=(1100, 100), text_input="Solve", font=get_font(20), base_color='white', hovering_color='green')
    hint_button = Button(image=None, pos=(1100, 150), text_input="Hint", font=get_font(20), base_color='white', hovering_color='green')
    lives_text = Button(image=None, pos=(1100, 200), text_input=f"Lives: {lives}", font=get_font(20), base_color='white', hovering_color='green')

    horizontal_lines_one = pygame.draw.line(screen, (255,255,255), (100, 100), (1000, 100), width=15)
    horizontal_lines_two = pygame.draw.line(screen, (255,255,255), (100, 400), (1000, 400), width=15)
    horizontal_lines_three = pygame.draw.line(screen, (255,255,255), (100, 700), (1000, 700), width=15)
    horizontal_lines_four = pygame.draw.line(screen, (255,255,255), (100, 1000), (1000, 1000), width=15)
    
    vertical_lines_one = pygame.draw.line(screen, (255,255,255), (95, 100), (95, 1000), width=15)
    vertical_lines_two = pygame.draw.line(screen, (255,255,255), (395, 100), (395, 1000), width=15)
    vertical_lines_three = pygame.draw.line(screen, (255,255,255), (695, 100), (695, 1000), width=15)
    vertical_lines_four = pygame.draw.line(screen, (255,255,255), (996, 100), (995, 1000), width=15)

    while running:
        screen.fill(background_colour) 

        mouse_position = pygame.mouse.get_pos()
        solver_button.changeColor(mouse_position)
        hint_button.changeColor(mouse_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for i in range(len(map_of_inputs)):
                for j in range(len(map_of_inputs)):
                    map_of_inputs[i][j].handle_event(event)
            if solver_button.checkForInput(mouse_position) and event.type == pygame.MOUSEBUTTONDOWN:
                board_stuff.solver(0, 0)
                for i in range(len(map_of_inputs)):
                    for j in range(len(map_of_inputs[i])):
                        map_of_inputs[i][j].text = str(board_stuff.grid[i][j])
                        
                lives_text = Button(image=None, pos=(1100, 200), text_input=f"Lives: 0", font=get_font(20), base_color='white', hovering_color='green')

            if hint_button.checkForInput(mouse_position) and event.type == pygame.MOUSEBUTTONDOWN:
                hint, row, col = hint_giver.give_hint()
                board_stuff.grid[row][col] = hint
                map_of_inputs[row][col].text = str(hint)
                print(hint, "HINT")
                print(row, col, "ROW, COL")
                lives -= 1
                lives_text = Button(image=None, pos=(1100, 200), text_input=f"Lives: {lives}", font=get_font(20), base_color='white', hovering_color='green')
        
        for i in range(len(map_of_inputs)):
            for j in range(len(map_of_inputs[i])):
                map_of_inputs[i][j].draw(screen)
                map_of_inputs[i][j].update()
        
        solver_button.update(screen)
        hint_button.update(screen)
        lives_text.update(screen)
        
        #pygame.display.flip()
        pygame.display.update()


main()

