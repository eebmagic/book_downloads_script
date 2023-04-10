import os
import json
from tqdm import tqdm
import time


def find_txt_files(dir_path):
    txt_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                ident = file_path.split('/')[-2]
                txt_files.append((file_path, ident, file_size))
    return txt_files


print("reading file...")
with open('available_books.json') as file:
    lines = json.load(file)

print(f"building table...")
table = {}
for d in tqdm(lines):
    table[d['identifier']] = d

years = []
counts = {}
skiptotal = 0
currtime = time.time()
twodaytime = currtime - 172800 # Unix time 48 hours ago
newtotal = 0
print(f"wakling dir...")
for path, ident, size in tqdm(find_txt_files('./downloads/')):
    if ident in table:
        ctime = os.stat(path).st_ctime
        if ctime > twodaytime:
            newtotal += 1

        d = table[ident]
        if 'year' in d:
            y = table[ident]['year']
            years.append(y)
            counts[y] = counts.get(y, 0)+1
    else:
        skiptotal += 1

total = 0
for year in sorted(counts.keys()):
    total += counts[year]
    print(year, f"{str(counts[year]):<6}", '█' * int(50 * counts[year] / max(counts.values())))

print(f"\nTotal skipped: {skiptotal}")
print(f"Total books in last 48 hours: {newtotal}")
print(f"Total books: {total}")

import matplotlib.pyplot as plt
plt.hist(years, bins=50)
plt.show()
