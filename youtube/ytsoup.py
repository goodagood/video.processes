import urllib2
from BeautifulSoup import BeautifulSoup
import time
import re
import os

def gather_multi_vl(kws, numbers=1200, onepiece=200, start=1, name='vloe' ):
    number_of_folders = numbers/onepiece
    for i in range( number_of_folders ):
        folder_name = "%s%i"%(name, i)
        nstart = start + i * (onepiece/20)
        gather_vlinks_on_encoder(kws, onepiece, start=nstart, name=folder_name)

    

def gather_vlinks_on_encoder(kws, numbers=200, start=1, name='vloe' ):
    """Gather the links from youtube and prepare downloading folder.

    So 'keepdl' can do it automatically.
    """
    fetch_vlinks(kws=kws, numbers=numbers, start=start)
    prepare_ytdl(dirname=name)
    pass


def fetch_vlinks(kws, numbers=200, start=1):
    # start is page number
    number_of_pags = int(numbers/20 + 1)
    vlinks = []
    for i in range(start,  start + number_of_pags):
        p   = read_yt_page(kws, page = i)
        ls  = extract_links(p)
        lsa = video_link_filter(ls)
        vlinks.extend(lsa)

        print "page %i, links %i \n"%(i, len(vlinks))
        time.sleep(38)

    vlc = refit_plist(vlinks)
    vlc = de_duplicate(vlc)
    vld = add2full_href(vlc)

    write_vlist(vld)
    return vld

## ??
def get_pages(kws, pages=100, filename='onepiece'):
    video_links = []
    # 10 pages each.
    # rounds 
    rounds = int(pages/10) + 1
    for i in range(1, rounds+1):
        pass
        #todo
        links = fetch_vlinks(kws, numbers=200, start=i)
        video_links.extend(links)

    pass

def de_duplicate(inlist):
    vla = set(inlist)
    vlb = list(vla)
    return vlb

def prepare_ytdl(dirname):
    adir = "/mnt/gyoutube/%s/"%dirname

    cmd = "mkdir /mnt/gyoutube/%s"%dirname
    print "%s \n"%cmd
    os.system(cmd)

    cmd = "mv /tmp/ylsoup  /mnt/gyoutube/%s/yhb"%dirname
    print "%s \n"%cmd
    os.system(cmd)

    cmd = """cp  /home/ubuntu/workspace/video.processes/youtube/autoyoutubedl.pl %s"""%adir
    print "%s \n"%cmd
    os.system(cmd)


def prepare_ytdl_pversion(dirname):
    adir = "/media/my/%s/"%dirname

    cmd = "mkdir /media/my/%s"%dirname
    print "%s \n"%cmd
    os.system(cmd)

    cmd = "mv /tmp/ylsoup  /media/my/%s/yhb"%dirname
    print "%s \n"%cmd
    os.system(cmd)

    cmd = """cp  /home/ubuntu/workspace/video.processes/youtube/autoyoutubedl.pl %s"""%adir
    print "%s \n"%cmd
    os.system(cmd)


def gather_vlinks_on_ec2proxy(kws, numbers=200, start=1, name='vloe' ):
    """Gather the links from youtube and prepare downloading folder.

    So 'keepdl' can do it automatically.
    """
    fetch_vlinks(kws=kws, numbers=numbers, start=start)
    prepare_ytdl_pversion(dirname=name)
    pass

def refit_plist(vlist):
    vnew = []
    for v in vlist:
        # cut off the playlist part in href:
        v = re.sub(r'&playnext=.+$', '', v)
        v = re.sub(r'&list=.+$', '', v)
        vnew.append(v)
        pass
    return vnew


def add2full_href(vlist):
    vnew = []
    for v in vlist:
        # cut off the playlist part in href:
        v = "http://www.youtube.com" + v
        vnew.append(v)
        pass
    return vnew




def write_vlist(vlist, filename = '/tmp/ylsoup'):
    with open(filename, 'wb') as fh:
        fh.write("\n".join(vlist))


def read_yt_page(kws, page = 0):
    keywords = "+".join(kws)
    url = "http://www.youtube.com/results?search_query=%s"%keywords

    if page > 1:
        url = url + "&page=%i"%page
    #url = "http://www.youtube.com/results?search_query=female+mma+ko&page=5

    try:
        urlopen = urllib2.urlopen(url)
        page = urlopen.read()
    except:
        page = ''

    return page


def extract_links(html):
    bs = BeautifulSoup(html)
    links = bs.findAll('a')
    href_str_list = get_href_string(links)
    return href_str_list


def video_link_filter(link_str_list):
    filted = []
    for l in link_str_list:
        if l.find('/watch?v=') >= 0:
            filted.append(l)
            pass
        pass
    # reduce duplication
    filted = set(filted)
    filted = list(filted)
    return filted


def get_href_string(allhref):
    hreflist = []
    if not allhref:
        return hreflist

    for a in allhref:
        if a.has_key('href'):
            ha = a['href']
            hreflist.append(ha)
            pass
        pass
    return hreflist
