# encoding=utf-8
import os
import os.path
import re
import sys

import codecs

#import gtrans  # google translate tool
from gtrans import quick_translate, quick_detect

folder = '/home/za/myvid/amis'

def getall_names( filename = '/tmp/a'):
    """get a list of names from a file
    """
    #fns = os.listdir(folder)
    with open(filename, 'rb') as namefile:
        string = namefile.read()
        ss = string.split("\n")

    return ss


def refit_filenames():
    fns = getall_webm()
    refits = []
    for fn in fns:
        if fn.endswith('.webm'):
            refit = fn[:-5]
        else:
            refit = ''
            pass
        refit = refit.replace('_', ' ')
        refit = refit.replace('quot', '')
        refit = refit.replace(' 39', '')
        if refit:
            refits.append(refit)

    return refits


def refit_filename(name):

    refit = name
    if name.endswith('.webm'):
        refit = name[:-5]
        pass

    refit = refit.replace("_39_s", "'s")
    refit = refit.replace('_', ' ')
    refit = refit.replace('.', ' ')

    amp = re.compile(r'\bamp\b', re.I)
    refit = amp.sub(' ', refit)

    quot = re.compile(r'\bquot\b', re.I)
    refit = quot.sub(' ', refit)

    n39 = re.compile(r'\b39\b')
    refit = n39.sub(' ', refit)

    if not refit:
        refit = 'no name'

    return refit


def trans_cname( folder = '/tmp', out_file='cname'):
    filenames = getall_names()

    name_cname = []
    for fn in filenames:
        newname = refit_filename(fn)
        #lang = quick_detect(newname)
        cname = quick_translate(newname, "zh-CN", 'en')
        if not cname:
            cname = newname

        pair = dict(name=fn, cname=cname)
        print fn, " -- ", cname
        name_cname.append(pair)
        #print newname
        pass

    '''
    for nc in name_cname:
        print nc['name']
        print nc['cname']
        pass
        '''

    full_path_out_file = os.path.join(folder, out_file)

    #with open(full_path_out_file, 'wb+') as f:
    # I always wonder why codecs needed on Ubuntu?
    with codecs.open(full_path_out_file, mode='w+', encoding='utf-8') as f:
        for namepair in name_cname:
            f.write(namepair['name'])
            f.write("\n")
            f.write(namepair['cname'])
            f.write("\n")
            f.write("\n")

    return name_cname



if __name__ == "__main__":
    #print getall_names()
    trans_cname()
"""
    print sys.argv[1:]

    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = '/home/za/myvid/amis'


    make_cname_file(folder)


    #print refit_filename('fjdk quot fjdkl quot amp 39 399 quott')

    '''
    with codecs.open('/tmp/aafutf', mode='w+', encoding='utf-8') as f:
        f.write(u'阿飞点卡 ASDF')
        '''
"""
