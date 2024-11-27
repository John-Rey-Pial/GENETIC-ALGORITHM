import random

# Problem Data
classes = ["Math", "Physics"]
teachers = ["T1", "T2"]
rooms = ["R1", "R2"]
room_capacities = {"R1": 30, "R2": 40}
timeslots = ["T1", "T2"]
student_counts = {"Math": 25, "Physics": 35}

POPULATION_SIZE = 4
GENERATIONS = 10
MUTATION_RATE = 0.1

def generate_random_schedule():
    schedule = []

    for cls in classes:
        room = random.choice(rooms)
        timeslot = random.choice(timeslots)
        teacher = random.choice(teachers)
        schedule.append((cls, room, timeslot, teacher))
    # counter = 1
    # for r in schedule:
    #   print(f'Schedule {counter}: {r}')
    #   counter += 1
    return schedule

def calculate_fitness(schedule):
    penalty = 0

    # Constraint: No room capacity conflict
    for cls, room, _, _ in schedule:
        if student_counts[cls] > room_capacities[room]: 
            penalty -= 1

    # Constraint: No room conflict
    room_time = {}
    for _, room, timeslot, _ in schedule:
        if (room, timeslot) in room_time:
            penalty -= 1
        else:
            room_time[(room, timeslot)] = True

    # Constraint: No teacher conflict
    teacher_time = {}
    for _, _, timeslot, teacher in schedule:
        if (teacher, timeslot) in teacher_time:
            penalty -= 1
        else:
            teacher_time[(teacher, timeslot)] = True
    return penalty

def crossover(parent1, parent2):
    trait = random.randint(0, len(classes) - 1)
    child1 = parent1[:trait] + parent2[trait:]
    # print(f'PARENT 1 TRAIT: {parent1[:trait]}')
    # print(f'PARENT 2 TRAIT: {parent2[trait:]}')

    child2 = parent2[:trait] + parent1[trait:]
    # print(f'PARENT 1 TRAIT: {parent2[:trait]}')
    # print(f'PARENT 2 TRAIT: {parent1[trait:]}')
    # print(f'CHILD 1:{child1}')
    # print(f'CHILD 2:{child2}')
    return child1, child2

def mutate(schedule):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, len(schedule) - 1)
        cls, _, _, _ = schedule[index]
        schedule[index] = (cls, random.choice(rooms), random.choice(timeslots), random.choice(teachers))
    return schedule

def get_fitness(individual):
    return individual[1]

# Genetic Algorithm
def genetic_algorithm():

    # Step 1: Population
    population = [generate_random_schedule() for _ in range(POPULATION_SIZE)]
    # for p in range(len(population)):
    #   print(f'Schedule {p}: {population[p]}')

    for generation in range(GENERATIONS):
        print(f'---------------------------------------------------------------\nGENERATION {generation}\n---------------------------------------------------------------')
        for pop in population:
          print(f'New Schedule: {pop}')
        # Step 2: Check Fitness
        fitness_scores = [(schedule, calculate_fitness(schedule)) for schedule in population]
        for f in range(len(fitness_scores)):
          print(f'Schedule {f}: {fitness_scores[f]}')

        fitness_scores.sort(key=get_fitness, reverse=True)
        for f in range(len(fitness_scores)):
          print(f'Schedule {f}: {fitness_scores[f]}')


        # Step 3: Natural Selection (Select 50%)
        selected = [schedule for schedule, _ in fitness_scores[:POPULATION_SIZE // 2]]
        for select in selected:
          print(f'Selected: {select}')

        # Step 4: Crossover
        next_generation = []
        counter = 1
        while len(next_generation) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population, 2)
            print(f'Pair {counter}')
            print(f'PARENT 1: {parent1}')
            print(f'PARENT 2: {parent2}')
            
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(child1)
            next_generation.append(child2)
            print(f'CHILD 1: {child1}')
            print(f'CHILD 2: {child2}')
            counter += 1

        # Step 4: Mutation
        population = [mutate(schedule) for schedule in next_generation]
        for pop in population:
          print(f'MUTATED CHILD: {pop}')

        # Debug: Best fitness in the current generation
        best_fitness = fitness_scores[0][1]
        print(f"Generation: {generation + 1}\nBest Fitness score: {best_fitness}")

        # If the best fitness score is acquired (0), end the loop
        if best_fitness == 0:
            break
    best_fitness_schedule = fitness_scores[0][0]
    return best_fitness_schedule

# Run Genetic Algorithm
best_schedule = genetic_algorithm()

# Display the result
print("\nBest Schedule:")
for cls, room, timeslot, teacher in best_schedule:
    print(f"Class: {cls}, Room: {room}, Timeslot: {timeslot}, Teacher: {teacher}")
