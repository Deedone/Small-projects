from PIL import Image
from time import time, sleep
from io import BytesIO
from multiprocessing.pool import ThreadPool
import sys
import requests
import threading
import vk_api
import pprint
import webbrowser
import proxy

pp = pprint.PrettyPrinter(indent=4)
proxy = proxy.get_p()
COUNTER = 0
BAR = 0
SIZE = 20

def getUser(api):
    r = api.users.get()
    pp.pprint(r)
    return 378237592 #r[0]['id']

def genhash(img):
    binary = ''
    img = img.resize((SIZE,SIZE), Image.BILINEAR)
    img = img.convert(mode="RGB")
    pix = img.load()
    try:
        avg = sum([sum(pix[i,j][0:3])//3 for i in range(SIZE) for j in range(SIZE)])//(SIZE**2)
    except Exception:
        avg = 255//2

    for i in range(SIZE):
        for j in range(SIZE):
            try:
                s = (pix[i,j][0] + pix[i,j][1] + pix[i,j][2])//3
            except Exception:
                print(pix[i,j])
                s = 0
            if s > avg:
                binary += '1'
            else:
                binary += '0'

    return binary

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. 
    """
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

def processImage(t):
    global COUNTER
    try:
        r = requests.get(t[0],proxies=proxy[1])
        img = Image.open(BytesIO(r.content))
        t.append(genhash(img))
        COUNTER+=1
        if not COUNTER%50:
            print(COUNTER)
        return t
    except Exception as e:
        print(e)
        t.append('0'*(SIZE**2))
        return t

def processImageList(l):
    global COUNTER
    COUNTER = 0
    pool = ThreadPool(50)
    results = pool.map(processImage, l)
    return results
    
def distance(s1,s2):
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def startSession(login='+***',passwd='****'):
    api = vk_api.VkApi(login, passwd,captcha_handler=captcha_handler,auth_handler=auth_handler)
    print(proxy)
    api.http.proxies = proxy[1]
    api.auth()
    return api.get_api()

def getAllPhotos(api,uid):
    albums = api.photos.getAlbums(owner_id=uid,need_system=1)
    photos = []
    pp.pprint(albums)
    for a in albums['items']:
        goal = a['size']
        offset = 0
        while offset<goal:
            temp = api.photos.get(owner_id=uid,album_id=a['id'],photo_sizes=1,offset=offset,count=100)
            offset+=len(temp['items'])
            #pp.pprint(temp)
            for it in temp['items']:

                link = it['sizes'][0]['src']
                aid = it['album_id']
                id = it['id']
                photos.append([link,id,aid])
    return photos

def filterSizes(l):
    pp.pprint(l)
    for size in l:
        if size['type'] not in 'opqr':
            ret = size['src']
    return ret

def checkall(p,uid):
    res = []
    p = p.copy()
    for a in p:
        for b in p:
            if distance(a[3],b[3]) < 1 and a!=b:
                print("\n","https://vk.com/photo{}_{}".format(uid,a[1]),"\n","https://vk.com/photo{}_{}".format(uid,b[1]),"\n",distance(a[3],b[3]))
                res.append(["https://vk.com/photo{}_{}".format(uid,a[1]),"https://vk.com/photo{}_{}".format(uid,b[1])])
        p.remove(a)
    return res

photos = 00
photos2 = 00
def main():
    global photos
    global photos2
    print("Setting up api")
    api = startSession()
    print("api done")
    uid = getUser(api)
    photos = getAllPhotos(api,uid)
    print(len(photos))
    photos2 = processImageList(photos)
    res = checkall(photos2,uid)
    for r in res:
        webbrowser.open(r[0])
        webbrowser.open(r[1])
        input()



main()




















