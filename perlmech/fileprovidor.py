import os
import shelve
import pickle

picklefile = '/tmp/pfile'
basepath = "/home/za/tmp/wiki-markdoc"
basepath = "/tmp/vt"  #testing

# The file descript videos in one folder
video_info_file_name = 'cname'
# The delimit in the video_info_file_name
vi_delimit = '---goodagood-video-info-delimit---'

class VideoFileProvidor(object):
    def __init__(self, basepath=basepath, picklefile=picklefile):
        self.basepath = basepath
        self.picklefile = picklefile

        self.todo = []
        self.done = []

        self.current_file = None
        self.current_file_state = ''

        ## when deploy, remove the no-video file extension:
        self.video_file_exts = ['flv', 'webm', 'mp4',
            'text','png','md','html']

        self.add_files()
        pass

    def __str__(self):
        todolen = len(self.todo)
        donelen = len(self.done)

        string = "\nbasepath: %s\n"%self.basepath
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
        with open(picklefile, 'wb') as pf:
            pickle.dump(self, pf)
            pass
        pass


    # Another way is to report in fail, but actually, 
    # we can't report when dead.  So, no report, no done.
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
        pass


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
    def get_video_info(self, fullfilename):
        #
        """
        specification: file: cname, '---goodagood-video-info-delimit---'
        """
        # the fullfilename is the video's filename
        video_info_file = self._find_info_file(fullfilename)
        #print "video_info_file: %s \n"%video_info_file
        #print self.read_chinese_title(video_info_file, fullfilename)
        return self.read_chinese_title(video_info_file, fullfilename)

        #todo
        pass

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
        with open(picklefile)as f:
            fileprovider = pickle.load(f)
            if fileprovider.basepath != basepath:
                fileprovider.change_basepath(basepath)
            fileprovider.check_file_list()
        pass
    else:
        fileprovider = VideoFileProvidor()
        pass

    return fileprovider



fp = get_file_provider()
#print fp
#print fp.is_in_folder('/tmp/aac', '/tmp/')
fnb = fp.pop_one_full_filename()
vinfo = fp.get_video_info(fnb)

'''
if __name__ == '__main__':
    fp = get_file_provider()
    print fp


    fp.add_files()
    print fp

    if fp.todo:
        fp.pickle_self()
    for f in fp.todo:
        print f
    pass
    '''
