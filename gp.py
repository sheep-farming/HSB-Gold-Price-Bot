import urllib2
from datetime import datetime
from sgmllib import SGMLParser
import time
import os
class MySgmlParser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.label = False
        self.nm = []

    def start_td(self, attrs):
        self.label = True

    def end_td(self):
        self.label = False

    def handle_data(self, data):
        if self.label:
            #data = data.strip()
	    self.nm.append(data.replace(' ','').replace(' ','').replace('\r','').replace('\n','').replace('\t',''))
now=datetime.now()
now=str(datetime.time(now))[0:8]
pricelist=[]

log=open('log/'+now.replace(':','')+'.txt','w')
def getPrice():
    content=urllib2.urlopen('http://bank.hangseng.com/1/2/rates/gold-prices/gold-prices').read()    
    listname = MySgmlParser()
    listname.feed(content)
    return listname.nm


def loop():
    global pricelist
    rst=getPrice()
    ask=rst[5]
    bid=rst[4]
    an=float(ask.replace(',',''))
    bn=float(bid.replace(',',''))
    pricelist.append(an)
    now=datetime.now()
    now=str(datetime.time(now))[0:8]
    bp=int((an-bn)/((an+bn)/2)*10000)
    os.system('clear')    
    print '\033[31mBID'+ask+'\033[32m ASK'+bid+'\033[33m SPR'+str(bp)+'\033[0m '+now+'\033[0m'
    log.write(str([ask,bid,now])+'\n')
    
    
def draw(lst):
    maxi=round(max(lst)+.1,1)
    mini=round(min(lst)-.1,1)
    leglen=max([len(str(float(maxi))),len(str(float(mini)))])
    x=80
    y=30
    global fd,sd,m
    sd=[]
    fd=[]
    m=[]
    
    for i in range(x):
        m.append([])
        for j in range(y):
            m[i].append(0)    
    
    for i in range(len(lst)*x):
        sd.append(lst[int(i/x)]*1.0)

    for i in range(x):
        k=((sum(sd[i*len(lst):(i+1)*len(lst)])/len(lst)-mini)*(y-1)*1.0/(maxi-mini))
        fd.append(int(k))
        m[i][int(k)]=1

    for i in range(y):
        if i==0:
            buf='=HistChart'+'='*(x+len(str(float(mini)))-9)+'\n'+str(float(maxi))+'-\033[47m'
        elif i==y-1:
            buf=str(float(mini))+'-\033[47m'
        else:
            buf=' '*(leglen+1)+'\033[47m'
            
        for j in range(x):
            v=m[j][y-1-i]
            if v==1:
                if j==x-1:
                    buf=buf+'\033[5;31;47m*\033[0m'+'-\033[1;43m'+str(lst[len(lst)-1])+'\033[0m'
                else:
                    buf=buf+'\033[31;47m*'
            else:
                buf=buf+' '
        print(buf+'\033[0m')
        if i==y-1:
            print('='*(x+len(str(float(mini)))+1))



while(1):
    loop()
    if len(pricelist)>2:
        draw(pricelist)
    time.sleep(2)    
    