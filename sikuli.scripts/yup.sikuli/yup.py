# encoding=utf-8
import os
import os.path
import re
import time
import ConfigParser
import pickle
# to remove directory and files in it, dangerous operation:
import shutil

## For windows, do not end folder name with '/' !
# settings:
base_folder            = 'd:/myvid'
base_folder = os.path.normpath(base_folder)

config_filename       = os.path.normpath('d:/sikuli/robot.cfg')

config = ConfigParser.ConfigParser()
config.read(config_filename)

log_filename           = config.get('basics', 'log_filename')
log_filename           = os.path.join(base_folder, log_filename)


def get_asctime():
    asct = time.asctime()
    #ascta = asct.replace(' ', '_')
    return asct

def writelog(msg=''):
    with open(log_filename, 'a+') as logfile:
        logfile.write ( "\n")
        logfile.write ( get_asctime() )
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
    pass


##### Video File Providor Class

picklefile = os.path.normpath('d:\\tmp\\youku.pfile')
basepath = os.path.normpath('d:\\myvid')

# The file descript videos in one folder
video_info_file_name = 'cname'
# The delimit in the video_info_file_name
vi_delimit = '---goodagood-video-info-delimit---'


class VideoFileProvidor(object):
    def __init__(self, basepath=basepath, picklefile=picklefile):
        self.basepath = os.path.normpath(basepath)
        self.picklefile = os.path.normpath(picklefile)

        self.todo = []
        self.done = []

        self.current_file = None
        self.current_file_state = ''

        ## when deploy, remove the no-video file extension:
        self.video_file_exts = ['flv', 'webm', 'mp4']
        #'text','png','md','html']

        self.delayed_add = 0

        self.add_files()
        pass

    def __str__(self):
        todolen = len(self.todo)
        donelen = len(self.done)

        string = "\nbasepath: %s\n"%self.basepath
        string += "current file: %s\n"% self.current_file
        string += "current file state: %s\n"% self.current_file_state
        string += "todo file list: total %s\n"% todolen
        if todolen > 3:
            string += "0, : %s \n"%self.todo[0]
            string += "1, : %s \n"%self.todo[1]
            string += "...... total %s\n"% todolen
            string += "%i, : %s \n"%(todolen-1, self.todo[todolen-1])
        else:
            for f in self.todo:
                string += " : %s \n"%f

        string += "done file list: total %i files.\n"% donelen
        if donelen > 3:
            string += "0, : %s \n"%self.done[0]
            string += "1, : %s \n"%self.done[1]
            string += "...... total %s\n"% donelen
            string += "%i, : %s \n"%(donelen-1, self.done[donelen-1])
        else:
            for f in self.done:
                string += " : %s \n"%f

        return string


    def change_basepath(self, newbase):
        if self.basepath == newbase:
            return False
        if os.path.isdir(newbase):
            self.basepath = newbase
            self.add_files()
            self.check_file_list()
            return True
        return False


    def delayed_adding_check(self):
        self.delayed_add += 1
        if self.delayed_add == 8:
            self.add_files()
            self.check_file_list()
            self.delayed_add = 0


    def is_video_file(self, filename):
        if not filename:
            return False
        for ext in self.video_file_exts:
            if filename.lower().endswith(ext):
                return True

        return False


    def make_all_file_list(self):
        all_file_list  = set(self.todo + self.done)
        all_file_list  = list(all_file_list)
        return all_file_list


    def add_files(self):
        all_file_list = self.make_all_file_list()
        new_file_list = []
        for (path, dirs, files) in os.walk(self.basepath):
            for f in files:
                fullfilename = os.path.join(path, f)
                if all_file_list.count(fullfilename):
                    # the file already in the lists, jump to next
                    continue
                else:
                    if self.is_video_file(fullfilename):
                        new_file_list.append( fullfilename )

        self.todo.extend(new_file_list)

        if not self.current_file:
            self.pop_one_full_filename()

        self.pickle_self()  #?
        pass

    def check_file_list(self):
        # remove duplication from self.todo
        self.todo = list( set(self.todo))

        to_remove = []
        for f in self.todo:
            if not os.path.isfile(f):
                to_remove.append(f)
                pass
            pass
        for f in to_remove:
            self.todo.remove(f)
            pass

        for f in self.done:
            if not os.path.isfile(f):
                to_remove.append(f)
                pass
            pass
        for f in to_remove:
            self.done.remove(f)
            pass

        self.add_files()



    def pickle_self(self):
        with open(self.picklefile, 'wb') as pf:
            pickle.dump(self, pf)
            #writelog("WRITE PICKLE FILE")
            pass
        pass


    # Another way is to report in fail, but actually, 
    # we can't report when dead.  So, no report, no done.
    # This can also be used to remove a file from todo list.
    def report_job_done(self, vfile = None):
        if  vfile is None:
            self.current_file_state = 'ok'
        else:
            self.done.append(vfile)
            try:
                self.todo.remove(vfile)
            except:
                return "It isn't in todo list: %s"%vfile
            pass
        self.pickle_self()
        return 'ok'


    def redo_file(self, vfile = None):
        """Put the file back into todo list.

        This is needed especially in testing.
        """
        if  vfile is None:
            self.current_file_state = None
        else:
            self.todo.insert(0,vfile)
            try:
                self.done.remove(vfile)
            except:
                return "It isn't in done list: %s"%vfile
            pass

        self.pickle_self()
        return 'ok'


    def drop_current_file(self):
        # falsely report job done:
        self.report_job_done()
        # then pop another file out:
        self.pop_one_full_filename()


    def pop_one_full_filename(self):
        if self.current_file :
            if self.current_file_state == 'ok':
                self.done.append(self.current_file)
            else:
                self.todo.append(self.current_file)

        self.current_file_state = None

        one = self.todo.pop(0)
        self.current_file = one

        self.pickle_self()
        self.delayed_adding_check()
        return one


    def clear_one_folder(self, folder='/tmp/'):
        """Clear all files from the folder from self.todo list.
        """
        to_remove = []
        for f in self.todo:
            if self.is_in_folder(f, folder):
                to_remove.append(f)

        for f in to_remove:
            self.todo.remove(f)
        self.pickle_self()


    def is_in_folder(self, filename, folder='/tmp/'):
        fn = os.path.normpath(filename)
        fd = os.path.normpath(folder)
        commonprefix = os.path.commonprefix([fn, fd])
        if commonprefix == fd:
            sufix_part = fn.replace(fd, '')
            sufix_part = sufix_part.lstrip('/')
            new_file_name = os.path.join(fd, sufix_part)
            if new_file_name == fn:
                return True
            pass
        return False



    ## 
    def get_video_info(self, fullfilename=None):
        #
        """
        specification: file: cname, '---goodagood-video-info-delimit---'
        """
        if fullfilename is None:
            fullfilename = self.current_file
        # the fullfilename is the video's filename
        video_info_file = self._find_info_file(fullfilename)
        #print "video_info_file: %s \n"%video_info_file
        #print self.read_chinese_title(video_info_file, fullfilename)
        if not video_info_file:
            return None

        vi_title, vi_lang, vi_desc = self.read_chinese_title(
                    video_info_file, fullfilename)

        vi_title = self.prefix_lang(vi_title, vi_lang)
        return vi_title, vi_lang, vi_desc


    def prefix_lang(self, title, lang):
        if lang.count('en'):
            title = "英- " + title
        elif lang.count('fr'):
            title = "法- " + title
        elif lang.count('es'):
            title = "西- " + title
        elif lang.count('pl'):
            title = "波- " + title
        elif lang.count('it'):
            title = "意- " + title
        elif lang.count('pt'):
            title = "葡- " + title
        elif lang.count('ja'):
            title = "日- " + title
        elif lang.count('de'):
            title = "德- " + title
        elif lang.count('ko'):
            title = "韩- " + title
        elif lang.count('ar'):
            title = "阿- " + title
        elif lang.count('sv'):
            title = "瑞- " + title
        elif lang.count('el'):
            title = "希- " + title
        else:
            title = lang + '- ' + title
            
        return title


    def _find_info_file(self, fullfilename):
        path, filename = os.path.split(fullfilename)
        cname_file = os.path.join(path, video_info_file_name)
        if os.path.isfile(cname_file):
            return cname_file
        else:
            return None
        pass


    ## get video description of the video from file video_info_file_name
    # -The format of the file 'info_filename' ('cname')is: 
    #      first line of file name, 
    #      followed by a line of Chinese title, 
    #      followed by lines of Chinese description, English description
    #      and delimit will in separate line.
    ##
    def read_chinese_title(self, info_filename, abs_vfn):
        """read chinese title from 'info_filename' file.

        info_filename : the file contains chinese title for each video file.
        abs_vfn : abs video filename
        """
        with open(info_filename, 'rb') as afile:
            file2str = afile.read()
            pass
        if not file2str:
            return None

        vfn = os.path.basename(abs_vfn)

        start = file2str.find(vfn)
        rest  = file2str[start:]
        end   = rest.find(vi_delimit)
        info  = rest[:end]
        info  = info.strip()

        lines = info.splitlines()
        #print "%i lines : %s \n"%(len(lines), "\n".join(lines))
        # filter out empty lines:
        no_empty_lines = filter( lambda x: x.strip(), lines)

        #filename = no_empty_lines[0]
        if len(no_empty_lines)>2:
            ctitle   = no_empty_lines[1]
        else:
            ctitle = abs_vfn

        if len(no_empty_lines)>3:
            lang = no_empty_lines[2]
        else:
            lang = 'unknown lang'

        if len(no_empty_lines)>3:
            description = "\n".join(no_empty_lines[2:])
        else:
            description = ctitle

        return ctitle, lang, description



