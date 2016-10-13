from splinter import Browser

executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)

def loadSites():
    siteListf = open('siteList.txt','r')
    siteList = siteListf.read().split(",")
    siteListf.close()
    return siteList

currenttask=0
def scanlist(siteList, iterations=6):
    global currenttask
    linksFull=list()
    links=list()
    print("Running iteration {}".format(currenttask+1))
    for url in siteList:
        b.visit(str(url))
        links = links + list(map(lambda x:x['href'], b.find_by_tag('a')))
        print("sitefinished")
    print(links)
    currenttask += 1
    linksFull+=scanlist(links)
    return links
def save(links,filename='links.txt'):
    with open(filename,"w+") as linksf:
        linksf.write('\n'.join(map(str,links)))
        linksf.close()
print('Hello!')
save(scanlist(loadSites(),iterations=3))