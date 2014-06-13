mouse = file('/dev/input/mouse0')
while True:
    status, dx, dy = tuple(ord(c) for c in mouse.read(3))
 
    def to_signed(n):
        return n - ((0x80 & n) << 1)
        
    dx = to_signed(dx)
    dy = to_signed(dy)
    print "%#02x %d %d" % (status, dx, dy)