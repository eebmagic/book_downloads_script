import os
import json
from tqdm import tqdm

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

print("walking files...")
files = find_txt_files('./downloads/')
print('done')

print("reading file...")
with open('available_books.json') as file:
    lines = json.load(file)

print(f"building table...")
table = {}
for d in tqdm(lines):
    table[d['identifier']] = d

years = []
counts = {}
noyear = set()
nodata = set()
too_old = set()
print(f"walking dir...")
for path, ident, size in tqdm(find_txt_files('./downloads/')):
    if ident in table:
        d = table[ident]
        if 'year' in d:
            y = table[ident]['year']

            # if year before 1850 remove dir
            if y < 1850:
                too_old.add(ident)
        else:
            noyear.add(ident)
    else:
        nodata.add(ident)


print(f"Total too old: {len(too_old)} / {len(files)} ({len(too_old)/len(files)*100:.2f}%)")
print(f"Total no data: {len(nodata)}")
print(f"Total no year: {len(noyear)}")

relevant = [f for f in files if f[1] in too_old]

import shutil
for rel in relevant:
    d = table[rel[1]]
    print(d['year'], rel[1], d['title'])
    path = '/'.join(rel[0].split('/')[:-1])
    print(path)

    # use os library to remove directory
    # shutil.rmtree(path)
    # print('removed')