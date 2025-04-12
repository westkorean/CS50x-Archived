import csv
import sys


def main():

    # Check for correct command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py <database.csv> <sequence.txt>")
        sys.exit(1)

    # Read database file into a list of dictionaries
    database = []
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if key != "name":
                    row[key] = int(row[key])  # Convert STR counts to integers
            database.append(row)

    # Read DNA sequence file into a string
    with open(sys.argv[2]) as file:
        dna_sequence = file.read().strip()

    # Get the STRs from the database header (excluding the name column)
    str_sequences = list(database[0].keys())[1:]

    # Compute longest match of each STR in the DNA sequence
    str_counts = {str_seq: longest_match(dna_sequence, str_seq) for str_seq in str_sequences}

    # Check database for matching profiles
    for person in database:
        if all(person[str_seq] == str_counts[str_seq] for str_seq in str_sequences):
            print(person["name"])
            return

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
