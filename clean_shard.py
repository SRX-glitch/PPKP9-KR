import sys

filepath = sys.argv[1]

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 7:
        ko = parts[6].strip()
        if '->' in ko:
            ko = ko.split('->')[-1].strip()
        # Replace 장음 'ー' with '~' or Remove if problematic
        ko = ko.replace('ー', '～')
        parts[6] = ko + '\n'
        new_lines.append('\t'.join(parts))
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Cleaned {filepath}")
