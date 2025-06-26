class Ball:
    def __init__(self, radius, pos, col) :
        self.radius = radius
        self.pos = pos
        self.col = col
    
    def render(self):
        print("   ## \n"+
              "  ####\n" +
              "   ##")

class Square:
    def __init__(self, len, pos, col) :
        self.len = len
        self.pos = pos
        self.col = col

def cir_eq(a: Ball, b: Ball):
    return (a.radius == b.radius and 
            a.pos == b.pos and
            a.col == b.col)

a = Square(4, [1, 2], 'red')
b = Ball(5, [1, 2], 'red')

print(b.pos)
print(b)
#print(cir_eq(a, b))
b.render()