from ..strategy.fitness_strategy import FitnessStrategy

class CompairTargetFitness(FitnessStrategy):
    def __init__(self, target: list):
        self.target = target

    def evaluate(self, genome: list) -> float:
        """Calculates fitness based on how many genes in the genome match the target genome."""
        fitness = 0
        for i in range(len(genome)):
            if self.target[i] == genome[i]:
                fitness += 1
        return fitness


class MaximizeOnesFitness(FitnessStrategy):
    def evaluate(self, genome):
        """Calculates fitness as the total number of 1's in the genome."""
        return sum(genome)


class MinimizeDistanceFitness(FitnessStrategy):
    def __init__(self, target_value):
        super().__init__()
        self.target_value = target_value
    
    def evaluate(self, genome):
        """
        Calculates fitness as the negative distance to the target value.
        Assumes the genome represents a binary-encoded real value.
        """
        # Convert binary genome to decimal value
        value = sum(g * (2**i) for i, g in enumerate(reversed(genome)))
        return -abs(self.target_value - value)  # Negative distance (lower is better)


class WeightedSumFitness(FitnessStrategy):
    def __init__(self, weights):
        super().__init__()
        self.weights = weights

    def evaluate(self, genome):
        """Calculates fitness as the weighted sum of genome bits."""
        return sum(g * w for g, w in zip(genome, self.weights))
