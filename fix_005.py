filepath = r"c:\Users\jngji\Desktop\실험실\rom\DS\파워프로군 포켓9\ppkp9-kr\handoff\work\shard_005.tsv"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 7:
        row_id = parts[0].strip()
        if row_id == 'L5531c8f58d':
            parts[6] = '그렇게 말해 주는 사람만 있어도\n'
        elif row_id == 'L8c909860d6':
            parts[6] = '말하면서도 장래를 생각하고 있구나。\n'
    new_lines.append('\t'.join(parts))

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed shard_005.tsv")
