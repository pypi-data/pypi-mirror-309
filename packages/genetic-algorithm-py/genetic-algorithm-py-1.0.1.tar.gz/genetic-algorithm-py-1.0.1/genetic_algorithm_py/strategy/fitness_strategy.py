class FitnessStrategy:
    def evaluate(self, genome:list)->float:
        """Evaluate the fitness of an individual based on its genome.
        
        This method should be overridden by subclasses to implement specific fitness calculations.
        """
        raise NotImplementedError("Subclasses must implement the evaluate method.")
