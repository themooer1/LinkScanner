from splinter import Browser
import threading
from queue import PriorityQueue

executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)
class peekQueue(PriorityQueue):
    def peek(self,index=0):
        if type(index) == int:
            return self.queue[item]
        else:
            raise TypeError
    def tolist(self):
        return list(self.queue)
class Scanner:
    def __init__(self,siteList='siteList.txt',iterations=2,maxthreads=8):
        self.recursion=iterations
        self.linkqueue=peekQueue
        self.threads=maxthreads
        self.siteList=self.loadSites(siteList)
        self.output=[]
    def loadSites(self,sitefilename):
        with open(str(sitefilename),'r') as siteListf:
            siteList = siteListf.read().split(",")
            siteListf.close()
        return siteList
    def startScan(self):
        threads=list()
        while not self.linkqueue.peek('0')[1] > self.recursion:
            p=threading.Thread(target=self.scan())
    def scan(self,siteList, iterations=2):
        url = self.linkqueue.get()
        b.visit(str(url))
        links = list(map(lambda x:x['href'], b.find_by_tag('a')))
        print("sitefinished")
        print(links)
        map(lambda x:self.linkqueue.put(x),links)
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