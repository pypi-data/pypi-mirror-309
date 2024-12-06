#!/usr/bin/env python3

import itertools
import string
import os

def create_word_list(filename, caps, numerals, specials, num_words, min_word_length=8):
    # Define character set based on user preferences
    chars = string.ascii_lowercase  # default to lowercase
    if caps.lower() == "yes":
        chars += string.ascii_uppercase
    if numerals.lower() == "yes":
        chars += string.digits
    if specials.lower() == "yes":
        chars += string.punctuation

    # Calculate total number of possible combinations for given character set and length
    total_combinations = lambda length: len(chars) ** length

    # Determine minimum length required to reach or exceed the desired number of words
    word_length = min_word_length
    while total_combinations(word_length) < num_words:
        word_length += 1

    # Write words to the file, adjusting to the required word count
    with open(filename + ".txt", "w") as f:
        words_written = 0
        # Continue generating words with current word length until we reach num_words
        while words_written < num_words:
            # Generate combinations for the current word length
            word_combinations = itertools.product(chars, repeat=word_length)
            for word_tuple in word_combinations:
                if words_written >= num_words:
                    break
                word = ''.join(word_tuple)
                f.write(word + "\n")
                words_written += 1
                
    file_size = os.path.getsize(filename + ".txt")
    print(f"File '{filename}.txt' created with {num_words} words. File size: {file_size / (1024 * 1024):.2f} MB")
    

if __name__ == "__main__":
    # Get user inputs
    filename = input("Enter the filename (without .txt extension): ")
    caps = input("Should words contain uppercase letters? (yes or no): ")
    numerals = input("Should words contain numerals? (yes or no): ")
    specials = input("Should words contain special characters? (yes or no): ")
    num_words = int(input("How many words do you want to generate? "))
    print("wait untill this code generates and save into that file...")

    # Generate file with word combinations
    create_word_list(filename, caps, numerals, specials, num_words)
