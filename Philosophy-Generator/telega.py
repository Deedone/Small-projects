import requests
import time

class TAPI():
    token = "589584568:***"
    url = "https://api.telegram.org/bot{}/{}"
    id = 220444439

    def __init__(self):
        try:
            with open("teledata.txt","r") as i:
                self.index = int(i.read())
        except Exception:
            self.index = 1

    def save(self):
        with open("teledata.txt","w") as o:
            o.write(str(self.index))

    def get_messages(self):
        r = requests.get(self.url.format(self.token,"getUpdates"),params={"offset":self.index})
        data = r.json()
        if not data['ok'] or len(data['result']) < 1:
            return []
        data = data['result']
        self.index = data[-1]['update_id']+1
        self.save()
        return [k['message']['text'] for k in data if 'text' in k['message'].keys()]
    
    def get_key(self):
        data = {"chat_id":self.id}
        files = {"photo" : ("temp.jpg",open("temp.jpg","rb"))}
        r = requests.post(self.url.format(self.token,"sendPhoto"),data=data,files=files)
        assert r.status_code == 200
        data = []
        while len(data) == 0:
            data = self.get_messages()
            time.sleep(5)
        print("got data",data)
        return data[-1]
    
    def get_twofactor(self):
        r = requests.get(self.url.format(self.token,"sendMessage"),data={"chat_id":self.id,"text":"Twofactor plz"})
        data = []
        while len(data) == 0:
            data = self.get_messages()
            time.sleep(5)
        print("got data",data)
        return data[-1]
                         
    
t = TAPI()
