import chess  # Python chess library to manage game states and moves
import random  # library for random selection of moves and strategies
#Done by:Ahmed Abdelgelil
class ChessAI:#    A chess AI that uses a GA to evolve strategies for playing chess.

    def _init_(self, population_size=100, generations=50):#        # Initialize the genetic algorithm parameters
        self.population_size = population_size  # Number of strategies in each generation
        self.generations = generations  # Number of generations to evolve
        self.population = self.initialize_population()  # Initial population of strategies (awel pop khales )

    def initialize_population(self):#Creates the initial population of strategies.
        #Each strategy consists of a random sequence of valid moves.
        return [self.random_strategy() for _ in range(self.population_size)]

    def random_strategy(self):#Generates a random sequence of valid moves as a strategy.(elhoma already 3andena men chess engine)
        board = chess.Board()  # Create a new chess board
        strategy = []  # List to store the random moves el Ai hay3mlha
        for _ in range(10):  # Generate a strategy with up to 10 moves per game
            if board.is_game_over():  # Stop if the game is over
                break
            move = random.choice(list(board.legal_moves))  # Choose a random legal move
            strategy.append(move)  # Add the move to the strategy
            board.push(move)  # Make the move on the board for the user opponent to see it
        return strategy

    def fitness(self, strategy):# Evaluates the fitness of a strategy based on the resulting board state.
        board = chess.Board()  # Create a new board
        for move in strategy:  # Apply each move in the strategy
            if move in board.legal_moves:  # Check if the move is legal
                board.push(move)  # Make the move,after the first one
            else:
                return -100  # Penalty for invalid strategy
        return self.evaluate_board(board)  # Evaluate the board after all moves

    def evaluate_board(self, board):#        Evaluates the board's material advantage.
        # Material values for each piece type
        values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        # Calculate the material score based on the pieces on the board for each one to able able to spectate later
        material_score = sum(values[piece.piece_type] for piece in board.piece_map().values())#map the values to each piece
        return material_score  # Return the material advantage

    def select(self):#        Selects the top 50% of the population based on fitness.
        sorted_population = sorted(self.population, key=self.fitness, reverse=True)  # Sort by fitness according to the values we have
        return sorted_population[:self.population_size // 2]  # Select the top half

    def crossover(self, parent1, parent2):# Combines two parent strategies to create a child strategy(bnkhtar parents with top fitness aka best moves)
        crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)  # Random split point done by the random library above
        child = parent1[:crossover_point] + parent2[crossover_point:]  # Combine parts of both parents
        return child

    def mutate(self, strategy):#Applies random mutation to a strategy with a small probability to make the best out of it
        board = chess.Board()  # Create a new board

        # Apply the existing moves in the strategy to the board
        for move in strategy:
            if move in board.legal_moves:
                board.push(move)
            else:
                break

        # 10% chance to mutate the strategy
        if random.random() < 0.1:
            mutation_index = random.randint(0, len(strategy) - 1)  # Choose a random mutation point

            # Undo all moves up to the mutation index
            while len(board.move_stack) > mutation_index:
                board.pop()

            # Choose a new random move at the mutation point
            mutation_move = random.choice(list(board.legal_moves))
            strategy[mutation_index] = mutation_move  # Apply the mutation
            board.push(mutation_move)  # Update the board with the new move

        return strategy  # Return the mutated strategy
#in the above part we keep mutating till we find the best output
    def run(self):#  Runs the genetic algorithm to evolve strategies over multiple generations.

        for generation in range(self.generations):
            selected = self.select()  # Select the best strategies
            next_generation = selected.copy()  # Start the next generation with selected strategies
            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)  # Pick two random parents
                child = self.crossover(parent1, parent2)  # Create a child strategy via crossover
                child = self.mutate(child)  # Apply mutation to the child
                next_generation.append(child)  # Add the child to the next generation
            self.population = next_generation  # Update the population
            print(f"Generation {generation + 1}: Best Fitness = {self.fitness(selected[0])}")  # Print the best fitness

    def getBestMove(self, gs, validMoves):#Returns the best move based on the evolved strategy.
        #(Currently selects a random valid move for simplicity.)
        board = chess.Board()  # Create a new chess board
        best_move = random.choice(validMoves)  # Choose a random valid move
        return best_move#we return the best move in order for the ai to implement and play the best move independtly according to the fitness and muattions calculation