from ..strategy.crossover_strategy import CrossoverStrategy
from ..individual import Individual
import random

class HalfCrossover(CrossoverStrategy):
    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs a half-point crossover, splitting the genome in half and swapping segments.
        """
        crossover_point = int(len(parent1.genome) / 2)
        offspring1_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
        offspring2_genome = parent2.genome[:crossover_point] + parent1.genome[crossover_point:]
        
        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent1.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2

class OnePointCrossover(CrossoverStrategy):
    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs one-point crossover, selecting a random point and swapping genome segments after this point.
        """
        crossover_point = random.randint(1, len(parent1.genome) - 1)
        offspring1_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
        offspring2_genome = parent2.genome[:crossover_point] + parent1.genome[crossover_point:]
        
        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent1.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2

class TwoPointCrossover(CrossoverStrategy):
    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs two-point crossover, selecting two random points and swapping genome segments between them.
        """
        point1 = random.randint(1, len(parent1.genome) - 2)
        point2 = random.randint(point1 + 1, len(parent1.genome) - 1)
        
        offspring1_genome = parent1.genome[:point1] + parent2.genome[point1:point2] + parent1.genome[point2:]
        offspring2_genome = parent2.genome[:point1] + parent1.genome[point1:point2] + parent2.genome[point2:]
        
        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent2.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2

class UniformCrossover(CrossoverStrategy):
    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs uniform crossover, randomly selecting genes from each parent.
        """
        offspring1_genome = [random.choice([gene1, gene2]) for gene1, gene2 in zip(parent1.genome, parent2.genome)]
        offspring2_genome = [random.choice([gene1, gene2]) for gene1, gene2 in zip(parent2.genome, parent1.genome)]
        
        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent2.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2

class BlendCrossover(CrossoverStrategy):
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs blend crossover, generating offspring genes within an extended range around each gene pair.
        """
        offspring1_genome = []
        offspring2_genome = []
        
        for gene1, gene2 in zip(parent1.genome, parent2.genome):
            lower = min(gene1, gene2)
            upper = max(gene1, gene2)
            diff = upper - lower
            offspring1_genome.append(random.uniform(lower - self.alpha * diff, upper + self.alpha * diff))
            offspring2_genome.append(random.uniform(lower - self.alpha * diff, upper + self.alpha * diff))
        
        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent2.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2

class ArithmeticCrossover(CrossoverStrategy):
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs arithmetic crossover, averaging each gene pair according to a blending factor alpha.
        """
        offspring1_genome = [(self.alpha * gene1 + (1 - self.alpha) * gene2) for gene1, gene2 in zip(parent1.genome, parent2.genome)]
        offspring2_genome = [(self.alpha * gene2 + (1 - self.alpha) * gene1) for gene1, gene2 in zip(parent1.genome, parent2.genome)]
        
        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent2.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2

class PMXCrossover(CrossoverStrategy):
    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        """
        Performs partially matched crossover (PMX), suitable for permutation-based problems like the TSP.
        """
        size = len(parent1.genome)
        point1 = random.randint(0, size - 2)
        point2 = random.randint(point1 + 1, size - 1)

        offspring1_genome = parent1.genome[:]
        offspring2_genome = parent2.genome[:]

        # Swap the subsequences between point1 and point2
        offspring1_genome[point1:point2] = parent2.genome[point1:point2]
        offspring2_genome[point1:point2] = parent1.genome[point1:point2]

        offspring1 = Individual(parent1.dna, len(parent1.genome))
        offspring1.genome = offspring1_genome
        offspring2 = Individual(parent2.dna, len(parent2.genome))
        offspring2.genome = offspring2_genome
        
        return offspring1, offspring2
