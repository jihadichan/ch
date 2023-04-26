import csv
import re
import json

"""
This extracts the old mnemonics from the Anki Uberkanji export file
"""

csv_file_path = '/home/cc/Downloads/UberKanji.txt'

# Read the CSV file
with open(csv_file_path, 'r') as file:
    csv_data = file.read()

# Read the CSV content
csv_reader = csv.reader(csv_data.splitlines(), delimiter='\t')

# Initialize the dictionary to store the results
result_dict = {}

# Iterate over each row in the CSV file
for row in csv_reader:
    # Check if the row has at least four columns
    if len(row) >= 4:
        # Replace the newlines in the HTML content with actual newlines
        row[3] = row[3].replace('<br>', '\n')

        # Cleanup row[3] before assessment
        row[3] = row[3].strip()
        row[3] = row[3].replace('&nbsp;', ' ')
        row[3] = row[3].replace('!done', '')

        # Check if the line starts with a kanji followed by a space and a hyphen
        match = re.search(r'([\u4e00-\u9faf] -.*?)\n', row[3])

        if match:
            # Extract the mnemonic line from the match
            mnemonic_line = match.group(1)
            mnemonic_line = mnemonic_line.strip()
            # Add the key from column 0 and the value (mnemonic_line) to the dictionary
            result_dict[row[0]] = re.sub(r'([\u4e00-\u9faf] -.*?)', "", mnemonic_line).strip()
        elif row[3].count('\n') == 0 and row[3] != '':
            result_dict[row[0]] = row[3]

# Save the results to a JSON file
with open('old_mnemonics.json', 'w') as json_file:
    json.dump(result_dict, json_file, ensure_ascii=False, indent=2)

print("Data saved to old_mnemonics.json")
