import json
import os
import random

# Load file with pointers to books
with open('available_books.json') as file:
    available = json.load(file)

with open('mapping_table.json') as file:
    table = json.load(file)

# Walk directory to check what is already available
already_downloaded = set()
for root, dirs, files in os.walk('./downloads/'):
    for file in files:
        if file.endswith('.txt'):
            ident = root.split('/')[-1]
            already_downloaded.add(ident)


# Shuffle full list and start downloading
random.shuffle(available)
for i, d in enumerate(available):
    ident = d['identifier']

    # Skip old books
    if ident in already_downloaded:
        print(f"skipping already downloaded {ident}")
        continue

    # Get list of files from command response: ia list ...
    response = os.popen(f"ia list {ident} --glob='*.txt'").read().strip()
    files = [f for f in response.split('\n') if 'meta.txt' not in f]

    # Run download command
    for file in files:
        command = f"ia download {ident} --glob='{file}' --destdir=downloads/"
        response = os.system(command)
        print(f"{i} response: {response} ({response == 0})")

    if response == 0:
        d['files'] = files
        table[ident] = d
    else:
        continue

# save the table dict
with open("mapping_table.json", "w") as file:
    json.dump(table, file)
    print("Dumped table to json.")
