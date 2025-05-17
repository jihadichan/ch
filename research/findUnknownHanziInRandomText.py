import csv
import sys
import unicodedata

"""
This script will find unknown hanzi in some random text.
- Export your known hanzi via Anki's Browse function (search for `(deck:UberHanzi OR deck:UberHanziLoop) -is:suspended`) into `SelectNotes.txt`
- Put some random text into `input.txt` (can be anything, only hanzi will be checked)
- See main() for file paths

"""


def is_hanzi(char):
    """Check if a character is a Hanzi character."""
    return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(char, '')


def read_known_hanzi(file_path):
    """Read known Hanzi from the SelectNotes.txt file and return a set of valid Hanzi characters."""
    known_hanzi = set()

    # Open the CSV file with tab delimiter
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')

        for row in reader:
            if len(row) < 2:
                continue  # Skip rows with less than 2 columns

            hanzi = row[1].strip()

            # Check if the character is a single Hanzi character
            if len(hanzi) != 1 or not is_hanzi(hanzi):
                sys.exit(f"Error: Invalid Hanzi in column 2: '{hanzi}'")

            known_hanzi.add(hanzi)

    return known_hanzi


def process_input_file(file_path, known_hanzi):
    """Read input.txt file, and find unknown Hanzi characters."""
    unknown_hanzi = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            char = file.read(1)
            if not char:  # End of file
                break

            if is_hanzi(char) and char not in known_hanzi:
                unknown_hanzi.add(char)

    return unknown_hanzi


def main():
    # File paths
    select_notes_file = '/home/cc/Desktop/_anki/SelectedNotes.txt'
    input_file = '/home/cc/Desktop/_anki/input.txt'

    # Step 1: Read known Hanzi from SelectNotes.txt
    known_hanzi = read_known_hanzi(select_notes_file)

    # Step 2: Process input.txt and find unknown Hanzi
    unknown_hanzi = process_input_file(input_file, known_hanzi)

    # Step 3: Output unknown Hanzi
    if unknown_hanzi:
        print("Unknown Hanzi characters:")
        for hanzi in sorted(unknown_hanzi):
            print(hanzi)
    else:
        print("No unknown Hanzi found.")


if __name__ == '__main__':
    main()
