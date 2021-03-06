import math
import sys
import pygame
import pygame_gui
import time
from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DRAW_MARGIN = 40
NODE_DRAW_DISTANCE = 70
CIRCLE_RADIUS = 20

class PyGameHelper:
    '''
    clasa utila pentru a detecta
    cand se da release la mouse, deoarece
    pygame nu are ceva pentru asta
    built-in
    '''

    def __init__(self):
        self.last_mouse_pressed = False
        self.mouse_released = False

    def update_input(self):
        mouse_state = pygame.mouse.get_pressed()

        self.mouse_released = False

        if (not mouse_state[0]) and self.last_mouse_pressed:
            self.mouse_released = True

        self.last_mouse_pressed = mouse_state[0]

    def was_mouse_released(self):
        return self.mouse_released

pygame_helper = PyGameHelper()

class NodeData:
    '''
    O calasa care tine pentru un nod
    pozitia sa in grid (x, y), dar si pozitia
    de pe ecran. Este utila pentru desenarea board-ului 
    '''

    def __init__(self, position):
        self.position = position
        self.draw_position = (DRAW_MARGIN + position[0] * NODE_DRAW_DISTANCE, 2 * DRAW_MARGIN + position[1] * NODE_DRAW_DISTANCE)

class GameGraph:
    '''
    Clasa care se ocupa de graful tablei de joc
    '''

    def __init__(self):

        '''
        Se creeaza intreaga tabla ca un graf. Avem un dictionar
        care ne spune ce nod se afla la o pozitie din grid, o lista
        de noduri, si o lista de adiacenta pentru a putea parcurge
        graful cu usurinta
        '''

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

        '''
        Functia care deseneaza tabla de joc, luandu-se
        dupa relatiile dintre muchii si pozitiile nodurilor
        '''
        
        for i in range(len(self.nodes)):
            if self.edges.get(i) != None:
                for j in range(len(self.edges[i])):
                    draw_pos1 = self.nodes[i].draw_position
                    draw_pos2 = self.nodes[self.edges[i][j]].draw_position

                    pygame.draw.line(screen, (0, 0, 0), draw_pos1, draw_pos2, 4)

class GameConfiguration:

    '''
    Aceasta clasa tine informatii despre o anumita
    stare din joc. Contine o lista cu nodurile unde se
    afla caini, si o variabila in care se tine nodul
    cu pozitia jaguarului.
    '''

    def __init__(self, game_graph, dogs = None, jaguar = None):

        '''
        In constructor se creaza o tabla cu configuratia initiala
        daca nu se specifica o alta configuratie
        '''
        
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

    def get_winner(self, game_graph):

        '''
        Functia care returneaza castigatorul dintr-o configuratie.
        Daca jaguraul nu mai poate face miscari, atunci cainii sunt
        castigatori. Daca sunt 9 sau mai putini caini ramasi, atunci
        acestia nu mai au cum sa inconjoare jaguarul, deci castiga
        jaguarul. Daca nu se intampla niciunul din aceste lucruri, inseamna
        ca nu suntem intr-o configuratie finala.
        '''

        available_jaguar_configs = JaguarPlayer.get_available_configurations(game_graph, self)
        if len(available_jaguar_configs) == 0:
            return 0

        if len(self.dogs) <= 9:
            return 1

        return -1

    def debug_print(self, game_graph):

        '''
        Functia care afiseaza tabla de joc in consola (cerinta 4)
        '''

        print_string = ""

        for y in range(7):
            for x in range(5):
                if game_graph.nodes_at_pos.get((x, y)) != None:
                    crt_node = game_graph.nodes_at_pos[(x, y)]
                    if crt_node in self.dogs:
                        print_string = print_string + "D "
                    elif crt_node == self.jaguar:
                        print_string = print_string + "J "
                    else:
                        print_string = print_string + ". "
                else:
                    print_string = print_string + "  "

            print_string = print_string + "\n"

        print(print_string)

    def render(self, screen, game_graph):

        '''
        Randeaza cercuri albe la pozitiile cainilor si un cerc negru la pozitia
        jaguarului. Daca au castigat cainii, ii va desena cu verde, iar daca a castigat
        jaguarul, il va desena cu verde pe el.
        '''

        crt_winner = self.get_winner(game_graph)

        for dog in self.dogs:
            
            dog_color = (255, 255, 255)
            if crt_winner == 0:
                dog_color = (0, 255, 0)

            pygame.draw.circle(screen, dog_color, self.game_graph.nodes[dog].draw_position, CIRCLE_RADIUS)
            pygame.draw.circle(screen, (0, 0, 0), self.game_graph.nodes[dog].draw_position, CIRCLE_RADIUS, 5)
        
        jaguar_color = (0, 0, 0)

        if crt_winner == 1:
            jaguar_color = (0, 255, 0)

        pygame.draw.circle(screen, jaguar_color, self.game_graph.nodes[self.jaguar].draw_position, CIRCLE_RADIUS)

