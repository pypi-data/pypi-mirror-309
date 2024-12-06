
# Genetic Algorithm Py Documentation


`genetic_algorithm_py` is a Python library that provides a customizable genetic algorithm framework. It includes base classes for genetic algorithms, such as DNA representation, population management, fitness evaluation, and various selection, crossover, and mutation strategies. This library is designed for users to easily implement and test their own genetic algorithms for optimization problems.

## Features
- Customizable selection, crossover, mutation, and fitness strategies.
- Predefined strategies in the `defaults` module for common use cases.
- Modular design to facilitate integration with different types of genetic algorithms.

---

## Table of Contents

* [Installation](#installation)
* [Getting Started](#getting-started)
* [Classes Structure](#classes-structure)
* [Classes and Modules](#classes-and-modules)
  * [GeneticAlgorithm](#geneticalgorithm)
  * [DNA](#dna)
  * [Individual](#individual)
  * [Population](#population)
  * [FitnessFunction](#fitnessfunction)
  * [Selection](#selection)
  * [Crossover](#crossover)
  * [Mutation](#mutation)
  * [Strategies.](#strategies)
    * [SelectionStrategy](#selectionstrategy)
    * [MutationStrategy](#mutationstrategy)
    * [CrossoverStrategy](#crossoverstrategy)
    * [FitnessStrategy](#fitnessstrategy)
    * [DNAStrategy](#dnastrategy)
  * [Defaults.](#defaults)
    * [Fitness Functions](#fitness-functions)
    * [Selection Methods](#selection-Methods)
    * [Crossover Methods](#crossover-methods)
    * [Mutation Methods](#mutation-methods)
* [Examples](#examples)
* [Contributing](#contributing)
* [License](#license)

---

## Installation

To install `genetic-algorithm-py`, use:

```bash
pip install genetic-algorithm-py
```

---

## Getting Started

To run a simple genetic algorithm with default strategies, follow this example:

```python
from genetic_algorithm_py import GeneticAlgorithm, DNA, Population
from genetic_algorithm_py.strategy import DNAStrategy
from genetic_algorithm_py.defaults import RouletteWheelSelection, MaximizeOnesFitness, HalfCrossover, ElementMutation

# Define genes and target
genes = [0, 1]
target = [1] * 10

# Set up DNAStrategy with default strategies
dna_strategy = DNAStrategy(
    genes=genes,
    target=target,
    selection_strategy=RouletteWheelSelection(),
    crossover_strategy=HalfCrossover(),
    mutation_strategy=ElementMutation(),
    fitness_strategy=MaximizeOnesFitness()
)

# Initialize DNA with the DNAStrategy
dna = DNA(dna_strategy)

# Run the Genetic Algorithm
ga = GeneticAlgorithm(dna=dna, population_size=100,genome_size=len(target), mutation_rate=0.01)
ga.run(generations=50)
print("best Individual : ", ga.allBestIndividual.genome)
print("best Fitness : ", ga.allBestIndividual.fitness)
```

---

## Classes Structure

The library is organized into modules for algorithm, strategies, and default implementations for fitness, selection, crossover, and mutation.

```plaintext
genetic_algorithm_py.
├── GeneticAlgorithm              # Main class that executes the genetic algorithm using various strategies
├── Individual                    # Represents a single individual (genome) in the population
├── Population                    # Represents the entire population of individuals (genomes) in the genetic algorithm
├── DNA                            # Manages DNA-related operations (like creating a genome, mutations, etc.)
├── FitnessFunction               # Defines how fitness is evaluated for individuals
├── Selection                      # Contains logic for selecting individuals from the population for reproduction
├── Crossover                      # Defines how crossover (genetic material exchange) is performed between parents
├── Mutation                       # Defines how mutation is applied to individuals (genes) in the population
├── strategy.                      # Folder containing various strategy classes that define the behavior of the algorithm
│   ├── SelectionStrategy          # Interface or base class for selection strategies (e.g., Roulette Wheel, Tournament)
│   ├── MutationStrategy           # Interface or base class for mutation strategies (e.g., Element Mutation, Gaussian Mutation)
│   ├── CrossoverStrategy         # Interface or base class for crossover strategies (e.g., OnePoint, TwoPoint, Uniform)
│   ├── FitnessStrategy            # Interface or base class for fitness evaluation strategies (e.g., Maximize OneseFitness)
│   └── DNAStrategy                # Defines strategies for DNA-related operations like selection, crossover, and mutation
├── defaults/                      # Folder containing default strategy classes that are commonly used or predefined
│   ├── MaximizeOnesFitness       # Fitness strategy that maximizes the number of ones in the genome
│   ├── MinimizeDistanceFitness   # Fitness strategy that minimizes the distance to a target solution
│   ├── WeightedSumFitness        # Fitness strategy that calculates a weighted sum of certain values
│   ├── CompairTargetFitness      # Fitness strategy that compares the genome to a target and evaluates the match
│   ├── RouletteWheelSelection    # Selection strategy based on the roulette wheel method
│   ├── TournamentSelection       # Selection strategy based on tournament-style competition
│   ├── StochasticUniversalSampling  # Selection strategy that samples individuals stochastically using a universal sampling technique
│   ├── RankSelection             # Selection strategy where individuals are selected based on their rank in the population
│   ├── ElitismSelection          # Selection strategy that always selects the best individuals from the population
│   ├── TruncationSelection       # Selection strategy that truncates the population, selecting only the best individuals
│   ├── RankBiasedSelection       # Selection strategy that biases selection toward higher-ranked individuals
│   ├── BoltzmannSelection        # Selection strategy based on Boltzmann distribution
│   ├── SteadyStateSelection      # Selection strategy that selects a subset of the population for reproduction, ensuring constant population size
│   ├── OnePointCrossover         # Crossover strategy that combines genes from two parents at a single crossover point
│   ├── UniformCrossover          # Crossover strategy where genes from both parents are chosen randomly
│   ├── HalfCrossover             # Crossover strategy that mixes half of the genes from one parent and the other half from another
│   ├── TwoPointCrossover         # Crossover strategy that uses two points to swap genetic material between parents
│   ├── BlendCrossover            # Crossover strategy that blends genes from two parents with a smooth transition
│   ├── ArithmeticCrossover       # Crossover strategy that combines genes using arithmetic operations
│   ├── PMXCrossover              # Partially Matched Crossover (PMX) strategy that ensures offspring have valid genetic material
│   ├── SwapMutation              # Mutation strategy that swaps two genes in a genome
│   ├── GaussianMutation          # Mutation strategy that modifies genes with a Gaussian distribution
│   ├── PolynomialMutation        # Mutation strategy that applies polynomial changes to genes
│   ├── ElementMutation           # Mutation strategy that randomly changes a single gene
│   ├── MultiElementMutation      # Mutation strategy that changes multiple genes in a genome
│   ├── BitFlipMutation           # Mutation strategy that flips bits in a binary genome
│   ├── ScrambleMutation          # Mutation strategy that scrambles genes within a portion of the genome
│   ├── SegmentSwapMutation      # Mutation strategy that swaps segments of genes in the genome
│   └── BoundaryMutation          # Mutation strategy that modifies genes by pushing them to their boundary values
```

---

## Classes and Modules

### GeneticAlgorithm

The main class for managing the algorithm's flow.

- **Parameters**
  - `dna`: Instance of the DNA class, configured with a specific DNAStrategy.
  - `population_size`: Number of individuals in the population.
  - `genome_size`: Length of each genome.
  - `mutation_rate`: Probability of mutation per gene must be between [0,1].

- **Attributes**:
  - `dna` : Instance of the DNA class, configured with a specific DNAStrategy.
  - `mutation_rate` : Probability of mutation per gene must be between [0,1].
  - `currentGen` : Current number of generation.
  - `allBestIndividual` : best Individual of all generations.
  - `population`: Holds the population of individuals.

- **Methods**:
  - `run(generations: int)-> Individual`: Runs the algorithm for a specified number of generations and returns best Individual last generation.
  - `run_single_generation()-> Individual` : Runs the algorithm for single generation and returns best Individual.

### DNA

The `DNA` class manages genetic operations by using a `DNAStrategy` that defines how selection, crossover, mutation, and fitness evaluation are handled.

- **Parameters**
  - `dna_strategy`: An instance of `DNAStrategy`.

- **Attributes**
  - `dna_strategy`: An instance of `DNAStrategy`.

- **Methods**
  - `generate_genome(genome_size: int) -> list` : Generates Genome of Given size as list and returns it.
  - `get_random_genes(genes_size: int) -> list` : Returns list of random genes of given size from genome.
  - `get_genes() -> list` : returns the list of total available genes from which genome is generated.
  - `get_target() -> list` : returns target if any.
  - `get_selection(self) -> Selection` : returns the `Selection` object which contains `SelectionStrategy`.
  - `get_crossover() -> Crossover` : returns the `Crossover` object which contains `CrossoverStrategy`.
  - `get_mutation() -> Mutation` : returns the `Mutation` object which contains `MutationStrategy`.
  - `get_fitness_function() -> FitnessFunction` : returns the `FitnessFunction` object which contains `FitnessStrategy`.

### Individual

Represents a single member of the population with a genome, DNA and associated fitness.

- **Parameters**
  - `dna`: Instance of the DNA class, configured with a specific DNAStrategy.
  - `genome_size`: Length of each genome.

- **Attributes**
  - `genome`: A list of genes representing the individual.
  - `fitness`: A float representing the individual's fitness score.
  - `dna` : Instance of the DNA class, configured with a specific DNAStrategy.
  
- **Methods**
  - `generate_genome(genome_size: int) -> list` : Generates Genome of Given size as list and returns it.
  - `calculate_fitness() -> float` : Recalculate fitness based on the provided fitness strategy and returns it.

### Population
Represents a collection of individuals in the genetic algorithm.

- **Parameters**
  - `dna`: Instance of the DNA class, configured with a specific DNAStrategy.
  - `population_size`: Number of individuals in the population.
  - `genome_size`: Length of each genome.

- **Attributes**
  - `individuals`: A list of `Individual` objects.

- **Methods**
  - `evaluate_population()`: Calculates the fitness of each individual using the fitness strategy.
  - `get_best_individual() -> Individual` : retuns an individual with highest fitness of all individuals in current population.

### FitnessFunction

- **Parameters**
  - `fitness_strategy`: An instance of `FitnessStrategy`.

- **Attributes**
  - `fitness_strategy`: An instance of `FitnessStrategy`.

- **Methods**
  - `evaluate(genome : list)` : Evaluates Fitness of all genes in Genome based on given `FitnessStrategy`.

### Selection

- **Parameters**
  - `selection_strategy`: An instance of `SelectionStrategy`.

- **Attributes**
  - `selection_strategy`: An instance of `SelectionStrategy`.

- **Methods**
  - `select_parents( population: Population) -> tuple[Individual, Individual]` : Selects two Individuals based on  given `SelectionStrategy` and returns tuple of that two Individuals.

### Crossover

- **Parameters**
  - `crossover_strategy`: An instance of `CrossoverStrategy`.

- **Attributes**
  - `crossover_strategy`: An instance of `CrossoverStrategy`.

- **Methods**
  - `crossover(parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]` : Performs Crossover of given two Individuals with given `CrossoverStrategy` and returns tuple of that two Individuals.

### Mutation

- **Parameters**
  - `mutation_strategy`: An instance of `MutationStrategy`.

- **Attributes**
  - `mutation_strategy`: An instance of `MutationStrategy`.

- **Methods**
  - `mutate(individual: Individual)` : Mutates given Individuals with given `MutationStrategy`.
  - `set_mutation_rate(mutation_rate: float)` : sets Mutation rate.

## Strategies 

Each strategy class defines a specific operation in the genetic algorithm. Subclass these for custom behavior.

### SelectionStrategy
Defines the method for selecting parents from the population.

- **Methods**
  - `select_parents(population:Population) -> tuple[Individual, Individual]`: Abstract method; overridden in subclasses to select two parents and returns tuple of that two parents(Individuals).

### CrossoverStrategy
Handles recombination of parent genomes to produce offspring.

- **Methods**
  - `crossover(parent1:Individual, parent2:Individual) -> tuple[Individual, Individual]`: Abstract method; overridden in subclasses to define specific crossover behavior and returns tuple of that two Individuals.

### MutationStrategy
Defines how individual genomes mutate to introduce genetic variation.

- **Methods**
  - `mutate(individual:Individual) -> Individual`: Abstract method; overridden in subclasses to define mutation behavior and returns mutated Individual.

### FitnessStrategy
Evaluates the fitness of an individual based on its genome.

- **Methods**
  - `evaluate(genome:list) -> float`: Abstract method; overridden in subclasses to calculate fitness and returns float.

### DNAStrategy
A higher-level strategy class that combines the selection, crossover, mutation, and fitness strategies to dictate genetic algorithm behavior.

- **Parameters**
  - `genes`: A list of possible genes for creating genomes.
  - `target`: An optional target genome used for fitness comparisons, default value is `None`.
  - `duplicate_genomes`: Boolean indicating if duplicate genes are allowed in genomes, default value is `True`.
  - `selection_strategy`: An instance of `SelectionStrategy`, default value is `RouletteWheelSelection()`.
  - `crossover_strategy`: An instance of `CrossoverStrategy`, default value is `HalfCrossover()`.
  - `mutation_strategy`: An instance of `MutationStrategy`, default value is `ElementMutation()`.
  - `fitness_strategy`: An instance of `FitnessStrategy`, default value is `MaximizeOnesFitness()`.
 
- **Attributes**
  - `genes`: A list of possible genes for creating genomes.
  - `target`: An optional target genome used for fitness comparisons.
  - `duplicate_genomes`: Boolean indicating if duplicate genes are allowed in genomes.
  - `selection_strategy`: An instance of `SelectionStrategy`.
  - `crossover_strategy`: An instance of `CrossoverStrategy`.
  - `mutation_strategy`: An instance of `MutationStrategy`.
  - `fitness_strategy`: An instance of `FitnessStrategy`.
  
- **Methods**
  - `generate_genome(genome_size:int) -> list`: Generates a genome of the specified size, with or without duplicates.
  - `get_random_genes(genes_size:int) -> list`: Retrieves a random selection of genes.
  
- **Exceptions**
  - `__init_subclass__()`: Prevents subclasses from overriding the `__init__` method.

### Custom Strategies

To create a custom strategy, subclass any strategy base class and override necessary methods. Here’s an example of a custom selection strategy:

```python
from genetic_algorithm_py.strategy import SelectionStrategy

class CustomSelection(SelectionStrategy):
  def select(self, population):
    # Custom selection logic
    return tuple(population[:2])

# Use the custom strategy
dna_strategy = DNAStrategy(
  genes=[0, 1],
  selection_strategy=CustomSelection()
)
```

## Defaults

The `defaults` module provides ready-to-use implementations for common strategies.

### Fitness Functions

Defined in `defaults/fitness_function.py`:

- `CompairTargetFitness(target:list)` : Measures how closely the genome matches a target genome.
- `MaximizeOnesFitness()`: Maximizes the number of ones in the genome.
- `MinimizeDistanceFitness(target_value:float)`: Minimizes the distance between the genome and a target value.
- `WeightedSumFitness(weights:list)`: Calculates fitness as a weighted sum of genome bits.

### Selection Methods

Defined in `defaults/selection.py`:

- `RouletteWheelSelection()`: Selects parents based on fitness proportionate probability.
- `TournamentSelection(tournament_size:int)`: Selects parents using a tournament of random individuals.
- `RankSelection()`: Selects parents based on rank order.
- `StochasticUniversalSampling(num_select:int)`: Selects parents using evenly spaced fitness pointers.
- `ElitismSelection()`: Selects the top `n` individuals based on fitness.
- `TruncationSelection(percentage:float[0,1])`: Selects the top percentage of individuals.
- `BoltzmannSelection(temperature:float)`: Selects parents using Boltzmann probabilities.
- `SteadyStateSelection(num_replacements:int=2)`: Replaces the least fit individuals in the population.
- `RankBiasedSelection(bias_factor:float[0,1])`: Selects parents using rank-based weights with a bias factor.

### Crossover Methods

The following crossover strategies are available in `defaults/crossover.py`:

- `HalfCrossover()`: Splits genomes in half and swaps segments.
- `OnePointCrossover()`: Performs a one-point crossover by selecting a random point and swapping segments.
- `TwoPointCrossover()`: Performs a two-point crossover by selecting two points and swapping segments between them.
- `UniformCrossover()`: Randomly selects genes from each parent to create offspring.
- `BlendCrossover(alpha:float)`: Generates offspring genes within an extended range around each gene pair (controlled by `alpha`).
- `ArithmeticCrossover(alpha:float)`: Averages gene pairs based on a blending factor (`alpha`).
- `PMXCrossover()`: Partially Matched Crossover, suitable for permutation-based problems.


### Mutation Methods

Defined in `defaults/mutation.py`:

- `MultiElementMutation()`: Mutates multiple elements in the genome based on the mutation rate.
- `ElementMutation()`: Mutates a single element based on the mutation rate.
- `BitFlipMutation()`: Flips genome bits based on the mutation rate.
- `SwapMutation()`: Swaps two elements in the genome.
- `ScrambleMutation()`: Randomly scrambles a subset of the genome.
- `SegmentSwapMutation()`: Swaps two segments of the genome.
- `GaussianMutation(mutation_rate:float[0,1], sigma:float)`: Applies Gaussian mutation to genome values.
- `BoundaryMutation(mutation_rate:float[0,1], min_value:flaot, max_value:float)`: Mutates genome values within specified boundaries.
- `PolynomialMutation(mutation_rate:float[0,1], eta:float)`: Applies polynomial mutation to genome values.

---

## Examples

### Example 1: Using Default Strategies

```python
from genetic_algorithm_py import Individual, Population 
from genetic_algorithm_py.strategy import DNAStrategy

# Define genes and create a DNA strategy instance with default behaviors
genes = [0, 1]
dna_strategy = DNAStrategy(genes)

# Run the Genetic Algorithm
ga = GeneticAlgorithm(dna=dna, population_size=100,genome_size=len(target), mutation_rate=0.01)
ga.run(generations=50)
print("best Individual : ", ga.allBestIndividual.genome)
print("best Fitness : ", ga.allBestIndividual.fitness)
```

### Example 2: Custom Crossover Strategy

```python
from genetic_algorithm_py.strategy import CrossoverStrategy

# Custom crossover that swaps halves of genomes
class CustomCrossover(CrossoverStrategy):
    def crossover(self, parent1, parent2):
        mid = len(parent1.genome) // 2
        child1_genome = parent1.genome[:mid] + parent2.genome[mid:]
        child2_genome = parent2.genome[:mid] + parent1.genome[mid:]
        return Individual(child1_genome), Individual(child2_genome)

# Your Other code

# Use CustomCrossover in the DNAStrategy
dna_strategy.crossover_strategy = CustomCrossover()
```
## Contributing

We welcome contributions! Please see our contribution guidelines in `CONTRIBUTING.md`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.