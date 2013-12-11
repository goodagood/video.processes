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

picklefile = os.path.normpath('d:\\tmp\\pfile')
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
                if new_file_list.count(fullfilename):
                    # in the new file lists, jump to next
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

        # remove duplicated in todo list:
        self.todo = list( set(self.todo))




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


    def check_current_file(self):
        if not os.path.isfile(self.current_file):
            self.drop_current_file()


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
        pass
    else:
        #writelog("NO PICKLE FILE")
        fileprovider = VideoFileProvidor()
        pass

    fileprovider.add_files()
    fileprovider.check_file_list()
    fileprovider.check_current_file()

    return fileprovider


####### End of videofileprovidor class


class TolerateCounter(object):
    def __init__(self, threshold = 8):
        self.threshold = threshold
        self.count = 0
        pass

    def under_tolerate(self):
        if self.count > self.threshold:
            self.count = 0
            return False
        self.count += 1
        return True


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


def set_working_log(section='working_log', name='wlogging', content=''):
    config.set(section, name, content)


def write_working_log():
    with open(config_filename, 'wb') as conffile:
        config.write(conffile)
    pass


def appendlog(fullfilename, msg=''):
    with open(fullfilename, 'a+') as logfile:
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
    pass


#def is_over3_and_check_fails():
def check_fails():
    # there are 2 bypa  job, the last is  named job according the name.
    while exists(Pattern("failed_offset_on_redo.png").similar(0.99).targetOffset(52,-1)):
        #The following will redo the fails
        #click(Pattern("1364905880031.png").similar(0.91).targetOffset(52,-1))
        click(Pattern("failed_offset_on_cancel.png").similar(0.98).targetOffset(92,-1))
        wait(5)

        if exists("blue_ok_cancle.png"):
            click("blue_ok_cancle.png")
        pass

    while exists("reloaded_56.png"): #56ican reload and lost
        click("reloaded_56.png")


def too_many_uploading():
    if easy_clean_check_pass():
        return False

    if not exists("bottom_space.png"): #not enough low space, it's too many
        return True

    if exists(Pattern("three_uploads.png").similar(0.86)):
        return True

    if not exists("empty_low_right.png"): #not enough lr space, it's too many
        return True

    return False


def enter_filename(fullfilename):
    wait("filename_input.png", 18)
    click("filename_input.png")
    type(fullfilename)
    type(Key.ENTER)
    wait(2)

    #this means error, clear the window and return False, by click 'cancel'
    if exists(Pattern("cancel_file_input.png").exact()):
        click(Pattern("cancel_file_input.png").exact())
        wait(2)
        return False
    return True

def enter_video_name(name='name'):
    if exists(Pattern("above_title_input.png").targetOffset(0,35)):
        click(Pattern("above_title_input.png").targetOffset(0,35))
        type('a', KeyModifier.CTRL)
        type(Key.BACKSPACE)
        paste(name)


def upload_one_file(fullfilename, filename, cname, long_cname=''):
    # start to upload new file, click 'select file':
    if exists("select_filea.png"):
        click("select_filea.png")
        wait(1)
        pass
    elif exists("middle_select_file.png"):
        click("middle_select_file.png")
        wait(1)
        pass
    else:
        exit(11)
        pass

    if not enter_filename(fullfilename):
        return False

    # click the last one of 'enter information':
    if exists(Pattern("fresh_appeared_add_info.png").similar(0.80).targetOffset(-5,-27)):
        click(Pattern("fresh_appeared_add_info.png").similar(0.80).targetOffset(-5,-27))
    else:
        return "missed enter info input"  #do nothing more, failed this one.

    wait("tag_input.png", 8)
    if exists("tag_input.png"):
        click("tag_input.png")
        type('goodagood')

    if exists("intro_input.png"):
        click("intro_input.png")
        paste(long_cname)
        pass

    if exists("edu_vtag.png"):
        click("edu_vtag.png")
        wait(1)
        pass

    enter_video_name(cname)
    #save
    if exists(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35)):
        click(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35))

    #wait(2) ## a few times failed, change to 2
    #check_save()
    return 'finished'

