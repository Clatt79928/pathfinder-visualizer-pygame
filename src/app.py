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
        self.bfs_button = MainButton(self,WHITE,338,BUTTON_HEIGHT,200,70,'BFS')
        self.dfs_button = MainButton(self,WHITE,558,BUTTON_HEIGHT,200,70,'DFS')
        self.astar_button = MainButton(self,WHITE,778,BUTTON_HEIGHT,200,70,'A* Search')
        self.dijkstra_button = MainButton(self,WHITE,998,BUTTON_HEIGHT,200,70,'Dijkstra Search')

    def run(self):
        while self.running:
            if self.state == 'main_menu':
                self.main_menu()
            pygame.quit()
            sys.exit()

    def load(self):
        self.background = pygame.image.load('background.png')
    
    def main_menu(self):
        # draw background
        pygame.display.update()
        self.screen.blit(self.background, (0, 0))

        # draw buttons
        self.bfs_button.draw_main_button(AQUAMARINE)
        self.dfs_button.draw_main_button(AQUAMARINE)
        self.astar_button.draw_main_button(AQUAMARINE)
        self.dijkstra_button.draw_main_button(AQUAMARINE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    print('Clicked BFS')
                if self.dfs_button.isOver(pos):
                    print('Clicked DFS')
                if self.astar_button.isOver(pos):
                    print('Clicked A* Search')
                if self.dijkstra_button.isOver(pos):
                    print('Clicked Dijkstra Search')

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




def run_visualizer(self):
        pass
