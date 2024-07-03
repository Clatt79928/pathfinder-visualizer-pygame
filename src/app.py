import pygame, sys
from settings import *
from main_buttons import *

pygame.init()

class App:
    def init(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main_menu'
        self.load()
        self.bfs_button = Buttons(self,WHITE,338,BUTTON_HEIGHT,200,70,'BFS')
        self.dfs_button = Buttons(self,WHITE,558,BUTTON_HEIGHT,200,70,'DFS')
        self.astar_button = Buttons(self,WHITE,778,BUTTON_HEIGHT,200,70,'A* Search')
        self.dijkstra_button = Buttons(self,WHITE,998,BUTTON_HEIGHT,200,70,'Dijkstra Search')

    def run(self):
        while self.running:
            if self.state == 'main_menu':
                self.main_menu_events()
            if self.state == 'show grid':
                self.grid_events()
            pygame.quit()
            sys.exit()

    def load(self):
        self.background = pygame.image.load('background.png')
        self.grid_background = pygame.image.load('grid_logo.png')

    def sketch_main_menu(self):
        # draw background
        self.screen.blit(self.background, (0, 0))

        # draw buttons
        self.bfs_button.draw_button(AQUAMARINE)
        self.dfs_button.draw_button(AQUAMARINE)
        self.astar_button.draw_button(AQUAMARINE)
        self.dijkstra_button.draw_button(AQUAMARINE)

        #setup for Grid
    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)
        self.screen.blit(self.grid_background, (0, 0))
    
    def sketch_grid(self):
        # Add borders for a cleaner look
        pygame.draw.rect(self.screen, ALICE, (240, 0, WIDTH, HEIGHT), 0)
        pygame.draw.rect(self.screen, AQUAMARINE, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        #draw grid
        # there are 52 square pixels across on grid without borders
        # there are 30 square pixels vertically on grid without borders
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (GS_X + x*self.grid_square_length, GS_Y),
                             (GS_X + x*self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y*self.grid_square_length),
                             (GE_X, GS_Y + y*self.grid_square_length))
    def sketch_grid_buttons(self):
        # Draw buttons
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)


    def main_menu_events(self):
        pygame.display.update()

        self.sketch_main_menu()

        #check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # get mouse position and check if it is clicking the button
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.state = 'show grid'
                if self.dfs_button.isOver(pos):
                    self.state = 'show grid'
                if self.astar_button.isOver(pos):
                    self.state = 'show grid'
                if self.dijkstra_button.isOver(pos):
                    self.state = 'show grid'
            #get mouse position and check if it is hovering the button
            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.colour = AQUAMARINE
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.colour = AQUAMARINE
                elif self.astar_button.isOver(pos):
                    self.astar_button.colour = AQUAMARINE
                elif self.dijkstra_button.isOver(pos):
                    self.dijkstra_button.colour = AQUAMARINE
                else:
                    self.bfs_button.colour, self.dfs_button.colour, self.astar_button.colour, self.dijkstra_button.colour = WHITE, WHITE, WHITE, WHITE




#playing state functions

    def grid_events(self):
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_end_node_button.isOver(pos):
                    print('pressed a')
                elif self.wall_node_button.isOver(pos):
                    print('pressed b')
                elif self.reset_button.isOver(pos):
                    print('pressed c')
                elif self.start_button.isOver(pos):
                    print('pressed d')

            # get mouse position and check if it is hovering over button
            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.colour = MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE


