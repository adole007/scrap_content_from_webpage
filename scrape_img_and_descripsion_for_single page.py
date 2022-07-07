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

dimension = [] #dimension of the artwork
date_created =[] #date artwork was created
artwork_origin =[] #artwork origin
medium = [] #artwork medium
decript_aut=[]#details about author
artwork_artist=[] #artist name
artwork_dept=[] #artwork department
title_artwork=[] # artwork title
date_released=[] # date artwork was released
aut_life=[] #authors name and time lived
filenames=[] #artwork names scrapped

def getdata(url): 
    r = requests.get(url) 
    return r.text
#f=(title,title_artwork,image_info,im_link,_links,decript_aut,artwork_artist)


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
    
def download_image(image_info):
    response = requests.get(image_info[0], stream=True)
        
    realname = ''.join(e for e in image_info[1][:30] if e.isalnum())
    
    file = open("./images_bs/{}.jpg".format(realname), 'wb')
    
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    filenames.append(realname) ##names for the artwork
    
    del response  
    
for all_links in soup.find_all('a',class_="m-listing__link"):
    links=(all_links['href']) ##provide link to webpage for each item
    _links.append(links)
    #print(_links)
    
for all_link in _links:
    cont_page= requests.get(all_link)
    htmls = cont_page.content
    sou= BeautifulSoup(htmls,"html.parser")
    
    for it in sou.find_all('div', class_="o-article__body o-blocks"):
        for item_t in sou.find_all(class_="o-blocks"):
            for i in list([item_t.find_all('p')[0:]]):
                if i == []:
                    [x for x in i if x]
                else:
                    decript_aut.append(i)

for i in range(0, len(image_info)):
    download_image(image_info[i])
    
f=(title,filenames,decript_aut)
df_ = pd.DataFrame(f,index = ["title","scrapped_artwork_name","description"])
dataset=pd.DataFrame(df_.T)
