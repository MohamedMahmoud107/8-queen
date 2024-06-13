import tkinter as tk
import numpy as np


def init_pop(index):
    return np.random.randint(0, 8, (index, 8))


# initial population
#############################################################################
# f(x)=-p(x) because it choose the max value
# p(x)=the number of queen those can be eaten by specific queen

def calc_fitness(population):
    fitness_vals = []
    for x in population:
        penalty = 0
        for i in range(8):
            r = x[i]  # r is the current row i column of q
            for j in range(8):
                if i == j:  # j column of another queens
                    continue  # column don't repeat because each queen has a unique index from 0:7
                d = abs(i - j)
                if x[j] in [r, r - d, r + d]:
                    penalty += 1
        fitness_vals.append(penalty)
    return -1 * np.array(fitness_vals)


#####################################################################################
def selection(population, fitness_vals):
    probs = fitness_vals.copy()
    probs += abs(probs.min()) + 1
    probs = probs / probs.sum()
    N = len(population)
    ind = np.arange(N)  # [0:N-1]
    selected_indices = np.random.choice(ind, size=N, p=probs)  # selsct random from ind elements
    selected_population = population[selected_indices]
    return selected_population


#########################################################################################
def crossover(parent1, parent2, pc):
    r = np.random.random()
    if r < pc:  # (0:pc) will implement  the function
        m = np.random.randint(1,
                              8)  # because if i make the range between (0,8) and the programe choose 0 the parent will be the child
        child1 = np.concatenate([parent1[:m], parent2[m:]])
        child2 = np.concatenate([parent2[:m], parent1[m:]])
    else:
        child1 = parent1.copy()
        child2 = parent2.copy()
    return child1, child2


########################################################################################
def mutation(invidual, pm):
    r = np.random.random()
    if r < pm:
        m = np.random.randint(8)
        invidual[m] = np.random.randint(0, 8)
    return invidual


########################################################################################

def crossover_mutation(selected_pop, pc, pm):
    N = len(selected_pop)
    new_pop = np.empty((N, 8), dtype=int)
    for i in range(0, N, 2):  # in each itaration we check about 2 parent so we move by 2 steps
        parent1 = selected_pop[i]
        parent2 = selected_pop[i + 1]
        child1, child2 = crossover(parent1, parent2, pc)
        new_pop[i] = child1
        new_pop[i + 1] = child2
    for i in range(N):
        mutation(new_pop[i], pm)
    return new_pop


#####################################################################################################
def eight_queens(pop_size, max_generations, pc=.7, pm=0.01):
    population = init_pop(pop_size)
    best_fitness_overall = None
    for i_gen in range(max_generations):
        fitness_vals = calc_fitness(population)
        best_i = fitness_vals.argmax()  # return the max fitness
        best_fitness = fitness_vals[best_i]
        if best_fitness_overall is None or best_fitness > best_fitness_overall:  # check if best fitness = best fitness overall
            best_fitness_overall = best_fitness
            best_solution = population[best_i]
        print(f'\ri_gen = {i_gen:07} -f ={-best_fitness_overall : 02}',
              end='')  # the max nom of f(x)= -64 so i make 2 digit to -best_fitness_overall = 3
        if best_fitness == 0:  # the loop will end when the bestfitness_overall = 0
            print(" found the best solution")
            break
        selected_Pop = selection(population, fitness_vals)
        population = crossover_mutation(selected_Pop, pc, pm)
    print()
    col = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h',
    }
    list2 = []
    for i in range(8):
        c = col[i], best_solution[i]
        list2.append(c)
    print(list2)
    return best_solution


def eight_queens(pop_size, max_generations, pc=0.7, pm=0.01):
    population = init_pop(pop_size)
    best_fitness_overall = None
    for i_gen in range(max_generations):
        fitness_vals = calc_fitness(population)
        best_i = fitness_vals.argmax()
        best_fitness = fitness_vals[best_i]
        if best_fitness_overall is None or best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            best_solution = population[best_i]
        print(f'\ri_gen = {i_gen:07} -f ={-best_fitness_overall:02}', end='')
        if best_fitness == 0:
            print(" found the best solution")
            break
        selected_Pop = selection(population, fitness_vals)
        population = crossover_mutation(selected_Pop, pc, pm)
    print()
    col = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h',
    }
    list2 = []
    for i in range(8):
        c = col[i], best_solution[i]
        list2.append(c)
    print(list2)
    return best_solution


def place_queen(row, col):
    board.create_oval(col * 50 + 5, row * 50 + 5, (col + 1) * 50 - 5, (row + 1) * 50 - 5, fill="orange")


def display_solution(best_solution):
    for col, row in enumerate(best_solution):
        place_queen(row, col)


def create_gui(best_solution):
    global board
    root = tk.Tk()
    root.title("Eight Queens Problem")

    board = tk.Canvas(root, width=400, height=400)
    board.pack()

    for i in range(8):
        for j in range(8):
            color = "white" if (i + j) % 2 == 0 else "black"
            board.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color)

    display_solution(best_solution)

    root.mainloop()


best_solution = eight_queens(700, 1000000)
create_gui(best_solution)
