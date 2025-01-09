# -*- coding: utf-8 -*-
"""Copy of Vehicle Routing Problem.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/175HhEZsHA9UfJDOJrZ8GyqQqH0hRNtV6
"""

!pip install matplotlib deap

import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base,creator,tools,algorithms

num_locations=10
locations=[(random.randint(0,100),random.randint(0,100)) for _ in range(num_locations)]
depot=(50,50)
num_vehicles=3

creator.create("FitnessMin",base.Fitness,weights=(-1.0,-1.0))
creator.create("Individual",list,fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(num_locations), num_locations)
toolbox.register("individual", tools.initIterate,creator.Individual,toolbox.indices)
toolbox.register("population", tools.initRepeat,list,toolbox.individual)

def evalVRP(individual):
    distances=[]
    total_distance=0
    for i in range(num_vehicles):
        vechicle_route=[depot]+[locations[individual[j]] for j in range(i,len(individual),num_vechicles)]+[depot]
        vechicle_distance=0
        for k in range(len(vechicle_route)-1):
            loc1=vechicle_route[k]
            loc2=vechicle_route[k+1]
            vechicle_distance+=np.sqrt((loc2[0]-loc1[0])**2 + (loc2[1]-loc1[1])**2)
        total_distance+=vechicle_distance
        distances.append(vechicle_distance)
    balance_penalty=np.std(distances)
    return total_distance,balance_penalty


toolbox.register("evaluate",evalVRP)

#SOLUTION CODE


#Fitness Function
def evalVRP(individual):
    total_distance = 0
    distances = []  # Track distance traveled by each vehicle for balance calculation
    # Split the list of locations among vehicles, ensuring each starts and ends at the depot
    for i in range(num_vehicles):

        vehicle_route = [depot] + [locations[individual[j]] for j in range(i, len(individual), num_vehicles)] + [depot]

        # Calculate total distance traveled by this vehicle
        vehicle_distance = sum(np.linalg.norm(np.array(vehicle_route[k+1]) - np.array(vehicle_route[k])) for k in range(len(vehicle_route)-1))

        total_distance += vehicle_distance
        distances.append(vehicle_distance)

    balance_penalty = np.std(distances)  # Use standard deviation of distances as a penalty for imbalance among vehicles
    return total_distance, balance_penalty
toolbox.register("evaluate",evalVRP)



toolbox.register("mate",tools.cxPartialyMatched)
toolbox.register("mutate",tools.mutShuffleIndexes,indpb=0.05)
toolbox.register("select",tools.selTournament,tournsize=3)

def plot_routes(individual, title="Routes"):
    plt.figure()
    # Plot locations as blue dots and the depot as a red square
    for (x, y) in locations:
        plt.plot(x, y, 'bo')
    plt.plot(depot[0], depot[1], 'rs')

    # Draw routes for each vehicle
    for i in range(num_vehicles):
        vehicle_route = [depot] + [locations[individual[j]] for j in range(i, len(individual), num_vehicles)] + [depot]
        plt.plot(*zip(*vehicle_route), '-', 'rs')

    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()

individual = [0, 1, 2, 3, 4,5,6,7,8,9]
plot_routes(individual, title="Optimal Route")

# Running the Genetic Algorithm
# Running the Genetic Algorithm
def main():
    random.seed(42)  # Seed for reproducibility
    pop = toolbox.population(n=300)  # Generate initial population
    hof = tools.HallOfFame(1)  # Hall of Fame to store the best individual

    # Setup statistics to track
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    # Run the genetic algorithm
    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 300, stats=stats, halloffame=hof)

    # Plot the best route found
    plot_routes(hof[0], "Optimal Route")
    return pop, stats, hof

if __name__ == "__main__":
    main()
