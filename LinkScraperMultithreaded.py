from splinter import Browser
import threading
from queue import Queue

executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)
class Scanner:
    def __init__(self,siteList,iterations=2,maxthreads=8):
        self.recursion=iterations
        self.threads=maxthreads
        self.siteList=siteList
        self.output=[]
        
def loadSites():
    siteListf = open('siteList.txt','r')
    siteList = siteListf.read().split(",")
    siteListf.close()
    return siteList
def scanlistThreaded(siteList, iterations=2, maxthreads=1):
    threads=list()
    siteList = Queue()
    while not siteList.empty():
        p=Process(target=scan(Queue.))
currenttask=0
def scan(siteList, iterations=2):
    global currenttask
    links=list()
    print("Running iteration {}".format(currenttask+1))
    for url in siteList:
        b.visit(str(url))
        links = links + list(map(lambda x:x['href'], b.find_by_tag('a')))
        print("sitefinished")
    print(links)
    currenttask += 1
    if currenttask<iterations:
        links+=scanlist(links)
    return links
def save(links,filename='links.txt'):
    print("Saving...")
    with open(filename,"w+") as linksf:
        linksf.write('\n'.join(map(str,links)))
        linksf.close()
print('Hello!')
save(scanlist(loadSites(),iterations=2,threads=8))