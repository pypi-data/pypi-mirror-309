import random
import math
from ..strategy.selection_strategy import SelectionStrategy
from ..individual import Individual
from ..population import Population

# Roulette Wheel Selection
class RouletteWheelSelection(SelectionStrategy):
    def select_parents(self, population: Population) -> tuple[Individual, Individual]:
        # Get fitness values of all individuals in the population
        fitness_values = [individual.fitness for individual in population.individuals]
        total_fitness = sum(fitness_values)
        # Calculate selection probabilities based on fitness
        selection_probs = [fitness / total_fitness for fitness in fitness_values]
        # Select two parents based on the calculated probabilities
        return random.choices(population.individuals, weights=selection_probs, k=2)

# Tournament Selection
class TournamentSelection(SelectionStrategy):
    def __init__(self, tournament_size=3):
        # Initialize tournament size
        self.tournament_size = tournament_size

    def select_parents(self, population):
        # Select a random sample of individuals for the tournament
        tournament = random.sample(population.individuals, self.tournament_size)
        # Select the individual with the highest fitness as the parent
        return max(tournament, key=lambda ind: ind.fitness)

# Rank Selection
class RankSelection(SelectionStrategy):
    def select_parents(self, population):
        # Sort population by fitness
        sorted_population = sorted(population.individuals, key=lambda ind: ind.fitness)
        # Assign rank weights based on the sorted order
        rank_weights = [i for i in range(1, len(population.individuals) + 1)]
        # Select one parent based on rank weights
        selected = random.choices(sorted_population, weights=rank_weights, k=1)
        return selected[0]

# Stochastic Universal Sampling (SUS)
class StochasticUniversalSampling(SelectionStrategy):
    def __init__(self, num_select=2):
        # Initialize number of parents to select
        self.num_select = num_select

    def select_parents(self, population):
        # Calculate total fitness and point distance between selections
        total_fitness = sum(ind.fitness for ind in population.individuals)
        point_distance = total_fitness / self.num_select
        start_point = random.uniform(0, point_distance)
        pointers = [start_point + i * point_distance for i in range(self.num_select)]
        selected = []
        for point in pointers:
            cumulative = 0
            # Select individuals based on fitness distribution
            for ind in population.individuals:
                cumulative += ind.fitness
                if cumulative >= point:
                    selected.append(ind)
                    break
        return selected

# Elitism Selection
class ElitismSelection(SelectionStrategy):
    def __init__(self, num_elites=2):
        # Initialize the number of elite individuals to select
        self.num_elites = num_elites

    def select_parents(self, population):
        # Sort population by fitness in descending order
        sorted_population = sorted(population.individuals, key=lambda ind: ind.fitness, reverse=True)
        # Return the top 'num_elites' individuals as parents
        return tuple(sorted_population[:self.num_elites])

# Truncation Selection
class TruncationSelection(SelectionStrategy):
    def __init__(self, percentage=0.5):
        # Initialize the percentage of the top individuals to select
        self.percentage = percentage

    def select_parents(self, population):
        # Sort population by fitness in descending order
        sorted_population = sorted(population.individuals, key=lambda ind: ind.fitness, reverse=True)
        # Calculate number of individuals to select based on percentage
        num_to_select = int(len(population.individuals) * self.percentage)
        # Return the top individuals based on truncation percentage
        return sorted_population[:num_to_select]

# Boltzmann Selection
class BoltzmannSelection(SelectionStrategy):
    def __init__(self, temperature=1.0):
        # Initialize temperature for Boltzmann selection
        self.temperature = temperature

    def select_parents(self, population):
        # Calculate Boltzmann weights based on fitness and temperature
        boltzmann_weights = [math.exp(ind.fitness / self.temperature) for ind in population.individuals]
        total = sum(boltzmann_weights)
        # Normalize the weights to get selection probabilities
        probabilities = [weight / total for weight in boltzmann_weights]
        # Select one parent based on calculated probabilities
        selected = random.choices(population.individuals, weights=probabilities, k=2)
        return tuple(selected)

# Steady-State Selection
class SteadyStateSelection(SelectionStrategy):
    def __init__(self, num_replacements=2):
        # Initialize number of replacements in steady-state selection
        self.num_replacements = num_replacements

    def select_parents(self, population):
        # Sort population by fitness in ascending order
        sorted_population = sorted(population.individuals, key=lambda ind: ind.fitness)
        # Return the least fit individuals for replacement
        return sorted_population[-self.num_replacements:]

# Rank-Biased Selection
class RankBiasedSelection(SelectionStrategy):
    def __init__(self, bias_factor=0.7):
        # Initialize bias factor for rank-biased selection
        self.bias_factor = bias_factor

    def select_parents(self, population):
        # Sort population by fitness
        sorted_population = sorted(population.individuals, key=lambda ind: ind.fitness)
        num_individuals = len(population.individuals)
        # Assign rank-based weights with a bias towards higher ranks
        weights = [(self.bias_factor ** (num_individuals - i)) for i in range(num_individuals)]
        # Select one parent based on rank-biased selection weights
        selected = random.choices(sorted_population, weights=weights, k=2)
        return tuple(selected)