def distance(pos1, pos2):
    
    '''
    Functie care calculeaza distanta dintre doua punce de pe ecran.
    Este utila cand verificam daca s-a dat click pe o pozitie din board.
    '''

    pos3 = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    pos3 = (pos3[0] * pos3[0], pos3[1] * pos3[1])
    return math.sqrt(pos3[0] + pos3[1])

def replace(arr, value, new_value):

    '''
    Functie care primeste un array, si returneaza un array nou
    care este o copie a celui initial, doar ca la pozitiile unde
    se afla valoarea value se va pune valoarea new_value.
    Functia este utila cand vrem sa mutam un caine la alta pozitie.
    '''

    arr2 = arr.copy()

    for i in range(len(arr2)):
        if arr2[i] == value:
            arr2[i] = new_value

    return arr2

class Player:

    '''
    Clasa de baza pe care o mostenesc toate tipurile de jucatori, chit
    ca sunt jucatori umani sau AI-uri.
    '''

    def __init__(self):
        pass

    def do_turn(self, game_graph, current_configuration):
        '''
        Din moment ce e un jucator generic, nu va face nicio mutare
        '''
        return current_configuration

    def get_clicked_node(self, game_graph, position):

        '''
        functie care primeste graful tablei de joc si pozitia la care s-a dat click pe ecran
        si returneaza nodul pe care s-a dat click (daca s-a dat click pe un nod, altfel returneaza
        -1)
        '''

        result = -1
        for ix, node in enumerate(game_graph.nodes):
            dist = distance(node.draw_position, position)
            if dist <= CIRCLE_RADIUS:
                result = ix

        return result

    def valid_neighbour(game_graph, current_configuration, current_node, other_node):

        '''
        Functie care verifica daca o mutare este valida (valabila si pentru jaguar, si pentru caini)
        Parte din cerinta 5.
        '''

        if game_graph.edges.get(current_node) != None:
            if other_node in game_graph.edges[current_node]:
                if (other_node not in current_configuration.dogs) and (other_node != current_configuration.jaguar):
                    return True

        return False

    def render(self, screen, game_graph):
        pass

class DogPlayer(Player):

    '''
    Clasa care mosteneste clasa Player, si care va fi mostenita
    de clasele care controleaza caini.
    '''

    def __init__(self):
        pass

    def get_available_configurations(game_graph, current_configuration):

        '''
        Genereaza toate mutarile posibile pentru jucatorul care controleaza cainii.
        Parte din cerinta 5.
        '''

        result = []
        for dog in current_configuration.dogs:
            for other_node in game_graph.edges[dog]:
                if Player.valid_neighbour(game_graph, current_configuration, dog, other_node):
                    result.append(GameConfiguration(game_graph, replace(current_configuration.dogs, dog, other_node), current_configuration.jaguar))
        
        return result

    def configuration_cost(game_graph, prev_configuration, current_configuration):

        '''
        Una din functiile de estimare. Aceasta functie este in favoarea cainilor. Ea numara
        cati caini inconjoara jaguarul. AI-urile pentru caini se folosesc de aceasta functie de estimare.
        '''

        count = 0
        for other_node in game_graph.edges[current_configuration.jaguar]:
            if other_node in current_configuration.dogs:
                count = count + 1
        
        return count

