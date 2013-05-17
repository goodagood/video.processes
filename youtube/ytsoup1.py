import urllib2
from BeautifulSoup import BeautifulSoup
import time
import re
import os
import pickle
import shutil


class YtLinkList(object):
    def __init__(self, kws, lmax, dirname):
        self.keywords = kws
        self.lmax = lmax
        self.dirname = dirname
        self.links = []

        self.pickle_filename = '/tmp/yllpickle'
        self.current_page = 1
        self.sleep_seconds = 8
        self.base_download_dir = '/mnt/gyoutube/'
        self.yt_links_filename = 'yhb'

    def merge_links(self, new_links):
        new_links = add2full_href(new_links)
        self.links.extend(new_links)
        vlc = refit_plist(self.links)
        vlc = de_duplicate(vlc)
        self.links = vlc
        return self.links

    def pickle_self(self):
        with open(self.pickle_filename, 'wb') as pf:
            pickle.dump(self, pf)
            return True

        return False

    def get_one_page(self):
        page_number = self.current_page
        self.current_page = self.current_page + 1

        lsa = get_links_from_one_page(self.keywords, page_number)
        self.merge_links(lsa)

        print "page %i, total links %i \n"%(page_number, len(self.links))
        self.pickle_self()
        time.sleep(self.sleep_seconds)

    def get_to_this_number(self, number):
        while( len(self.links) < number ):
            old_total = len(self.links)

            self.get_one_page()
            new_total = len(self.links)
            if old_total == new_total:
                return new_total
        return new_total

    def split_links_to_dl_dirs(self, size=250):
        if size <= 0:
            return False

        i = 1
        dname = self.mk_dirname(i)

        while( len(self.links) > 0 ):
            self.prepare_download_dir(dirname=dname, number_of_links=size)
            i = i+1
            dname = self.mk_dirname(i)

    def mk_dirname(self, i):
        dname = "%s%i"%( self.dirname, i)
        dirname = os.path.join(self.base_download_dir, dname)
        return dirname

    def write_links_to_file(self, filename = '/tmp/ylsoup', numbers=300):
        chomp = []
        if numbers > len(self.links):
            numbers = len(self.links)

        for i in range(numbers):
            one = self.links.pop()
            chomp.append(one)
        with open(filename, 'wb') as fh:
            fh.write("\n".join(chomp))
            print ("wrote %i links to file: %s"%(numbers, filename))
            return True
        return False

    def prepare_download_dir(self, dirname, number_of_links):
        os.mkdir(dirname)

        lfilename = os.path.join(dirname, self.yt_links_filename)
        self.write_links_to_file(lfilename, number_of_links)

        autoyoutubedl = "/home/ubuntu/workspace/video.processes/youtube/autoyoutubedl.pl"
        basename = os.path.basename(autoyoutubedl)
        target = os.path.join(dirname, basename)
        print( "copy %s ---> %s\n"%(autoyoutubedl, target))
        shutil.copyfile(autoyoutubedl, target)


    def batch_job_5588(self):
        self.get_to_this_number(5588)
        self.split_links_to_dl_dirs(size=558)

def load_pickled_object(pickle_filename):
    """Load the pickled YtLinkList object, and return it.
    """
    with open(pickle_filename, 'rb') as pf:
        pobj = pickle.load(pf)
        return pobj

    return None


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


def fetch_vlinks(kws, numbers=200, start_page=1):
    # start_page is page number
    number_of_pags = int(numbers/20 + 1)
    vlinks = []
    for i in range(start_page,  start_page + number_of_pags):
        lsa = get_links_from_one_page(kws, i)
        merge_into(vlinks, lsa)

        print "page %i, total links %i \n"%(i, len(vlinks))
        time.sleep(38)

    write_vlist(vlinks)
    return vld


def merge_into(link_list, new_links):
    link_list.extend(new_links)
    vlc = refit_plist(link_list)
    vlc = de_duplicate(vlc)
    vld = add2full_href(vlc)
    link_list = vld
    return link_list


def get_links_from_one_page(kws, page_number):
    p   = read_yt_page(kws, page = page_number)
    ls  = extract_links(p)
    lsa = video_link_filter(ls)
    return lsa


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

    cmd = """cp /home/ubuntu/workspace/video.processes/youtube/autoyoutubedl.pl %s"""%adir
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