def get_file_provider(basepath = basepath, picklefile = picklefile):
    if os.path.isfile(picklefile):
        with open(picklefile, 'rb')as f:
            fileprovider = pickle.load(f)
            if fileprovider.basepath != basepath:
                fileprovider.change_basepath(basepath)
            fileprovider.check_file_list()
        pass
    else:
        #writelog("NO PICKLE FILE")
        fileprovider = VideoFileProvidor()
        fileprovider.add_files()
        pass

    return fileprovider


def set_working_log(section='working_log', name='wlogging', content=''):
    config.set(section, name, content)

def write_working_log():
    with open(config_filename, 'wb') as conffile:
        config.write(conffile)
    pass


## reused: ??Stop using 'cname_file', this file contains file name and Chinese title
#  pairs.  It would be easy to put this file inside the same folder of the
#  video files.  
# -Make it a hard specification to name the file as 'cname', and put inside
#  the folder of video files.
# -It would be more convinient to write a working file 'cname.todo', it
#  will contain the _todo_ things. 
# -Remove the video file after uploading, this will save a lot trivial manual
#  jobs, and free disk space for more file uploading.
##



def appendlog(fullfilename, msg=''):
    with open(fullfilename, 'a+') as logfile:
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
    pass



def stop_signal_comes():
    stop = config.getint('basics', 'stop_at')
    if stop == 1:
        return True

    if stop == 0:
        return False
    else:
        stop = stop -1
        config.set('basics', 'stop_at', str(stop))
        write_working_log()

    return False


