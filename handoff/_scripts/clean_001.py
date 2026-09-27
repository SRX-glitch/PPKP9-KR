import re

filepath = r"c:\Users\jngji\Desktop\실험실\rom\DS\파워프로군 포켓9\ppkp9-kr\handoff\work\shard_001.tsv"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 7:
        ko = parts[6].strip()
        if '->' in ko:
            ko = ko.split('->')[-1].strip()
        parts[6] = ko + '\n'
        new_lines.append('\t'.join(parts))
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Cleaned shard_001.tsv")
