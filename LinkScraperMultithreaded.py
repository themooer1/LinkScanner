from splinter import Browser
import threading
import queue

executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)

def loadSites():
    siteListf = open('siteList.txt','r')
    siteList = siteListf.read().split(",")
    siteListf.close()
    return siteList
def scanlistThreaded(siteList, iterations=2, threads=1):
    threads=[]
    threadsize=int(len(siteList)/threads))
    for i in range(0,threads):
        t=threading.Thread(target=scanlist,args=(siteList[i*threadsize:(i+1)*threadsize],iterations=2))
        threads.append(t)
        t.start()

currenttask=0
def scanlist(siteList, iterations=2):
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