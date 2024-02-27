"""
    File: battleship.py
    Author: Musa Unal
    Purpose: This program simulates a game of Battleship,
    including ship placement and guessing mechanics.
    Course: CSC 120
"""
import sys

class GridPos:
    """
    Represents a single position on the Battleship game board.

    Each position may contain a part of a ship and can be guessed
    by the player. The class tracks whether a ship is present at 
    this position and if it has been guessed already.

    Attributes:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
        ship (Ship): The ship located at this position, if any.
        guessed (bool): True if this position has been guessed 
            already, False otherwise.
    """
    def __init__(self, x, y):
        """
        Initializes a new GridPos object with the specified coordinates.

        Initializes the ship to None and guessed to False by default.

        Parameters:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.
            ship (Ship): The ship located at this position, 
            if any.
            guessed (bool): True if this position has been guessed
            already, False otherwise.
        """
        self.x = x
        self.y = y
        self.ship = None
        self.guessed = False
    
    def __str__(self):
        return '.' if self.ship is None else self.ship.abbreviation

class Ship:
    """
    Represents a ship in the Battleship game.

    The ship is characterized by its type (e.g., battleship, submarine),
    its size, and its position on the board.The class also tracks the hits
    received by the ship.

    Attributes:
        SHIP_SIZES (dict): A class-level dictionary mapping 
            ship abbreviations to their sizes.
    """
    SHIP_SIZES = {
        'A': 5,  # Aircraft carrier
        'B': 4,  # Battleship
        'S': 3,  # Submarine
        'D': 3,  # Destroyer
        'P': 2   # Patrol boat
    }

    def __init__(self, abbreviation, x1, y1, x2, y2):
        """
        Initializes a new Ship object with given specifications.

        Parameters:
            abbreviation (str): The type of the ship 
                (e.g., 'A' for Aircraft carrier).
            x1, y1 (int): The starting coordinates of the ship.
            x2, y2 (int): The ending coordinates of the ship.

        The method checks if the ship type is valid, 
        calculates its positions, and initializes its hit status.
        """
        if abbreviation not in self.SHIP_SIZES:
            print("ERROR: fleet composition incorrect")
            sys.exit(0)
        self.abbreviation = abbreviation
        self.size = self.SHIP_SIZES[abbreviation]
        self.positions = self.calculate_positions(x1, y1, x2, y2)
        self.hits = 0
        self.hit_positions = []

    def calculate_positions(self, x1, y1, x2, y2):
        """
        Calculate the positions occupied by the ship on the board.

        The method checks whether the ship is placed horizontally
        or vertically and whether it fits within the board bounds.

        Parameters:
            x1, y1 (int): The starting coordinates of the ship.
            x2, y2 (int): The ending coordinates of the ship.

        Returns:
            list: A list of tuples representing the coordinates
            occupied by the ship.
        """
        if not (x1 == x2 or y1 == y2):
            print("ERROR: ship not horizontal or vertical: {} {} {} {} {}"\
                .format(self.abbreviation, x1, y1, x2, y2))
            sys.exit(0)
        
        positions = []
        if x1 == x2:  # Vertical placement
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if not (0 <= x1 <= 9 and 0 <= y <= 9):
                    print("ERROR: ship out-of-bounds:  {} {} {} {} {}".format(
                        self.abbreviation, x1, y1, x2, y2))
                    sys.exit(0)
                positions.append((x1, y))
        else:  # Horizontal placement
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if not (0 <= x <= 9 and 0 <= y1 <= 9):
                    print("ERROR: ship out-of-bounds:  {} {} {} {} {}".format(
                        self.abbreviation, x1, y1, x2, y2))
                    sys.exit(0)
                positions.append((x, y1))
        if len(positions) != self.size:
            print("ERROR: incorrect ship size:  {} {} {} {} {}".format(
                self.abbreviation, x1, y1, x2, y2))
            sys.exit(0)
        return positions

    def __str__(self):
        return "Ship {} of size {} at positions {}".format(
            self.abbreviation, self.size, self.positions)


