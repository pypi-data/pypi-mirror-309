from ..individual import Individual
from ..population import Population

# Crossover Strategy Base Class
class CrossoverStrategy:
    def crossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        # This method should be overridden by subclasses to implement specific crossover strategies
        raise NotImplementedError("This method should be overridden by subclasses")
