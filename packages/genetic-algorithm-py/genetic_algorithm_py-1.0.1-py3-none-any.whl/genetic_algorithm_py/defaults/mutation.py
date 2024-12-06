import random
from ..strategy.mutation_strategy import MutationStrategy
from ..individual import Individual

class MultiElementMutation(MutationStrategy):
    def mutate(self, individual: Individual):
        """Mutates multiple elements in the individual's genome based on mutation rate."""
        genome = individual.genome
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                genome[i] = individual.dna.get_random_genes()[0]  # Flip the bit
        return individual

class ElementMutation(MutationStrategy):
    def mutate(self, individual: Individual):
        """Mutates a single element in the individual's genome based on mutation rate."""
        genome = individual.genome
        if random.random() < self.mutation_rate:
            i = random.randint(0, len(genome) - 1)
            genome[i] = individual.dna.get_random_genes()[0]  # Flip the bit
        return individual

class BitFlipMutation(MutationStrategy):
    def mutate(self, individual: Individual):
        """Flips a bit in the individual's genome based on mutation rate."""
        genome = individual.genome
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                genome[i] = 1 - genome[i]  # Flip the bit
        return individual

class SwapMutation(MutationStrategy):
    def mutate(self, individual: Individual):
        """Swaps two elements in the individual's genome based on mutation rate."""
        genome = individual.genome
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(genome)), 2)  # Select two indices
            genome[idx1], genome[idx2] = genome[idx2], genome[idx1]  # Swap
        
        return individual

class ScrambleMutation(MutationStrategy):
    def mutate(self, individual):
        """Randomly scrambles a subset of the individual's genome based on mutation rate."""
        genome = individual.genome
        if random.random() < self.mutation_rate:
            start, end = sorted(random.sample(range(len(genome)), 2))
            subset = individual.dna.get_random_genes(end - start)
            random.shuffle(subset)
            genome[start:end] = subset
        return individual

class SegmentSwapMutation(MutationStrategy):
    def mutate(self, individual):
        """Swaps two segments of the individual's genome based on mutation rate."""
        genome = individual.genome
        if random.random() < self.mutation_rate:
            start1, end1 = sorted(random.sample(range(len(genome)), 2))
            start2, end2 = sorted(random.sample(range(len(genome)), 2))
            # Swap two segments of the genome
            genome[start1:end1], genome[start2:end2] = genome[start2:end2], genome[start1:end1]
        return individual

class GaussianMutation(MutationStrategy):
    def __init__(self, mutation_rate=0.01, sigma=0.1):
        """Initializes Gaussian mutation with a standard deviation for the mutation."""
        super().__init__(mutation_rate)
        self.sigma = sigma  # Standard deviation for Gaussian mutation

    def mutate(self, individual):
        """Applies Gaussian mutation to the individual's genome."""
        genome = individual.genome
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                genome[i] += random.gauss(0, self.sigma)  # Apply Gaussian mutation
        return individual

class BoundaryMutation(MutationStrategy):
    def __init__(self, mutation_rate=0.01, min_value=-1.0, max_value=1.0):
        """Initializes boundary mutation with specified mutation rate and boundaries."""
        super().__init__(mutation_rate)
        self.min_value = min_value
        self.max_value = max_value

    def mutate(self, individual):
        """Mutates an individual's genome within the specified boundaries."""
        genome = individual.genome
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                # Mutate the gene within the specified boundary
                genome[i] = random.uniform(self.min_value, self.max_value)
        return individual

class PolynomialMutation(MutationStrategy):
    def __init__(self, mutation_rate=0.01, eta=20.0):
        """Initializes polynomial mutation with mutation rate and distribution index."""
        super().__init__(mutation_rate)
        self.eta = eta  # Distribution index for the polynomial mutation

    def mutate(self, individual):
        """Applies polynomial mutation to the individual's genome."""
        genome = individual.genome
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                delta = random.random()  # Random value between 0 and 1
                if delta < 0.5:
                    genome[i] += (1 - genome[i]) * (delta ** (self.eta))
                else:
                    genome[i] -= genome[i] * ((1 - delta) ** (self.eta))
        return individual
