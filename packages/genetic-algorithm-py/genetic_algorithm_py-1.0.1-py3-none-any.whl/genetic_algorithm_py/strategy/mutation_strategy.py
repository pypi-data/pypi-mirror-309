from ..individual import Individual

class MutationStrategy:
    def __init__(self, mutation_rate: float = 0.01):
        """Initialize the mutation strategy with a mutation rate.
        
        Args:
            mutation_rate (float): The probability of mutation occurring for each gene.
        """
        self.mutation_rate = mutation_rate

    def mutate(self, individual: Individual) -> Individual:
        """This method should be overridden by specific mutation strategies.
        
        Args:
            individual (Individual): The individual whose genome will be mutated.
            
        Returns:
            Individual: The mutated individual.
        """
        raise NotImplementedError("Mutation strategy must implement the mutate method.")
