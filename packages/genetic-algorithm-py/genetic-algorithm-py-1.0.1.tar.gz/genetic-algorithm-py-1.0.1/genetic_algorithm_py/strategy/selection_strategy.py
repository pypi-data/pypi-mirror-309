from ..individual import Individual
from ..population import Population

class SelectionStrategy:
    def select_parents(self, population: Population) -> tuple[Individual, Individual]:
        """Select two parents from the population.

        This method should be overridden by subclasses to implement specific parent selection strategies.
        
        Args:
            population (Population): The population from which parents are selected.
        
        Returns:
            tuple: A tuple containing two selected parents (Individual).
        """
        raise NotImplementedError("This method should be overridden by subclasses")
