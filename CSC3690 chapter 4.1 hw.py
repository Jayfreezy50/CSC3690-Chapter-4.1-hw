import math
from collections import Counter

attributes = ["Toothed", "Hair", "Breathes", "Legs"]

data = [
    ["Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Not Hair", "Breathes", "Not Legs", "Reptile"],
    ["Not Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Hair", "Breathes", "Legs", "Mammal"],
    ["Toothed", "Not Hair", "Not Breathes", "Not Legs", "Reptile"],
    ["Toothed", "Not Hair", "Breathes", "Not Legs", "Reptile"],
    ["Toothed", "Not Hair", "Breathes", "Legs", "Mammal"],
    ["Not Toothed", "Not Hair", "Breathes", "Legs", "Reptile"],
]


def entropy(rows):
    counts = Counter(r[-1] for r in rows)
    total = len(rows)
    return abs(-sum(c / total * math.log2(c / total) for c in counts.values()))


def split(rows, col):
    groups = {}
    for r in rows:
        groups.setdefault(r[col], []).append(r)
    return groups


def gain(rows, col):
    remainder = 0
    for value, group in split(rows, col).items():
        remainder += len(group) / len(rows) * entropy(group)
    return entropy(rows) - remainder


def build(rows, attrs, indent=0):
    space = "    " * indent
    classes = Counter(r[-1] for r in rows)
    print(f"{space}Node: {dict(classes)}  entropy = {entropy(rows):.4f}")

    if len(classes) == 1:
        label = rows[0][-1]
        print(f"{space}Pure -> leaf: {label}")
        return label

    if not attrs:
        label = classes.most_common(1)[0][0]
        print(f"{space}No attributes left -> leaf: {label}")
        return label

    gains = {}
    for a in attrs:
        gains[a] = gain(rows, attributes.index(a))
        print(f"{space}Gain({a}) = {gains[a]:.4f}")

    best = max(gains, key=gains.get)
    print(f"{space}Best attribute: {best}\n")

    tree = {best: {}}
    rest = [a for a in attrs if a != best]
    for value, group in split(rows, attributes.index(best)).items():
        print(f"{space}{best} = {value}")
        tree[best][value] = build(group, rest, indent + 1)
    return tree


def predict(tree, example):
    while isinstance(tree, dict):
        attr = list(tree.keys())[0]
        tree = tree[attr][example[attr]]
    return tree


tree = build(data, attributes)

print("\nFinal tree:")
print(tree)

new_example = {
    "Toothed": "Toothed",
    "Hair": "Hair",
    "Breathes": "Not Breathes",
    "Legs": "Legs",
}
print("\nNew example:", new_example)
print("Predicted species:", predict(tree, new_example))