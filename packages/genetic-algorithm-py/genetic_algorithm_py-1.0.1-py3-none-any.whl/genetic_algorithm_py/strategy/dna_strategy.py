import random
from ..defaults.selection import RouletteWheelSelection
from ..defaults.crossover import HalfCrossover
from ..defaults.mutation import ElementMutation
from ..defaults.fitness_function import MaximizeOnesFitness
from .selection_strategy import SelectionStrategy
from .crossover_strategy import CrossoverStrategy
from .mutation_strategy import MutationStrategy
from .fitness_strategy import FitnessStrategy

# DNA Strategy class that defines genetic algorithm behavior
class DNAStrategy:
    def __init__(self, genes: list, target: list = None,
                duplicate_genomes: bool = True,
                selection_strategy: SelectionStrategy = RouletteWheelSelection(),
                crossover_strategy: CrossoverStrategy = HalfCrossover(),
                mutation_strategy: MutationStrategy = ElementMutation(),
                fitness_strategy: FitnessStrategy = MaximizeOnesFitness()):
        # Import necessary classes after class definition
        from ..algorithm import Selection, Crossover, Mutation, FitnessFunction
        # Initialize strategy objects
        self.selection = Selection(selection_strategy)
        self.crossover = Crossover(crossover_strategy)
        self.mutation = Mutation(mutation_strategy)
        self.fitness_function = FitnessFunction(fitness_strategy)
        # Initialize genes, target, and genome duplication flag
        self.genes = genes
        self.target = target
        self.duplicate_genomes = duplicate_genomes

    # Prevent subclass from overriding __init__ method
    def __init_subclass__(cls, **kwargs):
        # Check if the subclass has overridden __init__
        if '__init__' in cls.__dict__:
            raise TypeError(f"{cls.__name__} cannot override the __init__ method.")
        super().__init_subclass__(**kwargs)

    # Generate a genome of specified size
    def generate_genome(self, genome_size: int) -> list:
        if self.duplicate_genomes:
            # If duplicates are allowed, select genes with replacement
            return random.choices(self.genes, k=genome_size)
        else:
            # If no duplicates, ensure genome size doesn't exceed gene length
            if genome_size > len(self.genes):
                raise ValueError("Error: Genome size must be less than or equal to the length of genes.")
            else:
                # Shuffle genes and return a subset of the specified size
                random.shuffle(self.genes)
                return self.genes[:genome_size]

    # Get a list of random genes
    def get_random_genes(self, genes_size: int = 1) -> list:
        return random.choices(self.genes, k=genes_size)
