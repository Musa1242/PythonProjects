"""
File: fake_news_ms.py
    Author: Musa Unal
    Purpose: It reads csv file and gets all lines, processes 
            it according to repeated words and n number.  
             It sorts the Word objects using the merge sort 
             algorithm implemented in the merge_sort and merge 
             functions. Then, it returns filename, n number, and
            repeated words in the file.
    Course: CSC120
    Assignment: PA-long-08-extra
"""


import csv
import string

class Word:
    def __init__(self, word):
        self._word = word
        self._count = 1

    def word(self):
        return self._word
    
    def count(self):
        return self._count
    
    def incr(self):
        self._count += 1

    def __lt__(self, other):
        return self._word < other._word
    
    def __str__(self):
        return "{} : {:d}".format(self._word, self._count)
    
def merge_sort(words_list):
    if len(words_list) <= 1:
        return words_list
    mid = len(words_list) // 2
    left = words_list[:mid]
    right = words_list[mid:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    
    return merge(left, right)

def merge(left, right):
    result = []
    merge_lists(left, right, result)
    return result

def merge_lists(left, right, result, left_index=0, right_index=0):
    if left_index == len(left):
        result.extend(right[right_index:])
        return
    if right_index == len(right):
        result.extend(left[left_index:])
        return
    if (left[left_index].count() > right[right_index].count() or
       (left[left_index].count() == right[right_index].count() and
        left[left_index] < right[right_index])):
        result.append(left[left_index])
        merge_lists(left, right, result, left_index + 1, right_index)
    else:
        result.append(right[right_index])
        merge_lists(left, right, result, left_index, right_index + 1)

def read_and_process_file(file_name, words_list):
    file = open(file_name, mode='r')
    csvreader = csv.reader(file)

    def read_lines(csvreader, words_list):
        line = next(csvreader, None)
        if line is None:
            return
        if not line[0].startswith("#"):
            title = line[4]
            clean_and_update_words(title, words_list)
        read_lines(csvreader, words_list)

    read_lines(csvreader, words_list)
    file.close()

def process_title(title, index, result):
    if index == len(title):
        return result
    char = title[index]
    if char in string.punctuation:
        result += " "
    else:
        result += char
    return process_title(title, index + 1, result)

def clean_and_update_words(title, words_list):
    cleaned_title = process_title(title, 0, "")
    words = cleaned_title.split()
    update_words(words, 0, words_list)

def update_words(words, index, words_list):
    if index == len(words):
        return
    word = words[index].lower()
    if len(word) > 2:
        update_count(word, words_list)
    update_words(words, index + 1, words_list)

def update_count(word, words_list):
    index = find_word_index(words_list, 0, word)
    if index != -1:
        words_list[index].incr()
    else:
        words_list.append(Word(word))

def find_word_index(words_list, index, word):
    if index == len(words_list):
        return -1
    if words_list[index].word() == word:
        return index
    return find_word_index(words_list, index + 1, word)

def print_upto_count(words_list, n, count, filename, index=0):
    if index == 0:
        print("File:", "N:")
    if index == len(words_list) or words_list[index].count() < count:
        return
    print(words_list[index])
    print_upto_count(words_list, n, count, filename, index + 1)

    




def main():
    filename = input().strip()
    words_list = []
    read_and_process_file(filename, words_list)

    n = int(input())
    words_list = merge_sort(words_list)
    
    if n <= len(words_list):
        count = words_list[n].count()
        print_upto_count(words_list, n, count, filename)
    else:
        print("n is out of bounds")

        
        
if __name__ == "__main__":
    main()
