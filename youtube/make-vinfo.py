#!/usr/bin/python
# encoding=utf-8
import os
import os.path
import re
import sys

import codecs

#import gtrans  # google translate tool
from gtrans import quick_translate, quick_detect

folder = '/home/za/myvid/testc'

video_info_file_name = 'cname'

vi_delimit = '---goodagood-video-info-delimit---'

def gather_n_translate_video_info(folder=None):
    if not folder:
        return None
    fns = get_filenames_in_folder(folder)
    video_infos = gether_vinfo(folder, fns)
    write_video_info_file(folder, video_info_file_name, video_infos)
    pass


def get_filenames_in_folder( folder = '/home/za/myvid/testc'):
    fns = os.listdir(folder)
    return fns


def gether_vinfo(folder, fns):
    """
    fns : a list of filenames
    """
    description_files = filter(is_description_file, fns)

    for f in description_files:
        fns.remove(f)
        pass

    #f_has_no_description = filter(has_no_description, fns)
    f_has_no_description = filter(
            lambda x: x+'.description' not in description_files, fns)

    # 'cname' is the file name I write
    if 'cname' in f_has_no_description:
        f_has_no_description.remove('cname')

    #print "\n".join(description_files)
    #print "\n".join(f_has_no_description)

    vinfos = []
    for f in description_files:
        lines = gether_description(folder, f)
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

def gether_description(folder, f):
    #print f
    video_filename = f.replace('.description', '')

    lines = []
    lines.append(video_filename)
    lines.append(refit_filename(video_filename))

    absfn = os.path.join(folder, f)
    with open(absfn, 'rb') as fh:
        des = fh.read()
        des = gov_check(des)
        lines.append(des)
        pass
    return lines


def simple_description(f):
    lines = [f,]
    text = refit_filename(f)
    text = gov_check(text)
    lines.append(refit_filename(f))
    return lines


def is_description_file(fname):
    if fname.endswith('.description'):
        return True
    return False

def gov_check(text):
    """ Check to avoid angry our gov
    """
    text, n = re.subn(r'youtube', 'y2', text, flags=re.I)
    text, n = re.subn(r'twitter', 't------', text, flags=re.I)
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
    for line in vinfo[1:]:
        lang = quick_detect(line)
        c = ''
        if lang:
            c = quick_translate(line, 'zh-CN', lang)
        else:
            c = quick_translate(line, 'zh-CN', 'en')
            pass
        #print c
        chinese.append(c)
        pass
    # extend source language at the end:
    chinese.extend(vinfo[1:])
    # language, after chinese title
    chinese.insert(1, lang)
    # file name, first line:
    chinese.insert(0, vinfo[0])
    # replace in place:
    vinfo = chinese
    return chinese

def write_video_info_file(folder, filename, infos):
    absfn = os.path.join(folder, filename)
    with codecs.open(absfn, mode='w+', encoding='utf-8') as fh:
        for vinfo in infos:
            fh.write("\n".join(vinfo))
            fh.write("\n\n" + vi_delimit + "\n\n")

    pass

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
    print sys.argv[1]
    if not sys.argv[1]:
        print "\n Need a folder to 'gather and translate video infos'\n"
        exit(1)
    folder = sys.argv[1]
    gather_n_translate_video_info(folder)
    vf_name = os.path.join(folder, video_info_file_name)
    print "\n video info file: %s \n"%vf_name


    """
    ###
    fs = get_filenames_in_folder()
    print "\n".join(fs)

    vv = gether_vinfo(folder, fs)
    print "\n\n"
    for v in vv:
        print "\n"
        for l in v:
            print l

    print gether_description('/home/za/myvid/testc',
        "visual_c_and_serial_port_for_embedded_uart.flv.description")

    #visual_c_and_serial_port_for_embedded_uart.flv
    #visual_c_and_serial_port_for_embedded_uart.flv.description
    #visual_C_window_form.flv
    #visual_C_window_form.flv.description
    #visual_studio_10_full_y_programe_en_c.mp4
    #visual_studio_10_full_y_programe_en_c.mp4.description

    #print simple_description(fs[1])

    print sys.argv[1:]

    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = '/home/za/myvid/testc'


    make_cname_file(folder)


    #print refit_filename('fjdk quot fjdkl quot amp 39 399 quott')

    '''
    with codecs.open('/tmp/aafutf', mode='w+', encoding='utf-8') as f:
        f.write(u'阿飞点卡 ASDF')
        '''
    """
