# Identifies to whom a sequence of DNA belongs - Problem set 6 (5/5)

import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # If the correct number of arguments are provided, proceed with the program
    csv_filename = sys.argv[1]
    txt_filename = sys.argv[2]

    # Read database file into a variable
    with open(csv_filename, mode='r') as file:
        reader = csv.DictReader(file)
        database = list(reader)
    
    # Read DNA sequence file into a variable
    with open(txt_filename, 'r') as file:
        sequence = file.read().strip()

    # Find longest match of each STR in DNA sequence
    strs = list(database[0].keys())[1:] 

    # Create a dictionary to hold the longest match for each STR
    str_matches = {}

    # Compute the longest match for each STR in the DNA sequence
    for str in strs:
        str_matches[str] = longest_match(sequence, str)

    # Check database for matching profiles
    for person in database:
        # Assume a match until proven otherwise
        match = True
        for str in strs:
            # Compare the STR count in the database with the computed STR count
            if int(person[str]) != str_matches[str]:
                match = False
                break
        if match:
            print(person['name'])
            break
    else:
        print("No match")


    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
