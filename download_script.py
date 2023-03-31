import json
import os

print("Loading file...")
with open('available_books.txt') as file:
    data = file.read().strip()
    lines = data.split('\n')


table = {}
for i, line in enumerate(lines):
    d = json.loads(line)
    ident = d['identifier']

    # Get list of files from command response: ia list ...
    # response = os.popen(f"ia list {ident} --glob='*.[jt][sx][ot]*'").read().strip()
    response = os.popen(f"ia list {ident} --glob='*.txt'").read().strip()
    files = response.split('\n')

    # Run download command
    command = f"ia download {ident} --glob='*.txt' --destdir=downloads/"
    response = os.system(command)
    print(f"{i} response: {response} ({response == 0})")

    if response == 0:
        d['files'] = files
        table[ident] = d
    else:
        continue

    if i > 3:
        break

# save the table dict
with open("mapping_table.json", "w") as file:
    json.dump(table, file)
    print("Dumped table to json.")

