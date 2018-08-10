import pprint
from PIL import Image, ImageDraw
from time import time
from math import sqrt
pp = pprint.PrettyPrinter(indent=2)
DEBUG = 2

def i_j_itterator(w,h):
    for i in range(w):
            for j in range(h):
                yield i,j

def norm(v,min1,max1,min2,max2):
    return round(min2+(max2-min2)*((v-min1)/(max1-min1)))

class Filter():
    def __call__(self,s):
        if DEBUG > 0:
            print("Blurer called with {} arg".format(s))
        self.image = Image.open(s)
        self.pix = self.image.load()
        self.width = self.image.size[0] 
        self.height = self.image.size[1]
        self.result = Image.new("RGB",(self.width,self.height))
        self.draw = ImageDraw.Draw(self.result)
        

    def chpos(self,x,y):
        if x<0 or y<0:
            return False
        if x>=self.width or y>=self.height:
            return False
        return True

    
class Blurer(Filter):

    def __init__(self,kernel_size=3):
        self.ksize = kernel_size
        self.kernel = [[1 for j in range(self.ksize)] for i in range(self.ksize)]
        self.ksum = self.origksum = sum([sum(i) for i in self.kernel])
        if DEBUG > 0:
            print("KERNEL HERE:")
            pp.pprint(self.kernel)
        self.kcenter = ((self.ksize-1)//2)
        if DEBUG > 1:
            print(self.kcenter)

    def __call__(self,s):
        super().__call__(s)
        start = time()
        self.process_img()
        print(time() - start)
        self.result.save('out.png')
        
    def apply_kernel(self,x,y):
        x-=self.kcenter
        y-=self.kcenter
        self.ksum = self.origksum
        sumr = sumg = sumb = 0
        for ki,i in enumerate(range(x,x+self.ksize)):
            for kj,j in enumerate(range(y,y+self.ksize)):
                if not self.chpos(i,j):
                    self.ksum-=1
                    continue
                sumr+=self.pix[i,j][0]*self.kernel[kj][ki]
                sumg+=self.pix[i,j][1]*self.kernel[kj][ki]
                sumb+=self.pix[i,j][2]*self.kernel[kj][ki]
        return round(sumr / self.ksum),round(sumg / self.ksum),round(sumb / self.ksum)
                
    def process_img(self):
        for i,j in i_j_itterator(self.width,self.height):
            r,g,b = self.apply_kernel(i,j)
            self.draw.point((i,j),(r,g,b))


class Sobel(Filter):
    
    def __init__(self):
        self.vkernel = [[1 ,2 ,1],
                        [0 ,0 ,0],
                        [-1,-2,-1]]
        self.hkernel = [[1,0,-1],
                        [2,0,-2],
                        [1,0,-1]]
        self.kcenter = 1
        self.ksize = 3

    def __call__(self,s):
        super().__call__(s)
        self.image = self.image.convert('L')
        self.pix = self.image.load()
        self.result = self.result.convert('L')
        self.draw = ImageDraw.Draw(self.result)
        self.vtemp = Image.new("L",(self.width,self.height))
        self.vdraw = ImageDraw.Draw(self.vtemp)
        self.htemp = Image.new("L",(self.width,self.height))
        self.hdraw = ImageDraw.Draw(self.htemp)
        self.vdata = [[0 for x in range(self.width)] for y in range(self.height)]
        self.hdata = [[0 for x in range(self.width)] for y in range(self.height)]
        self.tdata = [[0 for x in range(self.width)] for y in range(self.height)]
        start = time()
        self.process_img()
        print(time() - start)
        self.result.save('out.png')

    def apply_kernel(self,x,y,kernel):
        x-=self.kcenter
        y-=self.kcenter
        sum = 0
        for ki,i in enumerate(range(x,x+self.ksize)):
            for kj,j in enumerate(range(y,y+self.ksize)):
                if not self.chpos(i,j):
                    continue
                sum+=self.pix[i,j]*kernel[kj][ki]
        return round(sum)

    def process_img(self):
        self.vmin = self.hmin = 999999
        self.vmax = self.hmax = 0
        self.tmax = 0
        for x,y in i_j_itterator(self.width,self.height):
            vval = self.apply_kernel(x,y,self.vkernel)
            hval = self.apply_kernel(x,y,self.hkernel)
            if vval > self.vmax : self.vmax = vval
            if vval < self.vmin : self.vmin = vval
            if hval > self.hmax : self.hmax = hval
            if hval < self.hmin : self.hmin = hval
            self.vdata[y][x] = vval
            self.hdata[y][x] = hval
            tval = sqrt((vval**2)+(hval**2))
            if tval > self.tmax : self.tmax = tval
            self.tdata[y][x] = tval
            
        for x,y in i_j_itterator(self.width,self.height):
            vval =  self.vdata[y][x]
            hval =  self.hdata[y][x]
            tval =  self.tdata[y][x]
            pixval = norm(vval,0,self.vmax,127,255) if vval >= 0 else norm(vval,self.vmin,0,0,127)
            self.vdraw.point((x,y),(pixval,))
            pixval = norm(hval,0,self.hmax,127,255) if hval >= 0 else norm(hval,self.hmin,0,0,127)
            self.hdraw.point((x,y),(pixval,))
            pixval = norm(tval,0,self.tmax,0,255)
            self.draw.point((x,y),(pixval,))
























s = Sobel()
b = Blurer(5)
s('a.jpg')