def check_gray_save():
    ## check again:
    if exists(Pattern("gray_save.png").similar(0.80)):
        if exists("vcat_missing.png"):
            click(Pattern("F2iiziIEEQH1.png").targetOffset(-79,-33))

        if exists("tag_missing.png"):
            click("tag_3.png")
            type('goodagood')
            pass

        click(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35))


def check_save():
    ## check again:
    if exists(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35)):
        if exists("vcat_missing.png"):
            click(Pattern("F2iiziIEEQH1.png").targetOffset(-79,-33))

        if exists("tag_missing.png"):
            click("tag_3.png")
            type('goodagood')
            pass

        click(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35))
        pass

def check_auto_comeup_missing_info_dialog():
    ## some missing info, the dialog will comeup again after uploading:
    if exists(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35)):

        click("tag_input.png")
        type('goodagood')

        if exists("edu_vtag.png"):
            click("edu_vtag.png")
            wait(1)
            pass
        click(Pattern("on_blue_save.png").similar(0.88).targetOffset(95,35))
        wait(1)
        check_save()


def close_finished():
    ''' This will popup gray save
    if exists("empty_finished.png"):
        click("empty_finished.png")
        wait(3)
        return
    '''

    while(exists(Pattern("finished_video_on_cross.png").similar(0.95).targetOffset(213,1))):
        click(Pattern("finished_video_on_cross.png").similar(0.94).targetOffset(213,1))
        wait(3)



def mocking(message='', duration=1, raise_exception=False):
    popup( "I am mocking...%s"%message )
    if raise_exception:
        raise Exception(message)
    time.sleep(duration)


def easy_clean_check_pass():
    """ Return True if enough space on 56ican interface.

    An easy way to know it's ok to add another video.
    """
    #if exists(Pattern("enough_space.png").similar(1.00)):

    if exists(Pattern("enough_space_right.png").exact()):
        
        return True
    else:
        return False

def check_waiting_info_2finished():
    if exists(Pattern("up_finished_waiting.png").exact()):
        click(Pattern("up_finished_waiting.png").exact())
        

def clean_56ican():
    if easy_clean_check_pass():
        return
    close_finished()
    check_gray_save()
    if easy_clean_check_pass():
        return
    check_auto_comeup_missing_info_dialog()
    check_save()
    check_fails()
    check_waiting_info_2finished()
    pass


def try_56ican(filename, fullfilename, title, description):
    try:
        upload_one_file(fullfilename, filename, title,description)
        logmsg = "fullfilename: %s \n title: %s\n" %(fullfilename, title)
        writelog( logmsg)
    except Exception, ex:
        logmsg = "exception in uploading file: %s\nwith description: %s \n"%(fullfilename, description)
        logmsg = logmsg + "\n" + ex.message
        writelog( logmsg)
    except:
        type, value, traceback = sys.exc_info()
        logmsg = str(type) + "\n" + str(value) + "\n" + str(traceback) + "\n"
        writelog( logmsg)

    while too_many_uploading():
        time.sleep(5)
        try:
            clean_56ican()
        except Exception, ex:
            logmsg = "exception in clean after file: %s\nwith description: %s \n"%(fullfilename, description)
            logmsg = logmsg + "\n" + ex.message
            writelog( logmsg)
        except:
            type, value, traceback = sys.exc_info()
            logmsg = str(type) + "\n" + str(value) + "\n" + str(traceback) + "\n"
            writelog( logmsg)


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
        try_56ican(filename, fullfilename, title, description)
        number_todo = len(fp.todo)
        writelog( "number of file to upload: %s"%(str(number_todo)))
        fp.report_job_done()

        if stop_signal_comes():
            print "STOP SIGNAL COMES"
            exit(0)

        fullfilename = fp.pop_one_full_filename()
        title,lang,description = fp.get_video_info(fullfilename)
        # I want to check the number of todo:
        description = "(%s) "%(str(number_todo))  + description
        filename = os.path.basename(fullfilename)



### do the job:

upload_loop_01()


##########################
### tests:
### comment out after testing:


