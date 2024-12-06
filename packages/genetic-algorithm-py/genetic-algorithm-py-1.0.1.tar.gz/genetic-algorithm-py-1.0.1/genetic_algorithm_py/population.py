from .individual import Individual
from typing import TYPE_CHECKING

# Import DNA only for type hinting to prevent circular imports
if TYPE_CHECKING:
    from .algorithm import DNA

class Population:
    """
    Represents a population in the genetic algorithm, consisting of multiple individuals.
    Each individual is evaluated based on its fitness, and the population can track the best individual.
    """

    def __init__(self, dna: 'DNA', population_size: int, genome_size: int):
        """
        Initializes the population with a specified number of individuals, each with a genome of specified size.
        
        Parameters:
            dna (DNA): The DNA strategy to be used for each individual in the population.
            population_size (int): The number of individuals in the population.
            genome_size (int): The length of the genome for each individual.
        """
        self.individuals = [Individual(dna, genome_size) for _ in range(population_size)]

    def evaluate_population(self) -> None:
        """
        Evaluates the fitness of each individual in the population.
        """
        for individual in self.individuals:
            individual.calculate_fitness()

    def get_best_individual(self) -> Individual:
        """
        Finds and returns the individual with the highest fitness in the population.
        
        Returns:
            Individual: The individual with the highest fitness score.
        """
        return max(self.individuals, key=lambda ind: ind.fitness)