class JaguarPlayer(Player):

    '''
    Clasa care mosteneste clasa Player, si care va fi mostenita
    de clasele care controleaza jaguarul.
    '''

    def __init__(self):
        '''
        avem o lista care tine nodurile selectate pentru a
        captura mai multi caini (folosita de jucatorul uman)
        '''
        self.move_plan = []

    def dog_between_nodes(game_graph, initial_node, target_node, dog_node):

        '''
        functie care verifica daca un caine care se afla pe nodul dog_node se afla
        in linie dreapta intre nodurile initial_node si target_node
        '''

        if initial_node in game_graph.edges[dog_node] and target_node in game_graph.edges[dog_node]:
            vec1 = (game_graph.nodes[dog_node].position[0] - game_graph.nodes[initial_node].position[0], game_graph.nodes[dog_node].position[1] - game_graph.nodes[initial_node].position[1])
            vec2 = (game_graph.nodes[target_node].position[0] - game_graph.nodes[dog_node].position[0], game_graph.nodes[target_node].position[1] - game_graph.nodes[dog_node].position[1])
            if vec1 == vec2:
                return True
        
        return False

    def can_add_to_plan(current_plan, game_graph, current_configuration, other_node):

        '''
        functie care verifica daca un nod se poate adauga la lista in care
        se pastreaza nodurile prin care va trece jaguarul in timp ce captureaza caini.
        Parte din cerinta 5.
        '''

        last_node_plan = current_configuration.jaguar
        if len(current_plan) != 0:
            last_node_plan = current_plan[-1]

        if last_node_plan == other_node:
            return False

        if other_node in current_configuration.dogs:
            return False

        if other_node in current_plan:
            return False

        if other_node == current_configuration.jaguar:
            return False

        for dog in current_configuration.dogs:
            if JaguarPlayer.dog_between_nodes(game_graph, last_node_plan, other_node, dog):
                return True

        return False

    def configuration_after_move(move_plan, game_graph, current_configuration):

        '''
        Functie care primeste lista cu succesiunea de noduri prin care face captura
        si returneaza o noua configuratie de board in urma executarii acelor capturi
        '''

        dogs_to_remove = []

        for i in range(len(move_plan)):
            prev_node = current_configuration.jaguar
            if i != 0:
                prev_node = move_plan[i - 1]
            crt_node = move_plan[i]

            for dog in current_configuration.dogs:
                if JaguarPlayer.dog_between_nodes(game_graph, prev_node, crt_node, dog):
                    dogs_to_remove.append(dog)

        current_configuration = GameConfiguration(game_graph, [dog for dog in current_configuration.dogs if dog not in dogs_to_remove], move_plan[-1])

        return current_configuration

    def get_available_captures(solutions, game_graph, current_configuration, crt_solution, last_node):

        '''
        functie recursiva (backtracking) returneaza toate posibilitatile de liste 
        de noduri care ar putea face parte dintr-o captura pornita din configuratia curenta
        '''

        if crt_solution != []:
            solutions.append(crt_solution)
        
        for other_node in range(len(game_graph.nodes)):
            if JaguarPlayer.can_add_to_plan(crt_solution, game_graph, current_configuration, other_node):
                new_sol = crt_solution.copy()
                new_sol.append(other_node)
                JaguarPlayer.get_available_captures(solutions, game_graph, current_configuration, new_sol, other_node)

    def get_available_configurations(game_graph, current_configuration):

        '''
        functie care returneaza toate configuratiile de joc care pot rezulta prin mutarea jaguarului din
        configuratia curenta.
        Parte din cerinta 5.
        '''

        possible_move_plans = []

        for other in game_graph.edges[current_configuration.jaguar]:
            if Player.valid_neighbour(game_graph, current_configuration, current_configuration.jaguar, other):
                possible_move_plans.append([other])

        JaguarPlayer.get_available_captures(possible_move_plans, game_graph, current_configuration, [], current_configuration.jaguar)

        available_configurations = [JaguarPlayer.configuration_after_move(move_plan, game_graph, current_configuration) for move_plan in possible_move_plans]

        return available_configurations

    def configuration_cost(game_graph, prev_configuration, current_configuration):
        return len(prev_configuration.dogs) - len(current_configuration.dogs)

