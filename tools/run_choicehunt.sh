#!/bin/bash
# Cold-boot verification: creation (the confirm sheets need TOUCH, not A), then
# @skiprun to get deep fast. Parks two states for breakpoint work.
set -u
cd "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr_v26.nds"
STEPS="@creation|shot"
for _ in $(seq 1 3); do
  STEPS="$STEPS|touch:75,166|spin:5|touch:75,152|spin:5|a|spin:5|shot"
done
STEPS="$STEPS|start|spin:10|start|spin:20|shot|save:/root/v26_post_intro.dss"
STEPS="$STEPS|@skiprun|save:/root/v26_deep.dss"
exec python3 -u tools/playtest.py --rom "$ROM" --tag v26 --shots all --steps "$STEPS"
