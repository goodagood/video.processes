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

folder = '/home/za/myvid/testc'
folder = '/mnt/cc/testc'

video_info_file_name = 'cname'

vi_delimit = '---goodagood-video-info-delimit---'

# file writting might fail, before write it to file, pickle the translated
g_translate_pfile = '/tmp/pickle-make-vinfos'


class Tdata(object):
    folder = '/home/za/myvid/testc'
    folder = '/mnt/cc/testc'

    video_info_file_name = 'cname'

    vi_delimit = '---goodagood-video-info-delimit---'

    # file writting might fail, before write it to file, pickle the translated
    pickle_file = '/tmp/pickle-make-vinfos'


    files = []


# Do the main job.
def gather_n_translate_video_info(folder=None):
    if not folder:
        return None
    fns = get_filenames_in_folder(folder)
    video_infos = gather_vinfo(folder, fns)

    # save a pickle before writting file, I lost a few times.
    with open(g_translate_pfile, 'wb') as pf:
        pickle.dump(video_infos, pf)

    write_video_info_file(folder, video_info_file_name, video_infos)
    pass


# Do the main job, updated 0412
def translate_flat_folder(folder=None):
    if not folder:
        return None

    # restore data from pickled file

    t = Tdata
    t.filename_list = get_filenames_in_folder(folder)
    t.original_video_infos = prepare_original_descp(folder, t.filename_list)


    # save a pickle before writting file, I lost a few times.
    with open(t.pickle_file, 'wb') as pf:
        pickle.dump(t, pf)

    #write_video_info_file(folder, video_info_file_name, video_infos)
    pass


def get_filenames_in_folder( folder = '/home/za/myvid/testc'):
    # not recursive
    fns = os.listdir(folder)
    return fns


def gather_vinfo(folder, fns):
    """
    fns : a list of filenames
    """
    description_files = filter(is_description_file, fns)

    for f in description_files:
        fns.remove(f)
        pass

    #f_has_no_description : file has no descriptions
    f_has_no_description = filter(
            lambda x: x+'.description' not in description_files, fns)

    # 'cname' is the file name I write
    if 'cname' in f_has_no_description:
        f_has_no_description.remove('cname')

    #print "\n".join(description_files)
    #print "\n".join(f_has_no_description)

    vinfos = []
    for f in description_files:
        lines = gather_description(folder, f)
        vinfos.append(lines)
        pass

    for f in f_has_no_description:
        lines = simple_description(f)
        vinfos.append(lines)
        pass

    cvinfos = []
    for vi in vinfos:
        cvi = translate_vinfo(vi)
        cvinfos.append(cvi)
    return cvinfos


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


def gather_description(folder, f):
    #print f
    video_filename = f.replace('.description', '')

    lines = []
    # The 1st is the video file name
    lines.append(video_filename)
    # Then the video file name refit to title
    text = refit_filename(video_filename)
    text = gov_check(text)
    lines.append(text)

    absfn = os.path.join(folder, f)
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
    text, n = re.subn(r'youtube', 'the biggest video website', text, flags=re.I)
    text, n = re.subn(r'twitter', 'the micro blog creator', text, flags=re.I)
    text, n = re.subn(r'facebook', 'one friendship website', text, flags=re.I)
    text, n = re.subn(r'chinese\S+government', 'they', text, flags=re.I)
    text, n = re.subn(r'beijing', 'one city', text, flags=re.I)
    text, n = re.subn(r'communist', 'believer', text, flags=re.I)
    text, n = re.subn(r'\bjzm\b', '', text, flags=re.I)
    text, n = re.subn(r'\bxjp\b', '', text, flags=re.I)
    text, n = re.subn(r'\bhjt\b', '', text, flags=re.I)
    text, n = re.subn(r'\bdxp\b', '', text, flags=re.I)
    text, n = re.subn(r'\bwjb\b', '', text, flags=re.I)
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


def translate_vinfo(vinfo):
    chinese = []
    lang = 'en'
    if not vinfo:
        return vinfo
    for line in vinfo[1:]:
        c, lang = translate_all_length_string(line)
        chinese.append(c)
        
        '''
        if not c:
            time.sleep(8)
            '''
        pass
    # extend source language description at the end:
    chinese.extend(vinfo[1:])
    # language, after chinese title
    chinese.insert(1, lang)
    # file name, first line:
    chinese.insert(0, vinfo[0])
    # replace in place:
    vinfo = chinese
    return chinese

def translate_line(line):
    line = line.strip()
    if not line:
        return ''

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
    return c, lang

def split_long_line(line):
    if len(line) < 2000:
        return

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



if __name__ == "xx__main__":
    print sys.argv[1]
    if not sys.argv[1]:
        print "\n Need a folder to 'gather and translate video infos'\n"
        exit(1)
    folder = sys.argv[1]
    translate_flat_folder(folder)

    ''' version before 0412
    gather_n_translate_video_info(folder)
    vf_name = os.path.join(folder, video_info_file_name)
    print "\n video info file: %s \n"%vf_name
    '''


    """
    ###
    fs = get_filenames_in_folder()
    print "\n".join(fs)

    vv = gather_vinfo(folder, fs)
    print "\n\n"
    for v in vv:
        print "\n"
        for l in v:
            print l

    print gather_description('/home/za/myvid/testc',
        "visual_c_and_serial_port_for_embedded_uart.flv.description")

    #visual_studio_10_full_y_programe_en_c.mp4
    #visual_studio_10_full_y_programe_en_c.mp4.description

    #print simple_description(fs[1])

    print sys.argv[1:]

    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = '/home/za/myvid/testc'





    """
