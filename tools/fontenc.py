"""PPKP9 2bpp glyph encoder. Glyph = 12 wide x 8 tall.
Each source byte = 4 horizontal pixels, 2 bits each (LSB pair = leftmost).
per pixel: 0b00=off(0), 0b10=full ink(15), 0b01=faint(1).
Layout: row r (0..7), col c (0..11):
  c in 0..3  -> byte[2r],    pixel (c)
  c in 4..7  -> byte[2r+1],  pixel (c-4)
  c in 8..11 -> byte[16+2r], pixel (c-8)
"""
def encode_glyph(bitmap):
    # bitmap: list of 8 rows, each a list/str of 12 values (0=off,1=full,2=faint)
    src=bytearray(36)
    def setpx(byte_i, pix, val):
        # pix 0..3 within byte; val 0/1/2
        bits = {0:0b00,1:0b10,2:0b01}[val]
        src[byte_i] |= bits << (pix*2)
    for r in range(8):
        row=bitmap[r]
        for c in range(12):
            v=row[c]
            if v==0: continue
            if c<4:   setpx(2*r,   c,   v)
            elif c<8: setpx(2*r+1, c-4, v)
            else:     setpx(16+2*r,c-8, v)
    return bytes(src)

if __name__=="__main__":
    # test "F": top row + left col + middle row
    F=[[0]*12 for _ in range(8)]
    for c in range(12): F[0][c]=1        # top row
    for r in range(8): F[r][0]=1          # left column
    for c in range(8): F[3][c]=1          # middle bar
    b=encode_glyph(F)
    print(b.hex())
