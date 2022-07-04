"""this stores the values in all pages"""
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
import requests
import urllib.request
import shutil
import random
import re
import pandas as pd


title = []
_links=[]
im_link =[]
image_info = []

#dimension = [] #dimension of the artwork
#date_created =[] #date artwork was created
#artwork_origin =[] #artwork origin
#medium = [] #artwork medium
decript_aut=[]#details about author
artwork_artist=[] #artist name
#artwork_dept=[] #artwork department
title_artwork=[] # artwork title
#date_released=[] # date artwork was released
aut_life=[] #authors name and time lived

def getdata(url): 
    r = requests.get(url) 
    return r.text

page = 200
url = f"https://www.artic.edu/collection?is_public_domain=1&page={page}"
#print(url)
response = requests.get(url)
html = response.content
soup = bs(html, "html.parser")
        
for all_title in soup.find_all('strong', class_="title f-list-7"):
    tit=all_title.get_text() ##provides the title of the art work in image_url
    title.append(tit)
    
for a in soup.find_all('a',class_="m-listing__link"):
    image_tag = a.findChildren("img")
    image_tilt=a.findChildren("strong",class_="title f-list-7")
        
    for i in image_tilt:
        v=random.randint(3, 9)
        if i == None:
            print(i.append(v))
        else:
            #image_info.append(i.get_text())
            for c in image_tag:
                cd=c["data-pin-media"]
                z=(cd,i.get_text())
                image_info.append(z)

            
for item_t in soup.find_all('span'):
    images = item_t.find_all('img', {'data-pin-media':re.compile('.jpg')})
    for image in images:
        image_url=((image['data-pin-media']+'\n')) #provides the image link to download with 600 size
        im_link.append(image_url)
    #print(image_url)
    
    
for all_links in soup.find_all('a',class_="m-listing__link"):
    links=(all_links['href']) ##provide link to webpage for each item
    _links.append(links)
#print(_links)
    
for all_link in _links:
    cont_page= requests.get(all_link)
    htmls = cont_page.content
    sou= BeautifulSoup(htmls,"html.parser")
    for item_t in sou.find_all('p',class_="title f-secondary o-article__inline-header-display")[:-1]:
        datx=(item_t.get_text()) ## obtain date artwork was released
        date_released.append(datx)
        
    for item_t in sou.find_all('p',class_="title f-secondary o-article__inline-header-display")[1:]:
        daty=(item_t.get_text()) ##obtain author life on earth
        aut_life.append(daty)
        
    for item_t in sou.find_all('span', class_ ="title f-headline-editorial o-article__inline-header-title"):
        title_artwork.append(item_t.get_text()) ##artwork title
        
    for item_t in sou.find_all('ul', class_="list list--inline f-secondary"):        
        artwork_dept.append(item_t.get_text()) ## artwork department
        
    for item_t in sou.find_all('div',class_="o-blocks"):
        for i in list([item_t.find_all('p')[0:][:-2]]):
            if i == []:
                [x for x in i if x]
            else:
                decript_aut.append(i)
                        
    for item_t in sou.find_all('dl', class_="deflist o-blocks__block"):
        for nex in item_t.find_all('dd')[0]:
            #print(nex.get_text())
            if nex == '\n':
                [x for x in nex if x]
            else:
                d=[]
                d.append(nex.get_text())
                rem_n1 = [x[1:] for x in d]
                rem_n = [x[:-1] for x in rem_n1]
                artwork_artist.append(rem_n) ### artist name
                        
        for n in item_t.find_all('dd')[2]:
            if n == '\n':
                [x for x in n if x]
            else:
                artwork_origin.append(n.get_text()) ##artwork origin
                        
        for e in item_t.find_all('dd')[3]:
            #print(nex.get_text())
            if e == '\n':
                [x for x in e if x]
            else:
                c=[]
                c.append(e.get_text())
                rem_n1 = [x[1:] for x in c]
                rem_n = [x[:-1] for x in rem_n1]
                date_created.append(rem_n) ### date artwork was created
                
        for cex in item_t.find_all('dd')[4]:
            if cex == '\n':
                [x for x in cex if x]
            else:
                medium.append(cex.get_text()) ##artwork medium
                        
        for cx in item_t.find_all('dd')[5]: 
            if cx == '\n':
                [x for x in cx if x]
            else:
                dimension.append(cx.get_text()) ##artwork dimension

f=(title,artwork_artist,title_artwork,date_released,aut_life,artwork_dept,dimension,date_created,artwork_origin,medium,image_info)
df_ = pd.DataFrame(f,index = ["title","authors_name",
                              "artwork_title","date_released",
                              "authors_name_and_age","artwork_department",
                              "dimension","date_created","artwork_origin",
                              "artwork_medium","image_information"])

dataset=pd.DataFrame(df_.T)
