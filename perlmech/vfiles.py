import os
import shelve
import pickle

picklefile = '/tmp/pfile'
shelvefile = '/tmp/shelvea/aa'
path = "/home/za/tmp/wiki-markdoc"

class VideoFileProvidor(object):
    def __init__(self, basepath=path, sfile='/tmp/shelvea/aa'):
        self.basepath = basepath
        self.shelvepath = sfile

        self.todo = []
        self.done = []

        self.current_file = None
        self.current_file_state = ''

        self.video_file_exts = ['flv', 'webm', 'mp4',
            'text','png','md','html']

        # to deprecate
        # large enough to hold many files names
        self.max = 38388

        #self.add_files()
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
            string += "%i, : %s \n"%(todolen, self.todo[todolen-1])
        else:
            for f in self.todo:
                string += " : %s \n"%f

        string += "done file list: total %i files.\n"% donelen
        if donelen > 3:
            string += "0, : %s \n"%self.done[0]
            string += "1, : %s \n"%self.done[1]
            string += "...... total %s\n"% donelen
            string += "%i, : %s \n"%(donelen, self.done[donelen-1])
        else:
            for f in self.done:
                string += " : %s \n"%f

        return string


    def is_video_file(self, filename):
        for ext in self.video_file_exts:
            if filename.lower().endswith(ext):
                return True

        return False


    # deprecated, 0407
    def rm_all_finished(self):
        length = len(self.done)
        for i in range(length):
            f = self.done.pop(0)
            #os.remove(f)
            print "os.remove(%s) \n"%f
        self.all_file_list  = self.update_all_list()


    # deprecated, 0407
    def rm_half_finished(self):
        half = len(self.done)/2
        for i in range(half):
            f = self.done.pop(0)
            #os.remove(f)
            print "os.remove(%s) \n"%f
        self.all_file_list  = self.update_all_list()


    # deprecated, 0407
    def keep_size(self):
        if len(self.done) > self.max :
            self.rm_half_finished()
            pass
        if len(self.todo) < (self.max/2) :
            self.add_files()
            pass
        self.all_file_list  = self.update_all_list()
        self.pickle_self()
        pass


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
        self.pickle_self()  #?
        pass

    def check_file_list(self):
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

        self.add_files(self)



    def pickle_self(self):
        with open(picklefile, 'wb') as pf:
            pickle.dump(self, pf)
            pass
        pass


    #deprecated 0407
    def _get_from_shelve(self, name=None):
        if not name:
            return None
        with shelve.open(self.shelvepath) as she:
            return she['name']

        return None


    #deprecated 0407
    def _update_shelve(self, name, value):
        if not name:
            return None
        with shelve.open(self.shelvepath) as she:
            she['name'] = value


    #deprecated 0407
    def get_one_full_filename(self):
        one = self.todo.pop(0)
        self.done.append(one)
        self.keep_size()
        return one


    def report_job_done(self):
        self.current_file_state = 'ok'


    def pop_one_full_filename(self):
        if self.current_file_state == 'ok':
            self.done.append(self.current_file)
        else:
            self.todo.append(self.current_file)

        self.current_file_state = None

        one = self.todo.pop(0)
        self.current_file = one

        self.pickle_self()
        return one



def get_file_provider(picklefile = picklefile):
    if os.path.isfile(picklefile):
        with open(picklefile)as f:
            fileprovider = pickle.load(f)
            fileprovider.check_file_list()
            #fileprovider.rm_all_finished()
        pass
    else:
        fileprovider = VideoFileProvidor()
        #fileprovider.add_files()
        pass

    return fileprovider


if __name__ == '__main__':
    fp = get_file_provider()
    print fp

    '''
    fp.add_files()
    print fp

    if fp.todo:
        fp.pickle_self()
    for f in fp.todo:
        print f
    pass
    '''
