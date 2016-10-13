from splinter import Browser
executable_path = {'executable_path':'/usr/local/bin/phantomjs'}
b=Browser("phantomjs",**executable_path)
links = list()
with open('siteList.txt','r') as siteListf:
    siteList=siteListf.read().split(",")
    siteListf.close()
for url in siteList:
    b.visit(str(url))
    links = links + list(map(lambda x:x['href'], b.find_by_tag('a')))
with open('links.txt',"w+") as linksf:
    linksf.write('\n'.join(map(str,links)))
    linksf.close()