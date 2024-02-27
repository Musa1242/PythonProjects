"""
    File: writer_bot_ht.py
    Author: Musa Unal
    Course: CSC 120
    Assignment: PA-long-11
    Purpose: Generates random text based on the
        Markov chain analysis of a given source text.
        It uses Hastable class to create the chain, 
        instead of Python build in dictionary.
    
"""


import random
import sys

# Constants
SEED = 8
NONWORD = '@'
random.seed(SEED)

class Hashtable:
    """
    This class implements a simple hashtable for storing
    key-value pairs. It uses linear probing for collision 
    resolution.

    The constructor initializes an empty hashtable
    of a given size.
    """
    def __init__(self, size):
        """
        Initialize the hashtable.

        Parameters:
        size (int): The initial size of the hashtable.
        """
        self._pairs = [None] * size
        self._size = size

    def _hash(self, key):
        """
        Add a key-value pair to the hashtable.

        Parameters:
        key (str): The key to be added.
        value: The value associated with the key.
        """
        p = 0
        for c in key:
            p = 31 * p + ord(c)
        return p % self._size

    def put(self, key, value):
        """
        Add a key-value pair to the hashtable.

        Parameters:
        key (str): The key to be added.
        value: The value associated with the key.
        """
        index = self._hash(key)
        start_index = index
        while True:   # Initialize 
            if self._pairs[index] is None:
                self._pairs[index] = [key, [value]] 
                return
            elif self._pairs[index][0] == key:  # Add to the existing list
                if value not in self._pairs[index][1]:
                    self._pairs[index][1] += [value] 
         
                return

            index -= 1  # Decrement the index for linear probing
            if index < 0:
                index = self._size - 1
            if index == start_index:  # Hashtable is full
                break


    def get(self, key):
        """
        Retrieve the value associated with a given key.

        Parameters:
        key (str): The key whose value is to be retrieved.

        Returns:
        The value associated with the key,
        or None if the key is not found.
        """
        index = self._hash(key)
        for _ in range(self._size):
            if self._pairs[index] is None:
                return None
            if self._pairs[index][0] == key:
                return self._pairs[index][1]
            index = (index - 1) % self._size
        return None

    def __contains__(self, key):
        """
        Check if a key is in the hashtable.

        Parameters:
        key (str): The key to be checked.

        Returns:
        True if the key is in the hashtable, False otherwise.
        """
        return self.get(key) is not None

    def __str__(self):
        return str(
            [pair for pair in self._pairs if pair is not None])
        
    
def read_file(file_name):
    """
    Reads the content of a file and returns a list of words,
    including punctuation.
    It opens a file and processes its content line by line. 
    Each word is separated based on whitespace. Punctuation
    is treated as part of the word.

    Parameters:
    file_name: A string representing the name of the
    file to be read.

    Returns:
    A list of strings, where each string is a word or
    punctuation from the file.
    """
    file = open(file_name, 'r')
    text = []
    for line in file:
        words = line.split()
        for i, word in enumerate(words):
            if i < len(words) - 1 and \
                words[i+1] in [',', '.', '!', '?', ';', ':']:
                text.append(word + words[i+1])
                words[i+1] = ""
            elif word not in [',', '.', '!', '?', ';', ':']:
                text.append(word)
    file.close()
    return text

def build_markov_chain(text, prefix_size, hash_table_size):
    """
    Build a Markov chain from a list of words.

    Parameters:
    text (list of str): The list of words from which to
        build the chain.
    prefix_size (int): The number of words in the prefix.
    hash_table_size (int): The size of the hashtable to 
        be used.

    Returns:
    A Hashtable object representing the Markov chain.
    """
    markov_chain = Hashtable(hash_table_size)
    prefix = (NONWORD,) * prefix_size
    for word in text:
        key = ' '.join(prefix).strip()
        if key in markov_chain:
            markov_chain.get(key).append(word)
        else:
            markov_chain.put(key, word)
        # print(f"Adding suffix '{word}' to prefix '{key}'")  
        # print(f"Current state of Hashtable: {markov_chain}")
        prefix = prefix[1:] + (word,)
    return markov_chain

def generate_text(chain, prefix_size, word_count):
    """
    Generate text using a Markov chain.

    Parameters:
    chain (Hashtable): The Markov chain to be 
        used for text generation.
    prefix_size (int): The number of words in the prefix.
    word_count (int): The number of words to generate.

    Returns:
    A string of generated text.
    """
    prefix = (NONWORD,) * prefix_size
    generated_words = []
    for _ in range(word_count):
        key = ' '.join(prefix).strip()
        suffixes = chain.get(key)
        if suffixes is None:
            break
        word = suffixes[random.randint(
            0, len(suffixes) - 1)] if len(suffixes) > 1 else suffixes[0]
        generated_words.append(word)
        new_prefix_words = (key + ' ' + word).split()[-prefix_size:]
        prefix = tuple(new_prefix_words)
    text_lines = [' '.join(generated_words[i:i+10]) \
        for i in range(0, len(generated_words), 10)]
    return '\n'.join(text_lines)


def print_text(text):
    """
    Print the generated text in a formatted way.

    Parameters:
    text (str): The text to be printed.
    """
    words = text.split()
    for i in range(0, len(words), 10):
        print(' '.join(words[i:i+10]))

def main():
    sfile = input()
    hash_table_size = int(input())
    prefix_size = int(input())
    number_of_words = int(input())

    if prefix_size < 1:  # error handling
        print(
            "ERROR: specified prefix size is less than one")
        sys.exit(0)

    if number_of_words < 1:
        print(
            "ERROR: specified size of the generated text is less than one")
        sys.exit(0)

    text = read_file(sfile)
    markov_chain = build_markov_chain(
        text, prefix_size, hash_table_size)
    generated_text = generate_text(
        markov_chain, prefix_size, number_of_words)
    print_text(generated_text)

if __name__ == "__main__":
    main()