class AIHelper:

    '''
    clasa care contine algoritmii minimax si alpha-beta
    adaptati pentru jocul nostru
    '''

    def __init__(self):
        '''
        initializam counter-ul pentru numarul de mutari cu 0
        '''
        self.algo_moves = 0

    def difficulty_to_depth(difficulty):
        '''
        dificultatea este un numar intre 0 si 2, deci noi va trebui sa il
        transformam intr-o adancime pentru parcurgeri, si facem asta folosind
        formula urmatoare
        '''
        return 1 + (difficulty * 2)

    def minimax(game_graph, initial_configuration, current_configuration, is_max, is_jaguar, crt_level, max_levels, cost_function):

        '''
        algoritmul minimax. Pentru estimare se foloseste functia cost_function trimisa ca argument.
        In functie de tipul de jucator (jaguar sau caini) se genereaza configuratii folosind functii diferite.
        '''

        available_configurations = []
        if is_jaguar:
            available_configurations = JaguarPlayer.get_available_configurations(game_graph, current_configuration)
        else:
            available_configurations = DogPlayer.get_available_configurations(game_graph, current_configuration)

        ai_helper_instance.algo_moves = ai_helper_instance.algo_moves + len(available_configurations) 
        
        if crt_level >= max_levels - 1:
            sol = (None, -1)
            for new_config in available_configurations:
                crt_cost = cost_function(game_graph, initial_configuration, new_config)
                if is_max:
                    if crt_cost > sol[1]:
                        sol = (new_config, crt_cost)
                else:
                    if sol[1] == -1 or crt_cost < sol[1]:
                        sol = (new_config, crt_cost)
            
            if sol[0] != None:
                return sol
            return (current_configuration, 0)
        
        result = (None, -1)

        for new_config in available_configurations:
            returned_val = AIHelper.minimax(game_graph, initial_configuration, new_config, not is_max, not is_jaguar, crt_level + 1, max_levels, cost_function)
            if returned_val[0] != None:
                if is_max:
                    if result[1] < returned_val[1]:
                        result = (new_config, returned_val[1])
                else:
                    if result[1] == -1 or result[1] > returned_val[1]:
                        result = (new_config, returned_val[1])

        if result[0] != None:
            return result

        return (current_configuration, 0)

    def alphabeta(game_graph, initial_configuration, current_configuration, is_max, is_jaguar, crt_level, max_levels, cost_function, alpha, beta):

        '''
        Algoritmul alpha-beta. Exact ca minimax, doar ca exista si optimizarea cu numerele
        alpha si beta.
        '''

        available_configurations = []
        if is_jaguar:
            available_configurations = JaguarPlayer.get_available_configurations(game_graph, current_configuration)
        else:
            available_configurations = DogPlayer.get_available_configurations(game_graph, current_configuration)

        ai_helper_instance.algo_moves = ai_helper_instance.algo_moves + len(available_configurations)

        if crt_level >= max_levels - 1:
            sol = (None, -1)
            for new_config in available_configurations:
                crt_cost = cost_function(game_graph, initial_configuration, new_config)
                if is_max:
                    if crt_cost > sol[1]:
                        sol = (new_config, crt_cost)
                else:
                    if sol[1] == -1 or crt_cost < sol[1]:
                        sol = (new_config, crt_cost)
            if sol[0] != None:
                return sol
            return (current_configuration, 0)

        if is_max:
            
            sol = (None, -1)
            for new_config in available_configurations:
                returned_val = AIHelper.alphabeta(game_graph, initial_configuration, new_config, not is_max, not is_jaguar, crt_level + 1, max_levels, cost_function, alpha, beta)
                
                if returned_val[0] != None:
                    if returned_val[1] > sol[1]:
                        sol = (new_config, returned_val[1])

                    alpha = max(alpha, returned_val[1])
                    if alpha >= beta:
                        break

            if sol[0] != None:
                return sol
        else:
            sol = (None, -1)
            for new_config in available_configurations:
                returned_val = AIHelper.alphabeta(game_graph, initial_configuration, new_config, not is_max, not is_jaguar, crt_level + 1, max_levels, cost_function, alpha, beta)

                if returned_val[0] != None:
                    if returned_val[1] < sol[1] or sol[1] == -1:
                        sol = (new_config, returned_val[1])
                    
                    beta = min(beta, returned_val[1])
                    if beta <= alpha:
                        break

            if sol[0] != None:
                return sol

        return (current_configuration, 0)

ai_helper_instance = AIHelper()        

class MinimaxDogPlayer(DogPlayer):

    '''
    clasa pentru jucatorul de caini care foloseste minimax
    '''

    def __init__(self, difficulty):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        self.difficulty = difficulty

    def do_turn(self, game_graph, current_configuration):
        '''
        Face o mutare folosind algoritmul minimax pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        ai_helper_instance.algo_moves = 0
        result = AIHelper.minimax(game_graph, current_configuration, current_configuration, True, False, 0, AIHelper.difficulty_to_depth(self.difficulty), DogPlayer.configuration_cost)
        print("Estimation: " + str(result[1]))
        print("Generated nodes: " + str(ai_helper_instance.algo_moves))
        return (result[0], ai_helper_instance.algo_moves)

class AlphaBetaDogPlayer(DogPlayer):

    '''
    clasa pentru jucatorul de caini care foloseste alpha-beta
    '''

    def __init__(self, difficulty):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        self.difficulty = difficulty

    def do_turn(self, game_graph, current_configuration):
        '''
        Face o mutare folosind algoritmul alpha-beta pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        ai_helper_instance.algo_moves = 0
        result = AIHelper.alphabeta(game_graph, current_configuration, current_configuration, True, False, 0, AIHelper.difficulty_to_depth(self.difficulty), DogPlayer.configuration_cost, -sys.maxsize, sys.maxsize)
        print("Estimation: " + str(result[1]))
        print("Generated nodes: " + str(ai_helper_instance.algo_moves))
        return (result[0], ai_helper_instance.algo_moves)

