import os

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
counts = {}
sizes = {}
totalsize = 0
for path, ident, size in find_txt_files('./downloads/'):
    fchar = ident[0].lower()
    counts[fchar] = counts.get(fchar, 0) + 1
    sizes[fchar] = sizes.get(fchar, 0) + size
    totalsize += size
print("DONE")

for k in sorted(list(counts.keys())):
    # print(k, counts.get(k), sizes.get(k))
    print(f"{k} {counts[k]:>5} {(round(sizes[k]/totalsize, 3)):>10}")

total = sum(counts.values())
nona = total - counts.get('a')

print(f"Total: {total}")
print(f"Non-A: {nona}")
