
from PIL import Image, ImageDraw
import sys
START = (1,2,3,4)
STOP = (1,2,3,0)

img = 'test.png'  #'test.png' 
image = Image.open(img)
draw = ImageDraw.Draw(image,'RGBA')
width = image.size[0]
height = image.size[1]
pix = image.load()

dic = {'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001'}
rdic = {}
for k in dic.keys():
    rdic[dic[k]] = k


##### end init
def count(pix,h,w):
    counter = 0
    print('Counting available memory')
    for i in range(w):
        for j in range(h):
            if pix[i,j][3] == 255:
                counter +=1
    print('You have {} bits of space'.format(counter))
    return counter
        
def pinput():
    print('Введи свой текст(на русском блджад без цифр)')
    s = input()
    ret = []
    for c in s:
        x = str(ord(c))[1:]
        if x == '2':
            x = '232'
        #print(x)
        for cc in x:
           ret.append(dic[cc])
    return ret

def save(pix,draw,h,w):
    s = ''.join(pinput())
    s = [c for c in s]
    s.reverse()
    #print(s)
    draw.point((0,0),START)
    for i in range(1,w):
        if len(s) <= 0:
                break
        for j in range(1,h):
            if len(s) <= 0:
                break
            temp = []
            for c in pix[i,j][:3]: ##### [255,255,255]
                if len(s) > 0:
                    if c > 150:#### dont want color to be -1 or 256
                        mod = -1
                    else:
                        mod = 1
                    bit = s.pop()
                    #print(bit)
                    if bit == '1':##### 1 = (c%2 = 1) | 0 = (c%2 = 0)
                        if not c%2:
                            c+=mod
                    if bit == '0':
                        if c%2:
                            c+=mod
                    temp.append(c)
            temp.append(pix[i,j][3])##### add alpha
            while len(temp)<4:
                temp.append(255)### ensure that temp has 4 values
            draw.point((i,j),(temp[0],temp[1],temp[2],temp[3]))###shit
    draw.point((i-1,j),STOP)
    global image
    image.save(img,'PNG')

def read(pix,h,w):
    buff = []
    for i in range(1,w):
        for j in range(1,h):
            if tuple(pix[i,j]) == STOP:
                return buff
            for c in pix[i,j][:3]:
                #print(c)
                buff.append(c%2)

def decrypt(pix,h,w):
    l = read(pix,h,w)
    arr = []
    for i in range(int(len(l)/4)):
        arr.append(''.join([str(c) for c in l[4*i:(4*i)+4]])) #######split list in blocks of four chars
    #print(arr)
    arr2 = []
    for c in arr:
        #print(rdic[c])
        arr2.append(rdic[c])
    #print(arr2)
    arr3 = [arr2[i:i + 3] for i in range(0, len(arr2), 3)]
    for i,c in enumerate(arr3):
        map(str,c)
        arr3[i] = '1'+''.join(c)
        if arr3[i] == '1232':
            arr3[i] = '32'
    print(arr3,'\n\n\n')
    for i in arr3:
        print(chr(int(i)),end='')




try:
    if sys.argv[2] == 'clean':
        draw.point((0,0),(0,0,0,0))
        image.save(img,'PNG')
    elif sys.argv[2] == 'help':
        print("""
    Ну кароче можешь шифровать и наоборот если чот зашифровано то оно
    его сразу расшифрует, что почистить картинку пиши clean после имени
    а так вообще всегда нужно имя каритнки написать а то не будет
    работать вооот
    """)
    sys.exit()
except Exception:
    pass

if tuple(pix[0,0]) == START:
    decrypt(pix,height,width)
else:
    save(pix,draw,height,width)