class HumanDogPlayer(DogPlayer):

    '''
    clasa pentru jucatorul uman care controleaza caini.
    '''

    def __init__(self):
        '''
        vom tine minte ultimul caine selectat, pentru ca
        vom face mutarea folosind acel caine
        '''
        self.selected_dog = -1

    def do_turn(self, game_graph, current_configuration):

        '''
        functia care face o mutare in functie de ce apasa utlizatorul (este
        posibil sa fie apelata de mai multe ori in update pana sa se faca
        o mutare, deoarece depinde de player, nu de calculator, nu stim cand
        se va decide). Se asteapta selectarea unui caine, dupa care se face mutarea
        aleasa daca este valida (se poate schimba cainele).
        '''
        
        if pygame_helper.was_mouse_released():
            node_ix = self.get_clicked_node(game_graph, pygame.mouse.get_pos())
            
            if node_ix != -1:

                if node_ix in current_configuration.dogs:
                    self.selected_dog = node_ix
                elif self.selected_dog != -1:
                    if Player.valid_neighbour(game_graph, current_configuration, self.selected_dog, node_ix):
                        current_configuration = GameConfiguration(game_graph, replace(current_configuration.dogs, self.selected_dog, node_ix), current_configuration.jaguar)
                        self.selected_dog = -1

        return (current_configuration, 0)

    def render(self, screen, game_graph):

        '''
        daca este un caine selectat, acesta va fi desenat cu verde.
        '''

        if self.selected_dog != -1:
            pygame.draw.circle(screen, (0, 255, 0), game_graph.nodes[self.selected_dog].draw_position, CIRCLE_RADIUS)
            pygame.draw.circle(screen, (0, 0, 0), game_graph.nodes[self.selected_dog].draw_position, CIRCLE_RADIUS, 5)

class MinimaxJaguarPlayer(JaguarPlayer):

    '''
    clasa pentru jucatorul jaguar care foloseste minimax
    '''

    def __init__(self, difficulty):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        super().__init__()
        self.difficulty = difficulty

    def do_turn(self, game_graph, current_configuration):
        '''
        Face o mutare folosind algoritmul minimax pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        ai_helper_instance.algo_moves = 0
        result = AIHelper.minimax(game_graph, current_configuration, current_configuration, True, True, 0, AIHelper.difficulty_to_depth(self.difficulty), JaguarPlayer.configuration_cost)
        print("Estimation: " + str(result[1]))
        print("Generated nodes: " + str(ai_helper_instance.algo_moves))
        return (result[0], ai_helper_instance.algo_moves)

class AlphaBetaJaguarPlayer(JaguarPlayer):

    '''
    clasa pentru jucatorul jaguar care foloseste alpha-beta
    '''

    def __init__(self, difficulty):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        super().__init__()
        self.difficulty = difficulty

    def do_turn(self, game_graph, current_configuration):
        '''
        Face o mutare folosind algoritmul alpha-beta pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        ai_helper_instance.algo_moves = 0
        result = AIHelper.alphabeta(game_graph, current_configuration, current_configuration, True, True, 0, AIHelper.difficulty_to_depth(self.difficulty), JaguarPlayer.configuration_cost, -sys.maxsize, sys.maxsize)
        print("Estimation: " + str(result[1]))
        print("Generated nodes: " + str(ai_helper_instance.algo_moves))
        return (result[0], ai_helper_instance.algo_moves)

class HumanJaguarPlayer(JaguarPlayer):

    '''
    clasa pentru jucatorul uman de jaguar
    '''

    def __init__(self):
        '''
        ne intereseaza sa avem o lista de capturi posibile creata
        '''
        super().__init__()

    def do_turn(self, game_graph, current_configuration):

        '''
        functie similara cu cea de ka jucatorul uman pentru caini, doar ca aici luam in calcul
        si daca sunt capturi multiple pe care le face jaguarul. Se fac toate verificarile
        '''

        if pygame_helper.was_mouse_released():
            node_ix = self.get_clicked_node(game_graph, pygame.mouse.get_pos())
            if node_ix != -1:
                if len(self.move_plan) == 0:
                    if JaguarPlayer.can_add_to_plan(self.move_plan, game_graph, current_configuration, node_ix):
                        self.move_plan.append(node_ix)
                    elif Player.valid_neighbour(game_graph, current_configuration, current_configuration.jaguar, node_ix):
                        current_configuration = GameConfiguration(game_graph, current_configuration.dogs, node_ix)
                else:
                    if JaguarPlayer.can_add_to_plan(self.move_plan, game_graph, current_configuration, node_ix):
                        self.move_plan.append(node_ix)
                    else:
                        current_configuration = JaguarPlayer.configuration_after_move(self.move_plan, game_graph, current_configuration)
                        self.move_plan = []

        return (current_configuration, 0)

    def render(self, screen, game_graph):

        '''
        deseneaza nodurile din planul de captura cu verde
        '''

        for node in self.move_plan:
            pygame.draw.circle(screen, (0, 255, 0), game_graph.nodes[node].draw_position, CIRCLE_RADIUS)

