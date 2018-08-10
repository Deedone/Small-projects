import requests
import re
from time import time
from threading import Thread
import json

def get_p():
    try:
        with open("pcache.json") as f:
            data = json.loads(f.read())
            if time() - data[0] < 6000:
                pstring = "{}:{}".format(data[1][0],data[1][1])
                pdic = {'http':'http://'+pstring,
               'https':'https://'+pstring}  
                return [data[1],pdic]
    except Exception:
        pass
    data = requests.get("https://free-proxy-list.net/anonymous-proxy.html").text
    #print(data)
    proxies = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d{3,5})</td><td>..</td><td.{11}>.{1,15}</td><td>.{5,20}</td><td.{11}>(?:yes|no)</td><td.{11}>yes',data)
    print("Debug: get {} proxies from list".format(len(proxies)))
    proxies = [list(p) for p in proxies]
    threads = []
    for p in proxies:
        if len(threads) > 30:
            for t in threads.copy():
                t.join()
                threads.remove(t)
        t = Thread(target=get_latency,args=(p,))
        threads.append(t)
        t.start()
    for t in threads.copy():
        t.join()
        threads.remove(t)
        
    proxies.sort(key=lambda x: x[2])
    pstring = "{}:{}".format(proxies[0][0],proxies[0][1])
    pdic = {'http':'http://'+pstring,
               'https':'https://'+pstring}
    with open("pcache.json","w") as f:
        data = [time(),proxies[0]]
        f.write(json.dumps(data))
    
    return [proxies[0],pdic]

def get_latency(proxy):
    #print("kok")
    pstring = "{}:{}".format(proxy[0],proxy[1])
    proxies = {'http':'http://'+pstring,
               'https':'https://'+pstring}
    try:
        start = time()
        r = requests.get("https://login.vk.com",proxies=proxies,timeout=4)
        end = time()
        
        proxy.append(end-start)
    except Exception:
        proxy.append(9999)