class Board:
    """
    Represents the game board for Battleship.

    This class manages the grid of positions, the placement of ships,
    and the processing of guesses.

    Attributes:
        grid (list): A 2D list representing the game board grid.
        ships (dict): A dictionary mapping ship abbreviations to
            Ship objects.
        ship_types (dict): A dictionary tracking the count of
            each type of ship.
    """
    def __init__(self):
        """
        Initializes a new Board object.

        Sets up the game grid, initializes the ships dictionary,
        and sets the initial count of ship types.
        """
        self.grid = []
        for y in range(10):
            row = []
            for x in range(10):
                row.append(GridPos(x, y))
            self.grid.append(row)
        self.ships = {}
        self.ship_types = {'A': 0, 'B': 0, 'S': 0, 'D': 0, 'P': 0}

    def place_one_ship(self, ship_info):
        """
        Places a single ship on the board based on the provided
        information.

        Validates ship type, position, and orientation, and
        checks for overlapping or out-of-bounds placements.

        Parameters:
            ship_info (str): A string containing the ship's 
                abbreviation and its start and end coordinates.
        """
        parts = ship_info.split()
        abbreviation = parts[0]
        x1, y1, x2, y2 = map(int, parts[1:])
        # Check if the ship type is valid and not duplicated
        if abbreviation not in self.ship_types \
            or self.ship_types[abbreviation] >= 1:
            print("ERROR: fleet composition incorrect")
            sys.exit(0)
        else:
            self.ship_types[abbreviation] += 1
            
        # Check if the placement is either horizontal or vertical
        if not (x1 == x2 or y1 == y2):
            print("ERROR: ship not horizontal or vertical: {}".format(
                ship_info))
            sys.exit()
        ship = Ship(abbreviation, x1, y1, x2, y2)
        # Check for legal placement
        if any(x < 0 or x > 9 or y < 0 or y > 9 for x, y in ship.positions):
            print("ERROR: ship out of bounds: {}".format(ship_info))
            sys.exit()
        if len(ship.positions) != ship.size:
            print("ERROR: incorrect ship size: {}".format(ship_info))
            sys.exit()  
        
        for x, y in ship.positions:
            if self.grid[y][x].ship is not None:
                print("ERROR: overlapping ship: {}".format(ship_info))
                sys.exit() 

        self.ships[abbreviation] = ship
        for x, y in ship.positions:
            self.grid[y][x].ship = ship

    def process_guess(self, x, y):
        """
        Processes a player's guess on the board.

        Checks the validity of the guess and updates the game state
        accordingly.

        Parameters:
            x (int): The x-coordinate of the guessed position.
            y (int): The y-coordinate of the guessed position.
        """
        if x < 0 or x > 9 or y < 0 or y > 9:
            print("illegal guess")
            return
        
        grid_pos = self.grid[y][x]
        if grid_pos.guessed:
            if grid_pos.ship is not None \
                and (x, y) in grid_pos.ship.hit_positions:
                print("hit (again)")
            else:
                print("miss (again)")
            return
        
        grid_pos.guessed = True
        if grid_pos.ship is None:
            print("miss")
        else:
            ship = grid_pos.ship
            ship.hits += 1
            ship.hit_positions.append((x, y))
            if ship.hits == ship.size:
                print(
                    "{} sunk".format(ship.abbreviation))
                if all(s.hits == s.size for s in self.ships.values()):
                    print("all ships sunk: game over")
                    sys.exit()  # End the game
            else:
                print("hit")


def main():
    # Read in the name of the placement file
    placement_filename = input()
    file = open(placement_filename, 'r')
    placement_content = file.readlines()
    file.close()

    # Initialize the board
    board = Board()

    # Check if the placement file content is empty
    if not placement_content:
        print("ERROR: placement file is empty")
        sys.exit(0)

    # Process placements
    for line in placement_content:
        line = line.strip()
        if line:
            board.place_one_ship(line)

    # Check if the fleet composition is correct
    if sum(board.ship_types.values()) != 5:
        print("ERROR: fleet composition incorrect")
        sys.exit(0)

    # Read in the name of the guess file
    guess_filename = input()
    file = open(guess_filename, 'r')
    guess_content = file.readlines()
    file.close()

    # Check if the guess file content is empty
    if not guess_content:
        print("ERROR: guess file is empty")
        sys.exit(0)

    # Process guesses
    for line in guess_content:
        guess = line.strip().split()
        if guess:
            x, y = map(int, guess)
            board.process_guess(x, y)

            
if __name__ == '__main__':
    main()

