# Determines the reading grade level of a text using the Coleman-Liau index - Problem set 6 (4/5)

import re

def count_letters(text):
    # Count and return the number of letters in text
    return len([char for char in text if char.isalpha()])

def count_words(text):
    # Count and return the number of words in text
    return len(text.split())

def count_sentences(text):
    # Count and return the number of sentences in text
    # Sentences are separated by '.', '!', or '?'
    return len(re.findall(r'[.!?]', text))

def main():
    # Prompt the user for some text
    text = input("Text: ")

    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Compute the Coleman-Liau index
    L = (100.0 * letters) / words
    S = (100.0 * sentences) / words
    grade = round(0.0588 * L - 0.296 * S - 15.8)

    # Print the grade level
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")

if __name__ == "__main__":
    main()
