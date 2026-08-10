#!/usr/bin/env python3
"""Scan dumped RAM/VRAM blobs (and ROM overlays) for a fixed-cell bitmap-font
region: a long run of glyph-sized cells with font-like ink density and low
structural variance. Reports best candidate offset+cell per file."""
import sys, os, glob, struct

def score_region(b, base, cell, ncells=256):
    """higher = more font-like over `ncells` cells starting at base"""
    if base+cell*ncells > len(b): ncells=(len(b)-base)//cell
    if ncells < 64: return -1, 0
    mid=0; blank=0; full=0
    for g in range(ncells):
        chunk=b[base+g*cell:base+(g+1)*cell]
        bits=sum(bin(x).count("1") for x in chunk)
        dens=bits/(cell*8)
        if dens==0: blank+=1
        elif dens>=0.75: full+=1
        elif 0.08<dens<0.55: mid+=1
    # font: mostly mid-density, few full/solid, some blanks ok
    return mid - full*2, ncells

def scan(path):
    b=open(path,"rb").read()
    best=None
    for cell in (24,32,18,16,72,128):  # 12x12(2Bpr),16x16,12x12(1.5B),8x16, 24x24, 32x...
        step=cell*16
        for base in range(0, max(1,len(b)-cell*256), step):
            s,n=score_region(b,base,cell)
            if best is None or s>best[0]:
                best=(s,base,cell,n)
    return best

targets=[]
sd="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
targets+=sorted(glob.glob(sd+"/*.bin"))
for t in targets:
    try:
        best=scan(t)
        print(f"{os.path.basename(t):20} best score={best[0]:6} @0x{best[1]:X} cell={best[2]}B ({best[3]} cells)")
    except Exception as ex:
        print(f"{os.path.basename(t)}: err {ex}")
