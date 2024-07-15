import sys
from settings import *
from main_buttons import *
from dijkstra import *
from astar import *
from bfs import *
from bidirectional import *
from dfs import*
from visualize_path import *

pygame.init()


class App:
    def init(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main_menu'
        self.algorithm_state = ''
        self.grid_square_length = 24 # tThe dimensoions of each grid 
        self.load()

        self.start_end_checker = 0  
        self.route_found = False
        set.mouse_drag =0

        # start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        self.wall_pos = wall_nodes_coords_list.copy()
        # wall nodes list (list already includes the coordinates of the borders)
        
        self.bfs_button = Buttons(self,WHITE,138,MAIN_BUTTON_HEIGHT,200,70,'BFS')
        self.dfs_button = Buttons(self,WHITE,358,MAIN_BUTTON_HEIGHT,200,70,'DFS')
        self.astar_button = Buttons(self,WHITE,578,MAIN_BUTTON_HEIGHT,200,70,'A* Search')
        self.dijkstra_button = Buttons(self,WHITE,798,MAIN_BUTTON_HEIGHT,200,70,'Dijkstra Search')
        self.bidirectional_button = Buttons(self, WHITE, 1018, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Bidirectional Search')

        self.start_end_node_button = Buttons(self,AQUAMARINE, START_END_BUTTON_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Buttons(self,AQUAMARINE, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(self,AQUAMARINE, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Reset')
        self.start_button = Buttons(self,AQUAMARINE, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start')
        self.main_menu_button = Buttons(self,AQUAMARINE, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*4 + BUTTON_SPACER*4, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Main Menu')

    def run(self):
        while self.running:
            if self.state == 'main_menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main_menu()


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
        self.bidirectional_button.draw_button(AQUAMARINE)

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
        # draw buttons
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)
##### checks for state when button is clicked and changes button colour when hovered over.
    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
            elif self.start_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.state = 'main_menu'
        # et mouse position and check if it is hovering over button
        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.colour = MINT
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.colour = MINT
            elif self.reset_button.isOver(pos):
                self.reset_button.colour = MINT
            elif self.start_button.isOver(pos):
                self.start_button.colour = MINT
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = MINT
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour,self.main_menu_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.colour = MINT

        elif self.state == 'draw walls':
            self.wall_node_button.colour = MINT

    def execute_reset(self):
        self.route_found = False
        self.start_end_checker = 0

        #start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        #reset class attributes
        self.bfs.bfs_reset()

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()

        # Switch States
        self.state = 'grid window'
    
    def back_to_main_menu(self):
        self.start_end_checker = 0

        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        self.wall_pos = wall_nodes_coords_list.copy()

        self.state = 'main_menu'


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
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.dijkstra_button.isOver(pos):
                    self.algorithm_state = 'dijkstra'
                    self.state = 'grid window'
                if self.bidirectional_button.isOver(pos):
                    self.algorithm_state = 'bidirectional'
                    self.state = 'grid window'
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
                elif self.bidirectional_button.isOver(pos):
                    self.bidirectional_button.colour = AQUAMARINE
            
                else:
                    self.bfs_button.colour, self.dfs_button.colour, self.astar_button.colour, self.dijkstra_button.colour,self.bidirectional_button.colour =WHITE, WHITE, WHITE, WHITE, WHITE




#playing state functions

    def grid_events(self):
        #print(len(wall_nodes_coords_list))
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            #helper function
            self.grid_window_buttons(pos, event)


#drawing state functions
    def draw_nodes(self):
        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.grid_window_buttons(pos, event)

            

            # set boundaries for where mouse position is valid
            if pos[0] > 264 and pos[0] < 1512 and pos[1] > 24 and pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                #print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # get mouse position and check if it is clicking button. 
                # then, draw if clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1
                   
                    if self.state == 'draw S/E' and self.start_end_checker < 2:

                        # choose point color for grid and record the coordinate of start pos
                        if self.start_end_checker == 0:
                            node_colour = TOMATO
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.start_end_checker += 1

                        # choose point color for grid and record the coordinate of end pos
                        elif self.start_end_checker == 1 and (x_grid_pos + 1, y_grid_pos +1) != (self.start_node_x, self.start_node_y):
                            node_colour = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.start_end_checker += 1
                        
                        else:
                            continue

                        # draw point on grid
                        pygame.draw.rect(self.screen, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                    
                    if self.state == 'draw walls':
                        if(x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos:
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))

                            pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos*24, 24 + y_grid_pos*24, 24, 24), 0)
                    
                for x in range(52):
                    pygame.draw.line(self.screen, ALICE, (GS_X + x * self.grid_square_length, GS_Y),(GS_X + x * self.grid_square_length, GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y * self.grid_square_length),(GE_X, GS_Y + y * self.grid_square_length))

#visualizing state functions

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        #print(self.start_node_x, self.start_node_y)
        #print(self.end_node_x, self.end_node_y)

            # make BFS object
        if self.algorithm_state == 'bfs':
            self.bfs = BreadthFirst(self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            # make Object for new path
            if self.bfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route,[])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
            else:
                self.draw_text('No Path Found', self.screen, [768, 384], 50, RED, FONT, centered=True)

        elif self.algorithm_state == 'dfs':
            self.dfs = DepthFirst(self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)
            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()
            if self.dfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route,[])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
            else:
                self.draw_text('No Path Found', self.screen, [768, 384], 50, RED, FONT, centered=True)

        elif self.algorithm_state == 'astar': #implement next
            self.astar = AStar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.astar.astar_execute()

            if self.astar.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.astar.route)
                self.draw_path.draw_path()
        elif self.algorithm_state == 'dijkstra': #implement next
        
            self.dijkstra = Dijkstra(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dijkstra.dijkstra_execute()

            if self.dijkstra.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.dijkstra.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('No Path Found', self.screen, [768, 384], 50, RED, FONT, centered=True)

        elif self.algorithm_state == 'bidirectional':
            self.bidirectional = Bidirectional(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.bidirectional.bidirectional_execute()

            if self.bidirectional.route_found:
                print(self.bidirectional.route_f)
                print(self.bidirectional.route_r)
                self.draw_path_f = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.bidirectional.route_f)
                self.draw_path_r = VisualizePath(self.screen, self.end_node_x, self.end_node_y, None, self.bidirectional.route_r)

                # draw paths on the app
                self.draw_path_f.draw_path()
                self.draw_path_r.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)

        pygame.display.update()
        self.state = 'aftermath'

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.colour = MINT
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour,self.main_menu_button.colour =STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                if self.main_menu_button.isOver(pos):
                    self.back_to_main_menu()