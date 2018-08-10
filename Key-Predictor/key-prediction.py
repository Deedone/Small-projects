from random import randint



class Gram:
    def __init__(self,s,n=''):
        self.pattern = s
        self.dcount = self.fcount = 0
        if n == 'd':
            self.dcount+=1
        elif n =='f':
            self.fcount+=1
    def add(self,n):
        if n == 'd':
            self.dcount+=1
        else:
            self.fcount+=1

    def predict(self):
        return 'f' if self.fcount > self.dcount else 'd'

    def __str__(self):
        return self.pattern


        
grams = {}
results = []
seq = ''
while len(seq) < 6:
    t = input("\nd or f: ")
    if t == 'd' or t == 'f':
        seq = seq + t
        

def add_gram(seq):
    global grams
    t = seq[-6:]
    if t[:5] in grams:
        grams[t[:5]].add(t[5])
    else:
        grams[t[:5]] = Gram(t[:5],t[5])


while True:
    if seq[-5:] in grams:
        pred = grams[seq[-5:]].predict()
        #print("Got prediction")
    else:
        pred = 'f' if randint(1,10) > 5 else 'd'
    inp = input("\nd or f: ")
    if inp != 'd' and inp != 'f':
        print("Fool")
        continue
    
    if pred == inp:
        print("Guess ",end='')
        results.append(1)
    else:
        print("Not guess ",end='')
        results.append(0)

    print("Success rate = ",int((results.count(1)/len(results))*100))
    if len(results) > 100:
        results.pop(0)
    seq = seq + inp
    add_gram(seq)
    if len(seq) > 1000:
        seq = seq[1:]






        
