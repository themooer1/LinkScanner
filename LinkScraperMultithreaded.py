from splinter import Browser
import threading
from collections import deque

executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)
class peekQueue(deque):
    def tolist(self):
        return list(self.queue)
    def isEmpty(self):
        return True if len(self) > 0 else False
    def peek(self,index=0):
        index=int(index)
        if not self.isEmpty():
            return list(self)[index]
        else:
            raise TypeError
class Scanner:
    def __init__(self,siteList='siteList.txt',iterations=2,maxthreads=8):
        self.recursion=iterations
        self.linkqueue=peekQueue()
        self.maxthreads=maxthreads
        self.siteList=self.loadSites(siteList)
        self.output=[]
    def loadSites(self,sitefilename):
        with open(str(sitefilename),'r') as siteListf:
            siteList = siteListf.read().split(",")
            siteListf.close()
        return siteList
    def startScan(self):
        threads=[]
        map(lambda x:self.linkqueue.appendleft((x,1)),self.siteList)
        while not self.linkqueue[0][1] > self.recursion:
            with list() as threads:
                if len(threads) <=self.maxthreads:
                    p=threading.Thread(target=self.scan())
                    threads.append(p)
                    p.start()
                for t in threads:
                    if not t.is_alive():
                        threads.remove(t)
                    print("Thread Added!")
                else:
                    threads[0].join()
                    print("{} Threads Reached!".format(len(threads)))

    def scan(self):
        url = self.linkqueue.pop()
        b.visit(str(url))
        links = list(map(lambda x:x['href'], b.find_by_tag('a')))
        print("sitefinished")
        print(links)
        map(lambda x:self.linkqueue.appendleft(x),links)
        self.linkqueue.task_done(url)
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