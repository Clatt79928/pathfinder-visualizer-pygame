import pygame, sys
from settings import *
from main_buttons import *
from bfs_class import *
from visualize_path_class import *

pygame.init()

best_rout = None

class App:
    def init(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main_menu'
        self.load()

        self.start_end_checker = 0  
        self.route_found = False
        self.best_route = None

        # start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        self.wall_pos = wall_nodes_coords_list
        # wall nodes list (list already includes the coordinates of the borders)
        
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
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()


        pygame.quit()
        sys.exit()

    def load(self):
        self.background = pygame.image.load('background.png')
        self.grid_background = pygame.image.load('grid_logo.png')

    #draw text
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)


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
        # add borders for a better look
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
        self.draw_text('Made By: Kevin Zhuang', self.screen, [1200, 720], 28, WHITE, FONT, centered=False)

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
                    self.state = 'draw S/E'
                elif self.wall_node_button.isOver(pos):
                    self.state = 'draw walls'
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


#drawing state functions
    # - check where the mouse is clicking on grid
    # - add in feature to draw nodes on grid
    # - add in feature so that the drawn nodes on grid translate onto text file
    def draw_nodes(self):
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_end_node_button.isOver(pos):
                    self.state = 'draw S/E'
                elif self.wall_node_button.isOver(pos):
                    self.state = 'draw walls'
                elif self.reset_button.isOver(pos):
                    print('Work In Progress')
                elif self.start_button.isOver(pos):
                    self.state = 'start visualizing'

            # Get mouse position and check if it is hovering over button
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

            # checking if mouse is within the boundary of the grid to draw
            if pos[0] > 264 and pos[0] < 1512 and pos[1] > 24 and pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                #print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # get mouse position and check if it is clicking button. 
                # then, draw if clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'draw S/E' and self.start_end_checker < 2:

                        # choose point color for grid and record the coordinate of start pos
                        if self.start_end_checker == 0:
                            node_colour = RED
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.start_end_checker += 1

                        # choose point color for grid and record the coordinate of end pos
                        elif self.start_end_checker == 1:
                            node_colour = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.start_end_checker += 1

                        # draw point on grid
                        pygame.draw.rect(self.screen, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                    # draw wall Nodes and append wall node coordinates to the wall nodes list
                    elif self.state == 'draw walls':
                        pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos*24, 24 + y_grid_pos*24, 24, 24), 0)
                        self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))
                        # print(len(self.wall_pos))

#visualizing state functions

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        #print(self.start_node_x, self.start_node_y)
        #print(self.end_node_x, self.end_node_y)

            # make BFS object
            self.bfs = BreadthFirst(self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                while not self.route_found:
                    self.bfs.bfs_execute()
                    best_route = self.bfs.route
                    self.route_found = True

            # make Object for new path
            while True:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, best_route)
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
                pygame.display.update()