class Game:

    '''
    clasa care se ocupa de functionarea jocului si 
    a meniului
    '''

    def create_gui(self, ui_manager):

        '''
        functie care creaza meniul asa cum este specificat in cerinte
        '''

        half_margin = DRAW_MARGIN / 2
        quarter_margin = half_margin / 2
        half_quarter_margin = quarter_margin / 2
        
        dog_pos = (DRAW_MARGIN, DRAW_MARGIN)

        self.dogs_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (110, 25)), text="DOGS PLAYER", manager=ui_manager)

        dog_pos = (dog_pos[0], dog_pos[1] + quarter_margin + 25)

        self.human_dog_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (110, 25)),
                                             text='HUMAN',
                                             manager=ui_manager)

        dog_pos = (dog_pos[0], dog_pos[1] + half_quarter_margin + 25)

        self.minimax_dog_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (110, 25)),
                                             text='MINIMAX',
                                             manager=ui_manager)

        dog_pos = (dog_pos[0], dog_pos[1] + half_quarter_margin + 25)

        self.alphabeta_dog_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (110, 25)),
                                        text='ALPHA-BETA',
                                        manager=ui_manager)

        dog_pos = (dog_pos[0], dog_pos[1] + quarter_margin + 25)

        self.dogs_difficulty_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (110, 25)), text="DIFFICULTY", manager=ui_manager)

        dog_pos = (dog_pos[0], dog_pos[1] + quarter_margin + 25)

        self.one_dogs_difficulty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (30, 25)),
                                             text='1',
                                             manager=ui_manager)

        self.two_dogs_difficulty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0] + 30 + 10, dog_pos[1]), (30, 25)),
                                        text='2',
                                        manager=ui_manager)

        self.three_dogs_difficulty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0] + 60 + 20, dog_pos[1]), (30, 25)),
                                text='3',
                                manager=ui_manager)

        jaguar_pos = (DRAW_MARGIN + 110 + quarter_margin, DRAW_MARGIN)

        self.jaguar_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((jaguar_pos[0], jaguar_pos[1]), (110, 25)), text="JAGUAR PLAYER", manager=ui_manager)

        jaguar_pos = (jaguar_pos[0], jaguar_pos[1] + quarter_margin + 25)

        self.human_jaguar_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((jaguar_pos[0], jaguar_pos[1]), (110, 25)),
                                             text='HUMAN',
                                             manager=ui_manager)

        jaguar_pos = (jaguar_pos[0], jaguar_pos[1] + half_quarter_margin + 25)

        self.minimax_jaguar_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((jaguar_pos[0], jaguar_pos[1]), (110, 25)),
                                        text='MINIMAX',
                                        manager=ui_manager)
        
        jaguar_pos = (jaguar_pos[0], jaguar_pos[1] + half_quarter_margin + 25)

        self.alphabeta_jaguar_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((jaguar_pos[0], jaguar_pos[1]), (110, 25)),
                                        text='ALPHA-BETA',
                                        manager=ui_manager)

        jaguar_pos = (jaguar_pos[0], jaguar_pos[1] + quarter_margin + 25)

        self.jaguar_difficulty_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((jaguar_pos[0], jaguar_pos[1]), (110, 25)), text="DIFFICULTY", manager=ui_manager)

        jaguar_pos = (jaguar_pos[0], jaguar_pos[1] + quarter_margin + 25)

        self.one_jaguar_difficulty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((jaguar_pos[0], jaguar_pos[1]), (30, 25)),
                                             text='1',
                                             manager=ui_manager)

        self.two_jaguar_difficulty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((jaguar_pos[0] + 30 + 10, jaguar_pos[1]), (30, 25)),
                                        text='2',
                                        manager=ui_manager)

        self.three_jaguar_difficulty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((jaguar_pos[0] + 60 + 20, jaguar_pos[1]), (30, 25)),
                                text='3',
                                manager=ui_manager)

        dog_pos = (dog_pos[0], dog_pos[1] + quarter_margin + 25)

        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((dog_pos[0], dog_pos[1]), (220 + quarter_margin, 25)),
                                text='PLAY!',
                                manager=ui_manager)

        self.human_dog_button.select()
        self.human_jaguar_button.select()
        self.one_dogs_difficulty.select()
        self.one_jaguar_difficulty.select()


    def __init__(self, ui_manager):

        '''
        pregateste jocul si meniul
        '''

        self.game_state = 0
        self.dog_player_type = 0
        self.jaguar_player_type = 0
        self.dog_difficulty = 0
        self.jaguar_difficulty = 0
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.create_gui(ui_manager)

    def ui_update(self, event):

        '''
        functie care verifica butoanele care au fost apsate si
        actioneaza corespunzator
        '''

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.human_dog_button:
                    
                    self.human_dog_button.select()
                    self.minimax_dog_button.unselect()
                    self.alphabeta_dog_button.unselect()
                    self.dog_player_type = 0

                elif event.ui_element == self.minimax_dog_button:
                    
                    self.human_dog_button.unselect()
                    self.minimax_dog_button.select()
                    self.alphabeta_dog_button.unselect()
                    self.dog_player_type = 1

                elif event.ui_element == self.alphabeta_dog_button:
                    
                    self.human_dog_button.unselect()
                    self.minimax_dog_button.unselect()
                    self.alphabeta_dog_button.select()
                    self.dog_player_type = 2

                elif event.ui_element == self.human_jaguar_button:
                    
                    self.human_jaguar_button.select()
                    self.minimax_jaguar_button.unselect()
                    self.alphabeta_jaguar_button.unselect()
                    self.jaguar_player_type = 0

                elif event.ui_element == self.minimax_jaguar_button:

                    self.human_jaguar_button.unselect()
                    self.minimax_jaguar_button.select()
                    self.alphabeta_jaguar_button.unselect()
                    self.jaguar_player_type = 1

                elif event.ui_element == self.alphabeta_jaguar_button:

                    self.human_jaguar_button.unselect()
                    self.minimax_jaguar_button.unselect()
                    self.alphabeta_jaguar_button.select()
                    self.jaguar_player_type = 2  

                elif event.ui_element == self.one_dogs_difficulty:

                    self.one_dogs_difficulty.select()
                    self.two_dogs_difficulty.unselect()
                    self.three_dogs_difficulty.unselect()
                    self.dog_difficulty = 0
                
                elif event.ui_element == self.two_dogs_difficulty:

                    self.one_dogs_difficulty.unselect()
                    self.two_dogs_difficulty.select()
                    self.three_dogs_difficulty.unselect()
                    self.dog_difficulty = 1

                elif event.ui_element == self.three_dogs_difficulty:

                    self.one_dogs_difficulty.unselect()
                    self.two_dogs_difficulty.unselect()
                    self.three_dogs_difficulty.select()
                    self.dog_difficulty = 2

                elif event.ui_element == self.one_jaguar_difficulty:

                    self.one_jaguar_difficulty.select()
                    self.two_jaguar_difficulty.unselect()
                    self.three_jaguar_difficulty.unselect()
                    self.jaguar_difficulty = 0

                elif event.ui_element == self.two_jaguar_difficulty:

                    self.one_jaguar_difficulty.unselect()
                    self.two_jaguar_difficulty.select()
                    self.three_jaguar_difficulty.unselect()
                    self.jaguar_difficulty = 1

                elif event.ui_element == self.three_jaguar_difficulty:

                    self.one_jaguar_difficulty.unselect()
                    self.two_jaguar_difficulty.unselect()
                    self.three_jaguar_difficulty.select()
                    self.jaguar_difficulty = 2

                elif event.ui_element == self.play_button:

                    self.game_graph = GameGraph()
                    self.current_configuration = GameConfiguration(self.game_graph)     
                    self.current_configuration.debug_print(self.game_graph)   

                    self.game_state = 1

                    if self.dog_player_type == 0:
                        self.dog_player = HumanDogPlayer()
                    elif self.dog_player_type == 1:
                        self.dog_player = MinimaxDogPlayer(self.dog_difficulty)
                    elif self.dog_player_type == 2:
                        self.dog_player = AlphaBetaDogPlayer(self.dog_difficulty)

                    if self.jaguar_player_type == 0:
                        self.jaguar_player = HumanJaguarPlayer()
                    elif self.jaguar_player_type == 1:
                        self.jaguar_player = MinimaxJaguarPlayer(self.jaguar_difficulty)
                    elif self.jaguar_player_type == 2:
                        self.jaguar_player = AlphaBetaJaguarPlayer(self.jaguar_difficulty)

                    self.current_player = self.jaguar_player
                    
                    self.dog_think_times = []
                    self.jaguar_think_times = []
                    self.dog_generated_nodes = []
                    self.jaguar_generated_nodes = []

                    self.last_think_time = time.time()
                    self.start_game_time = time.time()
                    self.shown_times = False
                    self.game_running = True


    def update(self):

        '''
        functie update care se apeleaza la fiecare frame si apeleaza functia
        care decide ce mutare se va dace in timpul jocului. La sfarsitul jocului
        se afiseaza in consola informatiile cerute. Daca se apasa ESC, jocul se opreste.
        '''

        if self.game_state == 0:
            pass
        elif self.game_state == 1:

            current_winner = self.current_configuration.get_winner(self.game_graph)
            pygame_helper.update_input()

            keys=pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self.game_running = False

            if current_winner == -1 and self.game_running:

                new_configuration, generated_nodes = self.current_player.do_turn(self.game_graph, self.current_configuration)
                if new_configuration != self.current_configuration:
                    
                    current_time = time.time()
                    time_diff = current_time - self.last_think_time
                    self.last_think_time = current_time

                    new_configuration.debug_print(self.game_graph)

                    print("Thinking time: " + str(time_diff))

                    if self.dog_player == self.current_player:
                        self.dog_think_times.append(time_diff)
                        self.dog_generated_nodes.append(generated_nodes)
                        self.current_player = self.jaguar_player
                    else:
                        self.jaguar_think_times.append(time_diff)
                        self.jaguar_generated_nodes.append(generated_nodes)
                        self.current_player = self.dog_player
                    self.current_configuration = new_configuration
            else:
                if not self.shown_times:

                    if len(self.jaguar_think_times) > 0 and len(self.dog_think_times) > 0:
                        print("Dogs thinking times: ")
                        print("Minimum: " + str(min(self.dog_think_times)))
                        print("Maximum: " + str(max(self.dog_think_times)))
                        print("Average: " + str(sum(self.dog_think_times) / len(self.dog_think_times)))
                        sorted(self.dog_think_times)
                        print("Median: " + str(self.dog_think_times[int(len(self.dog_think_times) / 2)]))
                        print("--------------------------------------------------------------")
                        print("Jaguar thinking times: ")
                        print("Minimum: " + str(min(self.jaguar_think_times)))
                        print("Maximum: " + str(max(self.jaguar_think_times)))
                        print("Average: " + str(sum(self.jaguar_think_times) / len(self.jaguar_think_times)))
                        sorted(self.jaguar_think_times)
                        print("Median: " + str(self.jaguar_think_times[int(len(self.jaguar_think_times) / 2)]))
                        print("--------------------------------------------------------------")
                        print("Dogs generated nodes: ")
                        print("Minimum: " + str(min(self.dog_generated_nodes)))
                        print("Maximum: " + str(max(self.dog_generated_nodes)))
                        print("Average: " + str(sum(self.dog_generated_nodes) / len(self.dog_generated_nodes)))
                        sorted(self.dog_generated_nodes)
                        print("Median: " + str(self.dog_generated_nodes[int(len(self.dog_generated_nodes) / 2)]))
                        print("--------------------------------------------------------------")
                        print("Jaguar generated nodes: ")
                        print("Minimum: " + str(min(self.jaguar_generated_nodes)))
                        print("Maximum: " + str(max(self.jaguar_generated_nodes)))
                        print("Average: " + str(sum(self.jaguar_generated_nodes) / len(self.jaguar_generated_nodes)))
                        sorted(self.jaguar_generated_nodes)
                        print("Median: " + str(self.jaguar_generated_nodes[int(len(self.jaguar_generated_nodes) / 2)]))
                        print("--------------------------------------------------------------")
                        print("Game time: " + str(time.time() - self.start_game_time))
                        print("Dogs moves count: " + str(len(self.dog_think_times)))
                        print("Jaguar moves count: " + str(len(self.jaguar_think_times)))
                        
                        self.shown_times = True

                if pygame_helper.was_mouse_released() or (not self.game_running):
                    self.game_state = 0

    def render(self, screen):

        '''
        functie care deseneaza pe ecran toate lucrurile cerute (se apeleaza
        si functii de randare din alte clase in interiorul acestei clase)
        '''

        if self.game_state == 0:
            pass
        elif self.game_state == 1:

            turn_string = "DOGS TURN"
            if self.current_player == self.jaguar_player:
                turn_string = "JAGUAR TURN"

            text_surface = self.myfont.render(turn_string, False, (0, 0, 0))
            screen.blit(text_surface, (DRAW_MARGIN, DRAW_MARGIN / 2))

            self.game_graph.render_graph(screen)
            self.current_configuration.render(screen, self.game_graph)
            self.current_player.render(screen, self.game_graph)

            current_winner = self.current_configuration.get_winner(self.game_graph)
            if current_winner != -1:
                winner_string = "DOGS WON!"
                if current_winner == 1:
                    winner_string = "JAGUAR WON!"
                text_surface = self.myfont.render(winner_string, False, (0, 0, 0))
                screen.blit(text_surface, (DRAW_MARGIN, WINDOW_HEIGHT - DRAW_MARGIN * 2))

def main():
    
    '''
    aici incepe programul. Fereastra are titlu pus asa cum este
    scris in cerinte.
    '''

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Silviu St??ncioiu Jocul Adugo (cainii si jaguarul)')

    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

    running = True

    ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(ui_manager)

    while running:

        time_delta = clock.tick(60)/1000.0
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game.game_state == 0:
                game.ui_update(event)
                ui_manager.process_events(event)

        if game.game_state == 0:
            ui_manager.update(time_delta)

        game.update()

        screen.fill((255, 255, 255))

        game.render(screen)

        if game.game_state == 0:
            ui_manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

    pass

if __name__ == "__main__":
    main()