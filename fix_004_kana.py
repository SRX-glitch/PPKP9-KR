filepath = r"c:\Users\jngji\Desktop\실험실\rom\DS\파워프로군 포켓9\ppkp9-kr\handoff\work\shard_004.tsv"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 7:
        row_id = parts[0].strip()
        if row_id == 'L4db1a1e820':
            parts[6] = '카운터엔 눈길이 안 갔어）\n'
    new_lines.append('\t'.join(parts))

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed L4db1a1e820 in shard_004.tsv")
