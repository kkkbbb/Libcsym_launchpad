import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
import os

site='https://launchpad.net'
urls=[
    'https://launchpad.net/ubuntu/xenial/+source/glibc',
    'https://launchpad.net/ubuntu/bionic/+source/glibc',
    'https://launchpad.net/ubuntu/focal/+source/glibc',
    'https://launchpad.net/ubuntu/impish/+source/glibc',
    'https://launchpad.net/ubuntu/jammy/+source/glibc'
]

def find_debug(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.debug'):
                res = os.popen('nm -n '+root+'/'+file+' | grep main_arena').read()
                if res:
                    print('success find:',root+'/'+file)
                    return root+'/'+file

def get_pack(link,name):
    res = requests.get(link).content
    only = SoupStrainer(id='source-builds')
    soup = BeautifulSoup(res,'html.parser',parse_only=only)
    if not os.path.exists(name+'_amd64.sym'):
        amd64 = site+soup.find_all('a',text='amd64')[0]['href']
    else:
        amd64 = 0
        print(name+'_amd64.sym already exists')
    if not os.path.exists(name+'_i386.sym'):
        i386 = site+soup.find_all('a',text='i386')[0]['href']
    else:
        i386 = 0
        print(name+'_i386.sym already exists')
    
    if amd64:
        pack_url = requests.get(amd64).content
        only = SoupStrainer(id='files')#files > ul > li:nth-child(5) > a
        soup = BeautifulSoup(pack_url,'html.parser',parse_only=only)
        try:
            pack64 = soup.find_all('a',text=re.compile('libc6-dbg.*'))[0]['href']
        except:
            pack64 = 0
            print('not found '+name+'_amd64.sym')
        if pack64:
            print(name+'_amd64:'+pack64)
            os.system('wget '+pack64+' -O '+name+'_amd64.deb;dpkg -X '+name+'_amd64.deb '+name)
            if os.path.exists(name+'/usr/lib/debug/lib/x86_64-linux-gnu/'):
                os.system('nm -n '+name+'/usr/lib/debug/lib/x86_64-linux-gnu/libc-*.so > '+name+'_amd64.sym;rm -rf '+name+'_amd64.deb;rm -rf '+name)
            else:
                res = find_debug(name)
                os.system('nm -n '+res+' > '+name+'_amd64.sym;rm -rf '+name+'_amd64.deb;rm -rf '+name)

    if i386:
        pack_url = requests.get(i386).content
        only = SoupStrainer(id='files')#files > ul > li:nth-child(5) > a
        soup = BeautifulSoup(pack_url,'html.parser',parse_only=only)
        try:
            pack32 = soup.find_all('a',text=re.compile('libc6-dbg.*'))[0]['href']
        except:
            pack32 = 0
            print('not found '+name+'_i386.sym')
        if pack32:
            print(name+'_i386:'+pack32)
            os.system('wget '+pack32+' -O '+name+'_i386.deb;dpkg -X '+name+'_i386.deb '+name)
            if os.path.exists(name+'/usr/lib/debug/lib/i386-linux-gnu/'):
                os.system('nm -n '+name+'/usr/lib/debug/lib/i386-linux-gnu/libc-*.so > '+name+'_i386.sym;rm -rf '+name+'_i386.deb;rm -rf '+name)
            else:
                res = find_debug(name)
                os.system('nm -n '+res+' > '+name+'_i386.sym;rm -rf '+name+'_i386.deb;rm -rf '+name)

for url in urls:
    res = requests.get(url).content
    only = SoupStrainer(id='portlet-releases')
    soup = BeautifulSoup(res,'html.parser',parse_only=only)
    items = list(set([site+x['href'] for x in soup.select('#portlet-releases > ul > li > a')]))
    print(url,'总长度:'+str(len(items)))
    for href in items:
        name = href.split('/')[-1]
        print("succes get href:",href) 
        get_pack(href,name)