def mocking(message='', duration=1, raise_exception=False):
    popup( "I am mocking...%s"%message )
    if raise_exception:
        raise Exception(message)
    time.sleep(duration)



def need_waiting():
    if not exists("yk_interface_low_space.png"): #not enough space, it's too many
        return True

    return False


def upload_one_file(fullfilename, ctitle, description):
    if exists("addfile.png"):
        click("addfile.png")
        wait(1)
    else:
        exit(11)
        pass    
    click("1365905328239.png")
    wait(1)
    
    type(fullfilename)
    type(Key.ENTER)
    wait(1)

    click(Pattern("title_input.png").targetOffset(40,0))
    type('a', KeyModifier.CTRL)
    type(Key.BACKSPACE)
    paste(ctitle)
    wait(1)

    click(Pattern("description_input.png").targetOffset(40,0))
    paste(description)

    click(Pattern("tag_inputy.png").targetOffset(10,0))
    type('goodagood')

    click("edu_caty.png")
    click("icopiedy.png")
    click("start_buttony.png")

    return 'finished'


def check_interface_yk():
    pass


def one_video_for_youku(filename, fullfilename, title, long_cname):
    while need_waiting():
        check_interface_yk()
        time.sleep(5)

    if len(title)>60:
        title = title[:58]
    try:
        upload_one_file(fullfilename, title,long_cname)
    except Exception, ex:

        logmsg = "exception in uploading file: %s\nwith long_cname: %s \n"%(fullfilename, long_cname)
        logmsg = logmsg + "\n" + ex.message
        writelog( logmsg)

    logmsg = "fullfilename: \n" + fullfilename + "\ncname: " + title
    writelog( logmsg)

    pass


# 0412, with new file providor.
def upload_loop_01():
    fp = get_file_provider()
    #print fp

    # pop a new file anyway, the old one append to 'todo'/'done' according to
    # 'current_file_state', this would be good in testing.
    fullfilename = fp.pop_one_full_filename()

    title,lang,description = fp.get_video_info(fullfilename)
    filename = os.path.basename(fullfilename)
    while fullfilename:

        #popup( fullfilename + "  " + cname)
        one_video_for_youku(filename, fullfilename, title, description)
        #writelog(fp.__str__()) ##testing

        fp.report_job_done()
        fullfilename = fp.pop_one_full_filename()
        title,lang,description = fp.get_video_info(fullfilename)
        filename = os.path.basename(fullfilename)

        #writelog(fp.__str__()) ##testing

        if stop_signal_comes():
            print "STOP SIGNAL COMES"
            exit(0)



##########################
### tests:
### comment out after testing:

'''
fp = get_file_provider()
fp.report_job_done()
fp.pop_one_full_filename()

writelog( "fp.current_file" )
writelog( fp.current_file )
fp.report_job_done()
writelog( "fp.current_file" )
writelog( fp.current_file )

fp.report_job_done('d:\\myvid\\msbasics\\Windows_Live_Movie_Maker_Tutorial_-_Part_1.mp4')
writelog( "fp.current_file" )
writelog( fp.current_file )

ffn = fp.pop_one_full_filename()
writelog( "fp.current_file" )
writelog( fp.current_file )

vit, vil, vid = fp.get_video_info(ffn)
writelog( "video info title" )
writelog( vit )
writelog( "video info lang" )
writelog( vil )
writelog( "video info description" )
writelog( vid )

writelog( "fp.__str__()")
writelog( fp.__str__())

fp.report_job_done('d:\\myvid\\msbasics\\1_9_Computer_hardware_basics.flv')
writelog( "fp.__str__()")
writelog( fp.__str__())
'''


### do the job:



upload_loop_01()
