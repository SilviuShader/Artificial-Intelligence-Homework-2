import pygame
from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DRAW_MARGIN = 40
NODE_DRAW_DISTANCE = 70
CIRCLE_RADIUS = 20

class NodeData:
    
    def __init__(self, position):
        self.position = position
        self.draw_position = (DRAW_MARGIN + position[0] * NODE_DRAW_DISTANCE, DRAW_MARGIN + position[1] * NODE_DRAW_DISTANCE)

class GameGraph:

    def __init__(self):
        self.nodes = []
        self.nodes_at_pos = {}
        self.edges = {}

        for i in range(5):
            for j in range (5):
                crt_node = NodeData((i, j))
                self.nodes.append(crt_node)
                self.nodes_at_pos[crt_node.position] = len(self.nodes) - 1

        for i in range(1, 4):
            crt_node = NodeData((i, 5))
            self.nodes.append(crt_node)
            self.nodes_at_pos[crt_node.position] = len(self.nodes) - 1

        for i in range(0, 5, 2):
            crt_node = NodeData((i, 6))
            self.nodes.append(crt_node)
            self.nodes_at_pos[crt_node.position] = len(self.nodes) - 1

        for i in range(5):
            for j in range(5):
                crt_node_index = self.nodes_at_pos[(i, j)]
                crt_node = self.nodes[crt_node_index]

                dx = [-1, 0, 1, 0]
                dy = [0, -1, 0, 1]

                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    dx = [-1, 0, 1, 0, -1, -1, 1, 1]
                    dy = [0, -1, 0, 1, -1, 1, -1, 1]

                for k in range(len(dx)):
                    new_pos = (i + dx[k], j + dy[k])

                    if self.nodes_at_pos.get(new_pos) != None:
                        if new_pos not in [(1, 5), (2, 5), (3, 5)]:
                            if self.edges.get(crt_node_index) == None:
                                self.edges[crt_node_index] = []
                            self.edges[crt_node_index].append(self.nodes_at_pos[new_pos])

        self.edges[self.nodes_at_pos[(1, 5)]] = []
        self.edges[self.nodes_at_pos[(2, 5)]] = []
        self.edges[self.nodes_at_pos[(3, 5)]] = []
        self.edges[self.nodes_at_pos[(0, 6)]] = []
        self.edges[self.nodes_at_pos[(2, 6)]] = []
        self.edges[self.nodes_at_pos[(4, 6)]] = []
        
        self.edges[self.nodes_at_pos[(2, 4)]].append(self.nodes_at_pos[(1, 5)])
        self.edges[self.nodes_at_pos[(2, 4)]].append(self.nodes_at_pos[(2, 5)])
        self.edges[self.nodes_at_pos[(2, 4)]].append(self.nodes_at_pos[(3, 5)])
        
        self.edges[self.nodes_at_pos[(1, 5)]].append(self.nodes_at_pos[(2, 4)])
        self.edges[self.nodes_at_pos[(2, 5)]].append(self.nodes_at_pos[(2, 4)])
        self.edges[self.nodes_at_pos[(3, 5)]].append(self.nodes_at_pos[(2, 4)])


        self.edges[self.nodes_at_pos[(2, 5)]].append(self.nodes_at_pos[(1, 5)])
        self.edges[self.nodes_at_pos[(2, 5)]].append(self.nodes_at_pos[(2, 6)])
        self.edges[self.nodes_at_pos[(2, 5)]].append(self.nodes_at_pos[(3, 5)])

        self.edges[self.nodes_at_pos[(1, 5)]].append(self.nodes_at_pos[(2, 5)])
        self.edges[self.nodes_at_pos[(2, 6)]].append(self.nodes_at_pos[(2, 5)])
        self.edges[self.nodes_at_pos[(3, 5)]].append(self.nodes_at_pos[(2, 5)])


        self.edges[self.nodes_at_pos[(0, 6)]].append(self.nodes_at_pos[(1, 5)])
        self.edges[self.nodes_at_pos[(0, 6)]].append(self.nodes_at_pos[(2, 6)])

        self.edges[self.nodes_at_pos[(1, 5)]].append(self.nodes_at_pos[(0, 6)])
        self.edges[self.nodes_at_pos[(2, 6)]].append(self.nodes_at_pos[(0, 6)])


        self.edges[self.nodes_at_pos[(4, 6)]].append(self.nodes_at_pos[(3, 5)])
        self.edges[self.nodes_at_pos[(4, 6)]].append(self.nodes_at_pos[(2, 6)])

        self.edges[self.nodes_at_pos[(3, 5)]].append(self.nodes_at_pos[(4, 6)])
        self.edges[self.nodes_at_pos[(2, 6)]].append(self.nodes_at_pos[(4, 6)])


    def render_graph(self, screen):
        
        for i in range(len(self.nodes)):
            if self.edges.get(i) != None:
                for j in range(len(self.edges[i])):
                    draw_pos1 = self.nodes[i].draw_position
                    draw_pos2 = self.nodes[self.edges[i][j]].draw_position

                    pygame.draw.line(screen, (0, 0, 0), draw_pos1, draw_pos2, 4)

class GameConfiguration:

    def __init__(self, game_graph, dogs = None, jaguar = None):
        
        self.game_graph = game_graph

        if jaguar == None:
            self.jaguar = game_graph.nodes_at_pos[(2, 2)]
        else:
            self.jaguar = jaguar
        
        if dogs == None:
            self.dogs = []
            
            for i in range(5):
                for j in range(3):
                    if (i, j) != game_graph.nodes[self.jaguar].position:
                        self.dogs.append(game_graph.nodes_at_pos[(i, j)])
        else:
            self.dogs = dogs.copy()

    def render(self, screen):
        for dog in self.dogs:
            pygame.draw.circle(screen, (255, 255, 255), self.game_graph.nodes[dog].draw_position, CIRCLE_RADIUS)
            pygame.draw.circle(screen, (0, 0, 0), self.game_graph.nodes[dog].draw_position, CIRCLE_RADIUS, 5)
        
        pygame.draw.circle(screen, (0, 0, 0), self.game_graph.nodes[self.jaguar].draw_position, CIRCLE_RADIUS)

class Player:

    def __init__(self):
        pass

    def do_turn(self, game_graph, current_configuration):
        return current_configuration

class DogPlayer(Player):

    def __init__(self):
        pass

class JaguarPlayer(Player):

    def __init__(self):
        pass

class HumanDogPlayer(DogPlayer):

    def __init__(self):
        pass

class HumanJaguarPlayer(JaguarPlayer):

    def __init__(self):
        pass

    def do_turn(self, game_graph, current_configuration):
        
        

class Game:

    def __init__(self):
        self.game_graph = GameGraph()
        self.current_configuration = GameConfiguration(self.game_graph)        

        self.dog_player = HumanDogPlayer()
        self.jaguar_player = HumanJaguarPlayer()

        self.current_player = self.jaguar_player

    def update(self):

        new_configuration = self.current_player.do_turn(self.game_graph, self.current_configuration)
        if new_configuration != self.current_configuration:
            if self.dog_player == self.current_player:
                self.current_player = self.jaguar_player
            else:
                self.current_player = self.dog_player

    def render(self, screen):
        self.game_graph.render_graph(screen)
        self.current_configuration.render(screen)

def main():

    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

    running = True

    game = Game()

    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()

        screen.fill((255, 255, 255))

        game.render(screen)

        pygame.display.flip()

    pygame.quit()

    pass

if __name__ == "__main__":
    main()