# Import strategies and core classes for genetic algorithm components
from .strategy.selection_strategy import SelectionStrategy
from .strategy.mutation_strategy import MutationStrategy
from .strategy.crossover_strategy import CrossoverStrategy
from .strategy.fitness_strategy import FitnessStrategy
from .strategy.dna_strategy import DNAStrategy
from .population import Population
from .individual import Individual

class DNA:
    """
    Manages DNA-related operations using a specified DNAStrategy.
    """

    def __init__(self, dna_strategy: DNAStrategy):
        self.dna_strategy = dna_strategy

    def generate_genome(self, genome_size: int) -> list:
        """
        Generates a genome of the specified size.
        """
        return self.dna_strategy.generate_genome(genome_size)

    def get_random_genes(self, genes_size: int = 1) -> list:
        """
        Retrieves random genes of the specified size.
        """
        return self.dna_strategy.get_random_genes(genes_size)

    def get_genes(self) -> list:
        return self.dna_strategy.genes

    def get_target(self) -> list:
        return self.dna_strategy.target

    def get_selection(self) -> 'Selection':
        return self.dna_strategy.selection

    def get_crossover(self) -> 'Crossover':
        return self.dna_strategy.crossover

    def get_mutation(self) -> 'Mutation':
        return self.dna_strategy.mutation

    def get_fitness_function(self) -> 'FitnessFunction':
        return self.dna_strategy.fitness_function


class FitnessFunction:
    """
    Encapsulates a fitness evaluation function using a FitnessStrategy.
    """

    def __init__(self, fitness_strategy: FitnessStrategy):
        self.fitness_strategy = fitness_strategy

    def evaluate(self, genome:list):
        """
        Evaluates the fitness of a given genome.
        """
        return self.fitness_strategy.evaluate(genome)


class Selection:
    """
    Manages parent selection operations using a specified SelectionStrategy.
    """

    def __init__(self, selection_strategy: SelectionStrategy):
        self.selection_strategy = selection_strategy

    def select_parents(self, population: Population) -> tuple[Individual, Individual]:
        """
        Selects two parents from the population for crossover.
        """
        return self.selection_strategy.select_parents(population)


class Crossover:
    """
    Handles crossover operations between individuals using a specified CrossoverStrategy.
    """

    def __init__(self, crossover_strategy: CrossoverStrategy):
        self.crossover_strategy = crossover_strategy

    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs crossover between two parents to produce offspring.
        """
        return self.crossover_strategy.crossover(parent1, parent2)


class Mutation:
    """
    Manages mutation operations on individuals using a specified MutationStrategy.
    """

    def __init__(self, mutation_strategy: MutationStrategy):
        self.mutation_strategy = mutation_strategy

    def mutate(self, individual: Individual):
        """
        Mutates the given individual.
        """
        return self.mutation_strategy.mutate(individual)

    def set_mutation_rate(self, mutation_rate: float):
        """
        Sets the mutation rate for the mutation strategy.
        """
        self.mutation_strategy.mutation_rate = mutation_rate


class GeneticAlgorithm:
    """
    Executes the genetic algorithm using DNA, population, selection, crossover, and mutation strategies.
    """

    def __init__(self, dna: DNA, population_size: int, genome_size: int, mutation_rate: float):
        # Initialize components and parameters
        self.dna = dna
        self.mutation_rate = mutation_rate
        self.dna.get_mutation().set_mutation_rate(mutation_rate)
        self.currentGen = 0
        self.allBestIndividual = None
        self.population = Population(dna, population_size, genome_size)

    def run(self, generations: int) -> Individual:
        """
        Runs the genetic algorithm across the specified number of generations.
        """
        # Evaluate initial population
        self.population.evaluate_population()
        for i in range(generations):
            best_individual = self.run_single_generation()
        return best_individual

    def run_single_generation(self) -> Individual:
        """
        Runs a single generation: selection, crossover, mutation, and evaluation.
        """
        # Generate new offspring for the population
        new_population = []
        # Evaluate the new population if it's the first generation
        if self.currentGen == 0:
            self.population.evaluate_population()
        while len(new_population) < len(self.population.individuals):
            # Select parents for crossover
            parent1, parent2 = self.dna.get_selection().select_parents(self.population)

            # Apply crossover to generate offspring
            offspring1, offspring2 = self.dna.get_crossover().crossover(parent1, parent2)

            # Apply mutation to offspring
            self.dna.get_mutation().mutate(offspring1)
            self.dna.get_mutation().mutate(offspring2)

            # Add offspring to the new population
            new_population.extend([offspring1, offspring2])

        # Replace the old population with the new generation
        self.population.individuals = new_population[:len(self.population.individuals)]
        
        # Evaluate the new population
        self.population.evaluate_population()

        # Track the best individual in the current generation
        best_individual = self.population.get_best_individual()
        if self.allBestIndividual is None:
            self.allBestIndividual = best_individual
        elif best_individual.fitness > self.allBestIndividual.fitness:
            self.allBestIndividual = best_individual
        self.currentGen += 1
        print(f"Generation {self.currentGen}, Best Fitness: {best_individual.fitness}")
        return best_individual
