import json
import matplotlib.pyplot as plt

print("Loading file...")
with open('available_books.txt') as file:
    data = file.read().strip()
    lines = data.split('\n')

print("Pulling years...")
years = []
for line in lines:
    d = json.loads(line)
    if 'year' in d:
        years.append(d['year'])

print(f"total: {len(years)}")
print(f"min: {min(years)}")
print(f"max: {max(years)}")
print(f"avg: {sum(years) / len(years)}")

values = sorted(list(set(years)))
print(values)
counts = {}
print("Doing counts...")
for x in values:
    counts[x] = years.count(x)
    # print(x, counts[x])

print("Plotting...")
plt.hist(years)
plt.yscale('log')
plt.show()
