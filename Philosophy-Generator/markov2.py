import codecs
import random

class Markov:

    def __init__(self,inp,order = 8, length = 500):
        self.order = order
        self.len = length
        self.process_inp(inp)


    def process_inp(self,inp):
        with codecs.open(inp,'r',"utf_8") as i:
            self.buf = i.read().strip()
        self.grams = self.make_grams(self.order)
        

    def make_grams(self,order):
        grams = {}
        for i in range(0,len(self.buf)-order):
            key = self.buf[i:i+order]
            val = self.buf[i+order]
            #print(key,val)
            if key not in grams:
                grams[key] = {}
            if val in grams[key]:
                grams[key][val]+=1
            else:
                grams[key][val]=1
        for key in grams:
            grams[key] = [[k,grams[key][k]] for k in grams[key]] 
        return grams

    def weighted_choice(self,choices):
       total = sum(w for c, w in choices)
       r = random.uniform(0, total)
       upto = 0
       for c, w in choices:
          if upto + w >= r:
             return c
          upto += w
       assert False, "Shouldn't get here"

    def gen(self):
        text = random.choice([k for k in self.grams.keys()])
        while len(text) < self.len:
            key = text[-self.order:]
            n = self.weighted_choice(self.grams[key]) 
            text = text + n
        return self.prettify(text)

    def prettify(self,text):
        startpos = endpos = 0
        for i,c in enumerate(text):
            if c in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯЪЬ":
                startpos = i
                break

        endpos = text.rindex('.')

        text = text.replace('\n\n','\n')
        return text[startpos:endpos+1].strip()
















        






