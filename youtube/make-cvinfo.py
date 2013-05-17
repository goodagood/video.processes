#!/usr/bin/python
# encoding=utf-8
import os
import os.path
import re
import sys
import time
import pickle

import codecs

#import gtrans  # google translate tool
from gtrans import quick_translate, quick_detect

vi_delimit = '---goodagood-video-info-delimit---'

class Tdata(object):
    vi_delimit = '---goodagood-video-info-delimit---'

    # file writting might fail, before write it to file, pickle the translated
    pickle_file = '/tmp/pickle-make-vinfos'

    video_info_file_name = 'cname'

    def __init__(self):
        self.folder = '/mnt/tmp/testc'

        self.filename_list        = []
        self.original_video_infos = []
        self.translated_video_infos = []

        self.translating_progress = 0


    def write_video_info_file(self):
        absfn = os.path.join(self.folder, self.video_info_file_name)
        with codecs.open(absfn, mode='wb', encoding='utf-8') as fh:
            for vinfo in self.translated_video_infos:
                for l in vinfo:
                    #print l
                    # To make sure it's utf-8, this save me 10hrs!!
                    if isinstance(l, str):
                        l = l.decode('utf-8')
                    fh.write(l)
                    fh.write("\n")
                fh.write("\n\n" + self.vi_delimit + "\n\n")


    def write_video_cinfo_file(self):
        absfn = os.path.join(self.folder, self.video_info_file_name)
        with codecs.open(absfn, mode='wb', encoding='utf-8') as fh:
            for vinfo in self.original_video_infos:
                #add language as 'cn' Chinese, note google use 'zh-CN'/'zh-TW'
                vinfo.insert(2, 'cn')
                for l in vinfo:
                    #print l
                    # To make sure it's utf-8, this save me 10hrs!!
                    if isinstance(l, str):
                        l = l.decode('utf-8')
                    fh.write(l)
                    fh.write("\n")
                fh.write("\n\n" + self.vi_delimit + "\n\n")



# Do the main job, updated 0412
# The functions will be coupled to class `Tdata`, they accept an instance
#  of Tdata as data.  This simple the data passing.
def translate_flat_ch_folder(folder=None):
    if not folder:
        return None

    t = Tdata()
    t.folder = folder
    t.filename_list = get_filenames_in_folder(t.folder)
    print t.filename_list
    t.original_video_infos = prepare_original_descp(t.folder, t.filename_list)
    print t.original_video_infos


    # save a pickle before writting file, I lost a few times.
    with open(t.pickle_file, 'wb') as pf:
        pickle.dump(t, pf)

    #translate_video_info_list(t)
    t.write_video_cinfo_file()
    return t
    pass


def continue_translate():
    """ Continue the failed job, get data from pickle file
    """
    # restore data from pickled file
    t = load_t()
    if not t:
        print "Can't load pickled file\n"
        return

    t.filename_list = get_filenames_in_folder(t.folder)
    print t.filename_list
    t.original_video_infos = prepare_original_descp(t.folder, t.filename_list)
    print t.original_video_infos


    # save a pickle before writting file, I lost a few times.
    with open(t.pickle_file, 'wb') as pf:
        pickle.dump(t, pf)

    translate_video_info_list(t, start = t.translating_progress)
    t.write_video_info_file()
    pass


def translate_video_info_list(t, start = 0, nameonly=True):

    total = len(t.original_video_infos)
    if start == 0:
        t.translated_video_infos = []
        t.translating_error = []
        t.translating_progress = 0
    else:
        if len(t.translated_video_infos) > start:
            t.translated_video_infos = t.translated_video_infos[:start]

    for i in range(start, total):
        vi  = t.original_video_infos[i]
        try:
            cvi = translate_vinfo(vi, nameonly=nameonly)
        except Exception, e:
            t.translating_error.append( e )
            t.translating_error.append( "video info number: %i"%i )

        # Not sure the sequence is same as 'original_video_infos'
        t.translated_video_infos.append(cvi)
        t.translating_progress = i
        pickle_t(t)
        time.sleep(1)  # my account has 1k/second limit
    return t.translated_video_infos


def pickle_t(t):
    with open(Tdata.pickle_file, 'wb') as pf:
        pickle.dump(t, pf)


def load_t():
    with open(Tdata.pickle_file, 'rb') as pf:
        t = pickle.load(pf)
        return t


def get_filenames_in_folder( folder = '/home/za/myvid/testc'):
    # not recursive
    fns = os.listdir(folder)
    return fns


def prepare_original_descp(folder, filenames):
    vfile_descriptions = []
    for fn in filenames:
        if is_other_file(fn):
            continue
        if has_description_file(folder, fn):
            descp_lines = gather_description(folder, fn)
        else:
            descp_lines = simple_description(fn)

        vfile_descriptions.append(descp_lines)
        pass
    return vfile_descriptions


def has_description_file(folder, filename):
    dfilename = filename + '.description'
    abs_df = os.path.join(folder, dfilename)
    return os.path.isfile(abs_df)

def is_other_file(filename):
    if not filename:
        return True
    if filename == 'cname':
        return True
    if filename == 'yhb':
        return True
    if filename == 'fyoutube':
        return True
    if re.search(r'\.pl$', filename, re.I):
        return True
    if re.search(r'\.py$', filename, re.I):
        return True
    if re.search(r'\.description$', filename, re.I):
        return True
    return False


