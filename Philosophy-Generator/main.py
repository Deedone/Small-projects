# -*- coding: utf-8 -*-
import vk_api
import sys
import requests
from PIL import Image, ImageTk
from time import time, sleep
from random import randint

from proxy import *
from auth import log,pasw
from markov2 import Markov
from telega import TAPI

proxies = {}
vk_session = 0
captcha_key= 0
t = 0

oldprint = print
def print(*args, **kwargs):
    with open("log.txt","a") as f:
        oldprint(args,kwargs,file=f)
    oldprint(*args,**kwargs)


def prepare():
    global proxies
    global vk_session
    global t
    t = TAPI()
    
    vk_session = vk_api.VkApi(
        log, pasw,
        captcha_handler=captcha_handler, #функция для обработки капчи
        auth_handler=auth_handler  # функция для обработки двухфакторной аутентификации
    )

    try:
        requests.get("http://vk.com",timeout=4)
        print("No proxy needed")
    except Exception:
        print("Installing proxy")
        p = get_p()
        proxies = p[1]
        vk_session.http.proxies = proxies

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    
def auth_handler():
    # Код двухфакторной аутентификации
    key = t.get_twofactor()
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

def captcha_handler(captcha):
    #get image
    r = requests.get(captcha.get_url(),proxies=proxies,stream=True)
    assert(r.status_code == 200)
    img = r.raw.read()
    with open("temp.jpg","wb") as f:
        f.write(img)

    key = t.get_key()
    
    print(key)

    return captcha.try_again(key)

def should_post():
    try:
        with open("lastposttime",'r') as i:
            t = float(i.read())
    except Exception:
        t = 0
        
    return time() - t > 60*60*3 #3 hours
        

def update_time():
    with open('lastposttime','w') as o:
        o.write(str(time()))

def post(api):
    print("Creating Markov chain")
    t = time()
    m = Markov('samples',7,250)
    text = m.gen()
    print("Generated in",time()-t,"seconds")
    api.wall.post(owner_id=-155694172, message=text)
    print("Posted")
    update_time()
    del m
    


def main():
    print("Started")
    prepare()
    api = vk_session.get_api()
   
    while True:
        try:
            if should_post():
                post(api)
            sleep(60*10)

        except Exception as e:
            
            print("REBUILDING CORE\n",e)
            prepare()
            api = vk_session.get_api()


if __name__ == '__main__':
    main()
