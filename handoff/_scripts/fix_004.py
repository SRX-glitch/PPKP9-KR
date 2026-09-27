filepath = r"c:\Users\jngji\Desktop\실험실\rom\DS\파워프로군 포켓9\ppkp9-kr\handoff\work\shard_004.tsv"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 7:
        row_id = parts[0].strip()
        if row_id == 'L493c391601':
            parts[6] = '그러니 그때 내가 떠날 때、\n'
        elif row_id == 'L4db1a1e820':
            parts[6] = '카ウンター엔 눈길이 안 갔어）\n'.replace('ー', '～')
    new_lines.append('\t'.join(parts))

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Updated shard_004.tsv")