def gather_description(folder, video_filename):
    """ gather description for video file 'f', when it has description-file.
    """
    #print video_filename

    lines = []
    # The 1st is the video file name
    lines.append(video_filename)
    # Then the video file name refit to title
    text = refit_filename(video_filename)
    text = gov_check(text)
    lines.append(text)

    dfilename = video_filename + '.description'
    absfn = os.path.join(folder, dfilename)
    with open(absfn, 'rb') as fh:
        des = fh.read()
        des = gov_check(des)
        lines.append(des)
        pass
    return lines


def simple_description(f):
    #print "simeple_description %s \n"%f  # testing
    if not f:
        return []
    lines = []
    lines.append(f)
    text = refit_filename(f)
    text = gov_check(text)
    lines.append(text)
    return lines


def is_description_file(fname):
    if fname.endswith('.description'):
        return True
    return False

def gov_check(text):
    """ Check to avoid angry our gov
    """
    try:
        text, n = re.subn(r'youtube', 'y2-----', text, flags=re.I)
        text, n = re.subn(r'twitter', 'twi----', text, flags=re.I)
        text, n = re.subn(r'facebook', 'fb', text, flags=re.I)
        text, n = re.subn(r'chinese\S+government', 'they', text, flags=re.I)
        text, n = re.subn(r'beijing', 'one city', text, flags=re.I)
        text, n = re.subn(r'communist', 'believer', text, flags=re.I)
        text, n = re.subn(r'\bjzm\b', ' ', text, flags=re.I)
        text, n = re.subn(r'\bxjp\b', ' ', text, flags=re.I)
        text, n = re.subn(r'\bhjt\b', ' ', text, flags=re.I)
        text, n = re.subn(r'\bdxp\b', ' ', text, flags=re.I)
        text, n = re.subn(r'\bwjb\b', ' ', text, flags=re.I)
    except:
        print "TROUBLE GOV CHECK: %s"%text
        # return anyway, do not interupt process
    return text


def refit_filename(name):

    refit = name
    # get rid of filename extension
    refit = re.sub(r'\.\w+$', '', refit)
    '''
    if name.endswith('.webm'):
        refit = name[:-5]
        pass
        '''
    # remove single letter except 'a' 'A'
    refit, n = re.subn(r'\b[b-zB-Z]\b', '', refit)

    refit = refit.replace('00001', '') # autonumbers from youtube-dl
    refit = refit.replace("_39_s", "'s")
    refit = refit.replace('_', ' ')
    refit = refit.replace('.', ' ')

    amp = re.compile(r'\bamp\b', re.I)
    # subn return tuple
    refit = amp.subn(' ', refit)[0]

    quot = re.compile(r'\bquot\b', re.I)
    refit = quot.subn(' ', refit)[0]

    n39 = re.compile(r'\b39\b')
    refit = n39.subn(' ', refit)[0]

    if not refit:
        refit = 'no name'

    return refit


def translate_vinfo(vinfo, nameonly=True):
    """ Translate video information, which in a list 'vinfo'.

    vinfo:  filename, title, description
    return: translated list: filename, chinese title, lang, descriptions
    """
    chinese = []
    lang = 'en'
    if not vinfo:
        return vinfo

    # vinfo[0] is filename, vinfo[1] is refitted filename
    # if nameonly set to True (default), only name get translated.

    if nameonly:
        c, lang = translate_all_length_string(vinfo[1])
        chinese.append(c)
    else:
        for line in vinfo[1:]:
            c, lang = translate_all_length_string(line)
            chinese.append(c)
            pass

    # extend source language description at the end:
    chinese.extend(vinfo[1:])
    # language, after chinese title
    chinese.insert(1, lang)
    # file name, first line:
    chinese.insert(0, vinfo[0])
    # replace in place:
    #vinfo = chinese
    return chinese

def translate_line(line):
    line = line.strip()
    if not line:
        return '', ''

    lang = 'en'
    print "Translating: %s ......\n"%line
    try:
        lang = quick_detect(line)
        if lang:
            c = quick_translate(line, 'zh-CN', lang)
        else:
            c = quick_translate(line, 'zh-CN', 'en')
            pass
    except:
        c = "failed to translate\n"
        pass
    print " get translated ------ : "
    print c
    print "\n" 
    return c, lang

def split_long_line(line):
    if len(line) < 2000:
        return [line,]

    lines = []
    parts = line.split("\n\n")
    for p in parts:
        if len(p) > 1800:
            small_parts = p.split("\n")
            for sp in small_parts:
                lines.append(sp)
        else:
            lines.append(p)
            pass
        pass
    return lines


def translate_all_length_string(gstring):
    language = 'en'
    results = '--'
    if not gstring:
        return results, '??'

    if len(gstring)>2000:
        lines = split_long_line(gstring)

        for line in lines:
            r, lang = translate_line(line)
            results = results + r + ".\n"
            if lang != 'en':
                language = lang
            pass
    else:
        results, language = translate_line(gstring)

    return results, language


'''
def write_video_info_file(folder, filename, infos):
    absfn = os.path.join(folder, filename)
    with codecs.open(absfn, mode='wb', encoding='utf-8') as fh:
        for vinfo in infos:
            for l in vinfo:
                #print l
                # To make sure it's utf-8, this save me 10hrs!!
                if isinstance(l, str):
                    l = l.decode('utf-8')
                fh.write(l)
                fh.write("\n")
            fh.write("\n\n" + vi_delimit + "\n\n")
'''



if __name__ == "__main__":
    print sys.argv[1]
    if not sys.argv[1]:
        print "\n Need a folder to 'gather and translate video infos'\n"
        exit(1)
    folder = sys.argv[1]
    translate_flat_ch_folder(folder)

