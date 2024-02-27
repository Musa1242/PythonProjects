"""
File: street.py
Author: Musa Unal
Purpose: To represent different street elements such as
    buildings, parks, and empty lots, and to visualize 
    them by printing the street at different height levels.
Course: CSC120
Assignment: PA-long-08 --redo
"""

class Building:
    """Represents a building on the street.

    A building is represented as a rectangle made of bricks.
    The size of the building and the brick pattern can be 
    specified.

    Attributes:
        width (int): The width of the building.
        height (int): The height of the building.
        brick (str): The brick pattern used to represent 
        the building.
    """

    def __init__(self, width, height, brick):
        """Initializes a Building object with specified width,
        height, and brick pattern.

        Parameters:
            width (int): The width of the building.
            height (int): The height of the building.
            brick (str): The brick pattern used to 
            represent the building.
        """
        self.width = width
        self.height = height
        self.brick = brick

    def at_height(self, height):
        """Returns a string representing the building at
        the specified height.

        If the height is within the building's height, it 
        returns a line of bricks.Otherwise, it returns a 
        line of spaces.

        Parameters:
            height (int): The height at which to represent 
            the building.

        Returns:
            str: A string representing the building at the 
            specified height.
        """
        if 0 <= height < self.height:
            return (self.brick * (
                self.width // len(self.brick) + 1))[:self.width]
        return ' ' * self.width


class Park:
    """Represents a park on the street.

    A park consists of trees and ground. The size of the park and 
    the foliage pattern can be specified.

    Attributes:
        width (int): The width of the park.
        foliage (str): The foliage pattern used to represent the 
        trees in the park.
    """

    def __init__(self, width, foliage):
        """Initializes a Park object with specified width and foliage pattern.
        Parameters:
            width (int): The width of the park.
            foliage (str): The foliage pattern used to 
                represent the trees in the park.
        """
        self.width = width
        self.foliage = foliage
        self.tree_height = 5
        self.ground_height = 0
        self.height = self.tree_height + self.ground_height
        
    def at_height(self, height):
        """Returns a string representing the park at the 
        specified height.

        If the height is less than the ground height,
        it returns a string of spaces to represent the ground.
        If the height is within the tree height range, 
        it returns a string representing the trees at that height.
        Otherwise, it returns a string representing the top border.

        Parameters:
            height (int): The height at which to represent the park.

        Returns:
            str: A string representing the park at the specified height.
        """
        if height < self.ground_height:
            # Ground
            return  ' ' * (self.width - 2) 
        elif height < self.tree_height + self.ground_height:
            # Tree
            tree_layer = height - self.ground_height
            return self.draw_tree(tree_layer)
        else:
            # Top border
            return ' ' + ' ' * (self.width - 2) + ' '

    def draw_tree(self, height):
        """Draw a section of the tree at the given height.

        Parameters:
            height (int): The height of the tree section to draw.

        Returns:
            str: A string representing a section of
                the tree at the specified height.
        """
        if height == 4:
            # Top of the foliage (1 foliage character)
            return self.centered_string(self.foliage)
        elif height == 3:
            # Middle of the foliage (3 foliage characters)
            return self.centered_string(self.foliage * 3)
        elif height == 2:
            # Base of the foliage (5 foliage characters)
            return self.centered_string(self.foliage * 5)
        elif height in [0, 1]:
            # Trunk (at heights 0 and 1)
            trunk_space = ' ' * ((self.width - 1) // 2)
            return trunk_space + '|' + trunk_space

    def centered_string(self, s):
        """
        Center a string within the park's width.

        Parameters:
            s (str): The string to be centered.

        Returns:
            str: The centered string within the park's width.
        """
        padding = (self.width - len(s)) // 2
        return ' ' * padding + s + ' ' * padding

class EmptyLot:
    """Represents an empty lot on the street.

    An empty lot can have trash. The size of the empty lot 
    and the trash pattern can 
    be specified.

    Attributes:
        width (int): The width of the empty lot.
        trash (str): The trash pattern used to represent the 
        trash in the empty lot.
    """

    def __init__(self, width, trash):
        """Initializes an EmptyLot object with specified width 
        and trash pattern.

        Parameters:
            width (int): The width of the empty lot.
            trash (str): The trash pattern used to represent the
            trash in the empty lot.
        """
        self.width = width
        self.trash = self.replace_underscores_with_spaces(trash)
        self.height = 1

    def replace_underscores_with_spaces(self, trash):
        """Recursively replaces underscores with spaces in the string.
        
        Parameters:
            trash (str): The trash pattern used to represent the
            trash in the empty lot.
        
        """
        if "_" not in trash:
            return trash
        else:
            index = trash.index("_")  # Find the index of the first underscore
            trash = trash[:index] + " " + trash[index + 1:]  # Replace the underscore
            return self.replace_underscores_with_spaces(trash)

    def at_height(self, height):
        """Returns a string representing the empty lot at the
        specified height.

        If the height is 0, it returns a line of trash. Otherwise,
        it returns a line of spaces.

        Parameters:
            height (int): The height at which to represent the empty
            lot.

        Returns:
            str: A string representing the empty lot at the specified
            height.
        """
        if not self.trash or height >= 1:
            return ' ' * self.width
        return (self.trash * (self.width // len(self.trash)) 
                + self.trash[:self.width % len(self.trash)])


def print_street_at_height(elements, height, total_width,
                           current_index=0, line=''):
    """Prints the street at the specified height.

    Parameters:
        elements (list): A list of street elements 
            (Buildings, Parks, and EmptyLots).
        height (int): The height at which to print the street.
        total_width (int): The total width of the street.
        current_index (int): The current index in the elements 
            list. Defaults to 0.
        line (str): The accumulated line string. Defaults to 
            an empty string.
    """
    if height < 0:
        print('+' + '-' * total_width + '+')
        return
    
    if current_index == len(elements):
        print('|' + line + '|')
        print_street_at_height(elements, height - 1, total_width)
        return
    
    
    line += elements[current_index].at_height(height)
    print_street_at_height(
        elements, height, total_width, current_index + 1, line)

def parse_street(street_input, elements=None):
    """Parses the street input string and converts it into
    a list of street elements.

    Parameters:
        street_input (str): A string representing the street
            with various elements.
        elements (list, optional): A list to store the parsed
            street elements.

    Returns:
        list: A list of street elements (Buildings, Parks,
        and EmptyLots).
    """
    if elements is None:
        elements = []

    items = street_input.split()
    if not items:
        return elements

    item = items[0]
    rest_of_street = ' '.join(items[1:])
    kind, specs = item.split(':', 1)

    if kind == 'b':
        width, height, brick = specs.split(',')
        elements.append(Building(int(width), int(height), brick))
    elif kind == 'p':
        width, foliage = specs.split(',')
        elements.append(Park(int(width), foliage))
    elif kind == 'e':
        width, trash = specs.split(',')
        elements.append(EmptyLot(int(width), trash))

    return parse_street(rest_of_street, elements)

def get_max_height(elements, current_max=1):
    if not elements:
        return current_max
    else:
        first, *rest = elements
        new_max = current_max if current_max > first.height else first.height
        return get_max_height(rest, new_max)

    
def sum_widths(elements, current_sum=0):
    """
    Recursively calculate the total width of elements in a list.

    :param elements: List of objects, each having a 'width' attribute
    :param current_sum: Integer, the current total width calculated
    :return: The total width of all elements
    """
    if not elements:
        return current_sum
    else:
        first, *rest = elements
        return sum_widths(rest, current_sum + first.width)


def main():
    street_input = input("Street: ")
    elements = parse_street(street_input)
    height = get_max_height(elements)
    total_width = sum_widths(elements)

    # Print the top border
    print('+' + '-' * total_width + '+')

    # Print the empty line above buildings
    print('|' + ' ' * total_width + '|')

    # Print the street at each height level
    print_street_at_height(elements, height - 1, total_width)


if __name__ == '__main__':
    main()




