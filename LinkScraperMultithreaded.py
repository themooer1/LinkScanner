import requests
import string
import threading
from collections import deque
from time import sleep

class peekQueue(deque):
    def __init__(self):
        self.lock=threading.Lock()
    def tolist(self):
        return list(self)
    def isEmpty(self):
        return False if len(self) > 0 else True
    def peek(self,index=0):
        index=int(index)
        try:
            return self.tolist()[index]
        except:
            return (None,1)
class Scanner:
    def __init__(self,siteList='siteList.txt',iterations=2,maxthreads=8,autoSave=30):
        """Iterations is the recursion depth to which the scanner will follow URLs.  Maxthreads is how many individual URLs
        the scanner will request in parallel.  AutoSave indicates the number of seconds between automatic saves or False
        to disable."""
        self.recursion=iterations
        self.linkqueue=peekQueue()
        self.maxthreads=maxthreads
        self.siteList=self.loadSites(siteList)
        print("Sitelist:"+str(self.siteList))
        self.output={}
        self.autoSaveDave = None
        if autoSave is not False:
            self.autoSaveDave=threading.Thread(name="autoSave",target=self.autoSave(int(autoSave)))

    def loadSites(self,sitefilename):
        with open(str(sitefilename),'r') as siteListf:
            siteList = siteListf.read().split(",")
            siteListf.close()
        return siteList

    def getAllLinks(self,html):
        links = []
        start = html.find('href="')
        end = html.find('"', start + 6)
        while True:
            if start == 5:
                try:
                    del links[-1]
                except:
                    pass
                break
            else:
                start = html.find('href="') + 6
                end = html.find('"', start)
                link = html[start:end]
                if 'http://' in link:
                    links.append(link)
                elif 'https://' in link:
                    links.append(link)
                elif '//' in link:
                    links.append('http:'+link)
                html = html[end:]
        return links
    def isValidURL(self,url):
        if "mailto:" in str(url):
            return False
        else: return True

    def startScan(self):
        self.linkqueue.extendleft([(x,1) for x in self.siteList])
        print(self.linkqueue.tolist())
        if self.autoSaveDave !=None:
            self.autoSaveDave.start()
        while not self.linkqueue.peek(0)[1] > self.recursion:
            if (len(threading.enumerate()) <=self.maxthreads+1) and not self.linkqueue.isEmpty():
                p=threading.Thread(target=self.scan)
                p.start()
#                print("Thread Added!")
            elif len(threading.enumerate()) >=self.maxthreads:
                threading.enumerate()[-1].join()
                print("{0} Threads Reached!".format(len(threading.enumerate())))
                self.save()
            else:
                sleep(1)


    def scan(self):
        with self.linkqueue.lock:
            url,tasknum = self.linkqueue.pop()
        if "mailto:" in str(url):
            pass
        elif 'android-app://' in str(url):
            pass
        elif url in self.output:
            self.output.update({url: {'getCount': self.output[url]['getCount'] + 1}})
        else:
            r = requests.get(url,verify=False)
            links = self.getAllLinks(r.text)
            for x in links:
                self.linkqueue.appendleft((x,tasknum+1))
            self.output.update({url:{'getCount':1}})
    def save(self,filename='links.txt'):
        print("Saving...")
        with open(filename,"w+") as linksf:
            linksf.write("RESULTS\n"+'\n'.join(map(str,self.output.keys())))
            linksf.close()
    def autoSave(self,delay):
        while True:
            sleep(delay)
            self.save()
print('Hello!')
if __name__=='__main__':
    linkscanner=Scanner(iterations=30000000000000,maxthreads=20,autoSave=False)
    linkscanner.startScan()
    linkscanner.save()
