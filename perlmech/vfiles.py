import os
import pickle

picklefile = '/tmp/pfile'
path = "/home/za/tmp"

class Bufof30(object):
    def __init__(self):
        self.basepath = path
        self.todo = []
        self.done = []
        self.all  = self.update_all_list()

        self.max = 30
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


    def rm_all_finished(self):
        length = len(self.done)
        for i in range(length):
            f = self.done.pop(0)
            #os.remove(f)
            print "os.remove(%s) \n"%f
        self.all  = self.update_all_list()


    def rm_half_finished(self):
        half = len(self.done)/2
        for i in range(half):
            f = self.done.pop(0)
            #os.remove(f)
            print "os.remove(%s) \n"%f
        self.all  = self.update_all_list()


    def keep_size(self):
        if len(self.done) > self.max :
            self.rm_half_finished()
            pass
        if len(self.todo) < (self.max/2) :
            self.add_files()
            pass
        self.all  = self.update_all_list()
        self.pickle_self()
        pass


    def update_all_list(self):
        self.all  = set(self.todo + self.done)
        self.all  = list(self.all)
        return self.all


    def add_files(self):
        for (path, dirs, files) in os.walk(self.basepath):
            for f in files:
                if len(self.todo) < self.max:
                    fullfilename = os.path.join(path, f)
                    if self.all.count(fullfilename):
                        # the file already in the lists, jump to next
                        continue
                    else:
                        self.todo.append( fullfilename )
                else:
                    return
        self.all  = self.update_all_list()
        self.pickle_self()
        pass

    def pickle_self(self):
        with open(picklefile, 'wb') as pf:
            pickle.dump(self, pf)
            pass
        pass

    def get_one_full_filename(self):
        one = self.todo.pop(0)
        self.done.append(one)
        self.keep_size()
        return one

    pass


def get_file_provider(picklefile = picklefile):
    if os.path.isfile(picklefile):
        with open(picklefile)as f:
            fileprovider = pickle.load(f)
            #fileprovider.rm_all_finished()
        pass
    else:
        fileprovider = Bufof30()
        #fileprovider.add_files()
        pass

    return fileprovider




if __name__ == '__main__':
    fp = get_file_provider()
    print fp
    '''
    if fp.todo:
        fp.pickle_self()
    for f in fp.todo:
        print f
    pass
    '''
