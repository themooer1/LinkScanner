from splinter import Browser
import threading
from collections import deque

executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)
class peekQueue(deque):
    def tolist(self):
        return list(self)
    def isEmpty(self):
        return False if len(self) > 0 else True
    def peek(self,index=0):
        index=int(index)
        if not self.isEmpty():
            return self.tolist()[index]
        else:
            raise IndexError
class Scanner:
    def __init__(self,siteList='siteList.txt',iterations=2,maxthreads=8):
        self.recursion=iterations
        self.linkqueue=peekQueue()
        self.maxthreads=maxthreads
        self.siteList=self.loadSites(siteList)
        print("Sitelist:"+str(self.siteList))
        self.output=[]

    def loadSites(self,sitefilename):
        with open(str(sitefilename),'r') as siteListf:
            siteList = siteListf.read().split(",")
            siteListf.close()
        return siteList
    def startScan(self):
#        threads=[]
        self.linkqueue.extendleft([(x,1) for x in self.siteList])
        print(self.linkqueue.tolist())
        while not self.linkqueue.peek(0)[1] > self.recursion:
            if len(threading.enumerate()) <=self.maxthreads:
                p=threading.Thread(target=self.scan)
                p.start()
                print("Thread Added!")
            else:
                threading.enumerate()[0].join()
                print("{} Threads Reached!".format(len(threads)))


    def scan(self):
        url,tasknum = self.linkqueue.pop()
        b.visit(str(url))
        links = [x['href'] for x in b.find_by_tag('a')]
        print("sitefinished")
        print(links)
        for x in links:
            self.linkqueue.extendleft((x,tasknum+1))
        self.output=self.output+links
    def save(self,filename='links.txt'):
        print("Saving...")
        with open(filename,"w+") as linksf:
            linksf.write('\n'.join(map(str,self.output)))
            linksf.close()
print('Hello!')
if __name__=='__main__':
    linkscanner=Scanner()
    linkscanner.startScan()
    linkscanner.save()