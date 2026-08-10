#!/bin/bash
# Get deep into a run from the parked A/B-choice state, using the skiprun scene
# (X auto-advance + periodic A so prompts do not stall it) and park a state at
# the end for breakpoint work.
set -u
cd "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"

ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr_v18.nds"
STATE="/root/v18_choice.dss"

exec python3 -u tools/playtest.py --rom "$ROM" --load-state "$STATE" \
    --tag s18 --shots all --steps "shot|@skiprun|save:/root/v18_deep.dss"
