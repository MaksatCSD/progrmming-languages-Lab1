import requests
import re

s = requests.session()

def getpage(url, session, timeout = 5):     #грузим страницу
    try:
        request = session.get(url, timeout = timeout)
    except Exception:
        return "error"  # на всякий случай
    return request.text

def getlinks(rootURL, r):   #получаем чистые обсолютные адреса
    rootURL = re.sub(r'/$','',rootURL)      #убрать лишний/
    httpPattern =re.compile(r'href[ ]?=[ ]?[\'\"]((?:{})?/[^/\s][^\s>\'\"]+)'.format(rootURL))
    links = httpPattern.findall(r)
    nonlinks = []
    for lId in range(len(links)):
        if re.match(rootURL,links[lId])==None:      #относительные адреса в абсолютные
            links[lId] = rootURL+links[lId]
        if re.search(r'(\b/[^/\s\.]+\.\w{1,5})',links[lId])!=None:      #избавимся от ненужных фалов
            nonlinks.append(links[lId])
    for nl in nonlinks:
        links.remove(nl)
    return links

mailPattern = re.compile(r'[\w\d\-\.\_]+@[\w\d\-\_]+\.\w{1,5}')
visitedSet=set()
mailsSet=set()

def getMails(rootURL, urlToGo, recDepths): # рекурсивная функция
    flag = recDepths
    print("RECDEPHS:",flag)
    r = getpage(urlToGo,s)
    linksList = getlinks(rootURL,r)
    for mail in mailPattern.findall(r):
        mailsSet.add(mail)
    if recDepths>0:
        while len(linksList)>0:
            link = linksList.pop(0)
            while link in visitedSet:
                if len(linksList)==0:
                    return
                link = linksList.pop(0)
            print("going to:",link)
            visitedSet.add(link)
            getMails(rootURL, link, recDepths-1)
        return

url1 ="http://www.csd.tsu.ru/"
getMails(url1,url1,3)
print(mailsSet)
