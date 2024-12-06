from typing import TYPE_CHECKING

# Import DNA only for type hinting to prevent circular imports
if TYPE_CHECKING:
    from .algorithm import DNA

class Individual:
    """
    Represents an individual in the genetic algorithm, defined by its DNA and fitness score.
    Each individual has a genome, which is evaluated for fitness based on the fitness function
    defined in the DNA strategy.
    """

    def __init__(self, dna: 'DNA', genome_size: int):
        """
        Initializes an individual with DNA and a randomly generated genome.
        Calculates fitness if a fitness function is defined.
        
        Parameters:
            dna (DNA): The DNA strategy to be used for generating and evaluating the genome.
            genome_size (int): The length of the genome.
        """
        self.dna = dna
        self.genome = self.generate_genome(genome_size)
        self.fitness = None

        # Calculate fitness if a fitness function is available
        fitness_function = self.dna.get_fitness_function()
        if fitness_function is not None:
            self.fitness = self.calculate_fitness()

    def generate_genome(self, genome_size: int) -> list:
        """
        Generates a genome of the specified size using the DNA strategy.
        
        Parameters:
            genome_size (int): The size of the genome to be generated.
        
        Returns:
            list: The generated genome.
        """
        return self.dna.generate_genome(genome_size)

    def calculate_fitness(self) -> float:
        """
        Calculates and returns the fitness of the individual based on its genome.
        
        Returns:
            float: The fitness score of the individual.
        """
        self.fitness = self.dna.get_fitness_function().evaluate(self.genome)
        return self.fitness
