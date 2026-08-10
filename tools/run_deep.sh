#!/bin/bash
# From the day-loop state, pick a practice and let the day run, using X to
# auto-advance dialogue instead of one A per box. Story events -- the ones with
# TEXT choice lists -- come out of the day loop, and those options are what the
# menu_hook redirect has to be judged on. The A/B prompt the prologue ends on is
# drawn from GRAPHICS, so it never touches the escape path.
set -u
cd "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"

ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr_v17.nds"
STATE="/root/v17_deep.dss"

STEPS="shot|a|spin:6|shot|a|spin:8|shot"
for _ in $(seq 1 70); do STEPS="$STEPS|x|spin:6|shot"; done

exec python3 -u tools/playtest.py --rom "$ROM" --load-state "$STATE" \
    --tag d17 --shots all --steps "$STEPS|save:/root/v17_day2.dss"
