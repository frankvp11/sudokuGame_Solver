import pygame

pygame.init()
text_font = pygame.font.Font("assets/font.ttf", 25)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

leftover = 0

class InputBox:

    def __init__(self, x, y, w, h, text='', i=None, j=None):
        self.index_one = i
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

    def handle_event(self, event, screen):
        global sudoku_board
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
                        sudoku_board[self.index_one][self.index_two] = 0
                    except TypeError:
                        pass
                else:
                    try:
                        
                        number= int(event.unicode)
                        self.text += event.unicode
                        if int(self.text) > 0 and int(self.text) < 9 and self.valid(sudoku_board, self.index_one, self.index_two, number):
                            sudoku_board[self.index_one][self.index_two] = number
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
    
    
    def valid(self, grid, i, j, val):
        for it in range(9):
            if grid[i][it]== val:
                print("Horizontal")
                return False
            if grid[it][j]== val:
                print(it, j)
                print("Vertical")
                return False
        it = i//3
        jt = j//3
        for i in range(it * 3, it * 3 + 3):
            for j in range (jt * 3, jt * 3 + 3):
                if grid[i][j]== val:
                    return False
        return True
                
    
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



#Input box Reqs:
#name = InputBox(x, y, w, h)
#name.handle_event(event, screen)
#name.draw(screen)
#name.update()



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



def main():
    global sudoku_board
    running = True


    map_of_inputs = []



    for i in range(9):
        j_list = []
        for j in range(9):
            j_list.append(InputBox(100+j*100, 100+i*100, 100, 100, text=str(sudoku_board[i][j]), i=i, j=j))
        map_of_inputs.append(j_list)
        
    while running:
        screen.fill(background_colour)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for i in range(len(map_of_inputs)):
                for j in range(len(map_of_inputs[i])):
                    map_of_inputs[i][j].handle_event(event, screen)
        
        for i in range(len(map_of_inputs)):
            for j in range(len(map_of_inputs[i])):
                map_of_inputs[i][j].draw(screen)
                map_of_inputs[i][j].update()
        pygame.display.update()


main()

