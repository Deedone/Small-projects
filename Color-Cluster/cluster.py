from PIL import Image, ImageDraw
from random import randint
from math import sqrt
class Cluster:

    def __init__(self):
        self.pos = [randint(0,255) for _ in range(3)]
        self.points = []
        self.prevpos = [-1,-1,-1]
        self.size = 0
        self.final = [0,0,0]
        self.fdist = 999999999999

    def dist(self,point):
        return sum( ((self.pos[i] - point[i])**2 for i in range(3)) )

    def append(self,p):
        self.points.append(p)
        self.size = len(self.points)
        
    def is_stable(self):
        return self.pos == self.prevpos

    def repos(self):
        self.prevpos = self.pos.copy()
        try:
            self.pos = [sum((self.points[i][j] for i in range(self.size)))/self.size for j in range(3)]
        except ZeroDivisionError:
            pass
        self.points = []
        self.size = 0
    def apply(self,p):
        d = self.dist(p)
        if d < self.fdist:
            self.final = p
            self.fdist = d

SIZE = 400
K = 7
clusters = []
pixels = []

def distr(p):
    pos = mindist = 9999999999
    for i,c in enumerate(clusters):
        d = c.dist(p)
        #if p != (0,0,0):
            #print(i,d,p,c.pos)
        if d < mindist:
            mindist = d
            pos = i
    #print(pos,mindist,"adasd")
    clusters[pos].append(p)

def do(s):
    global clusters
    clusters = [Cluster() for _ in range(K)]

    img = Image.open(s).resize((SIZE,SIZE)).convert("RGB")
    #img.show()
    pix = img.load()
    points = []
    for i in range(SIZE):
        for j in range(SIZE):
            points.append(pix[i,j])
    i = 0
    while (not all([c.is_stable() for c in clusters])) and i<10:
        print(i)
        i+=1
        for p in points:
            distr(p)
        for c in clusters:
            c.repos()
        for c in clusters:
            print([round(x) for x in c.pos])

    for c in clusters:
        for p in points:
            c.apply(p)
        
    img = Image.open(s)
    w = img.size[0] 
    h = img.size[1]
    new = Image.new("RGB",(w+200,h),(255,255,255))
    new.paste(img,(0,0))
    draw = ImageDraw.Draw(new)
    bh = round(h/K)
    clusters.sort(key=lambda c: sum(c.final)/3)
    for i,c in enumerate(clusters):
        sw = w+10
        ew = w+190
        sh = (bh*i)+5
        eh = (bh*(i+1))-5
        print((sw,sh),(ew,eh))
        draw.rectangle(((sw,sh),(ew,eh)),c.final)
    new.show()
        
do("test.png")




















            
    
