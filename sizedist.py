import os
import matplotlib.pyplot as plt

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
results = find_txt_files('./downloads/')

sizes = [size for _, _, size in results]

minimum = min(sizes)
maximum = max(sizes)

for file, ident, size in results:
    if size == minimum:
        print(f"min: {file} {ident} {size}")
    if size == maximum:
        print(f"max: {file} {ident} {size}")

print(f"min: {min(sizes)}")
print(f"max: {max(sizes)}")

minsize = 20_000
filtered = [size for size in sizes if size > minsize]
print(f"# of docs under minsize ({minsize}): {len(sizes) - len(filtered)}")
print(f"# of docs over minsize ({minsize}): {len(filtered)}")

avgsize = sum(filtered) / len(filtered)
print(f"avgsize: {(avgsize/1024):.2f} KB")

plt.hist(filtered, bins=100)
plt.show()