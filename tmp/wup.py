# encoding=utf-8
import os
import os.path
import re
import time
import ConfigParser
# to remove directory and files in it, dangerous operation:
import shutil

# settings:
base_folder            = 'd:\\myvid\\'

config_filename       = os.path.join(base_folder, 'robot.cfg')

config = ConfigParser.ConfigParser()
config.read(config_filename)

log_filename           = config.get('basics', 'log_filename')
log_filename           = os.path.join(base_folder, log_filename)

chinese_title_filename = config.get('basics', 'chinese_title_filename')
#chinese_title_filename = os.path.join(base_folder, chinese_title_filename)

todo_filename          = config.get('basics', 'todo_filename')
#todo_filename          = os.path.join(base_folder, todo_filename)

def set_working_log(section='working_log', name='wlogging', content=''):
    config.set(section, name, content)

def write_working_log():
    with open(config_filename, 'wb') as conffile:
        config.write(conffile)
    pass

'''
log_filename           = os.path.join(base_folder, 'sikulilog')
chinese_title_filename = 'cname'
todo_filename          = 'cname.todo'
'''

# make a unique and readable logfile name
def get_asctime():
    asct = time.asctime()
    #ascta = asct.replace(' ', '_')
    return asct

## Stop using 'cname_file', this file contains file name and Chinese title
#  pairs.  It would be easy to put this file inside the same folder of the
#  video files.  
# -Make it a hard specification to name the file as 'cname', and put inside
#  the folder of video files.
# -It would be more convinient to write a working file 'cname.todo', it
#  will contain the _todo_ things. 
# -Remove the video file after uploading, this will save a lot trivial manual
#  jobs, and free disk space for more file uploading.
##


def writelog(msg=''):
    with open(log_filename, 'a+') as logfile:
        logfile.write ( "\n")
        logfile.write ( get_asctime() )
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
    pass



def appendlog(fullfilename, msg=''):
    with open(fullfilename, 'a+') as logfile:
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
    pass


# deperacated, 0322
## get video file names and chinese names of the video from file 'cname?'
# -The format of the file 'cname' is: 
#      first line of file name, 
#      followed by a line of Chinese title,
#      and empty line(s).
##
def chop_to_filename_ctitle_pieces(cname_file):
    with open(cname_file) as afile:
        file2str = afile.read()
        pass
    if not file2str:
        return []


    # One line file name, followed by one line Chinese video title, followed
    # by empty line(s):
    todos = re.split(r'\n[\n\s]*\n', file2str)

    # chop the file text to piece of one file name plus chinese name of the
    # video
    chops = []

    for p in todos:
        lines = p.split('\n')
        # filter out empty lines:
        my_lines = filter( lambda x: x.strip(), lines)

        # 1 line: name of the file
        # 2 line: chinese name of it
        # If it's not two lines pair, we drop it:
        if len(my_lines) == 2:
            one = dict(name=my_lines[0], cname=my_lines[1])
            chops.append(one)
        pass

    return chops


def upload_one_file(fullfilename, filename, cname, long_cname=''):
    if long_cname == '':
        long_cname = cname


    return 'finished'
    

def write_todo_file(content_start, dir_start, contents):
    base       = filedirs[dir_start]['basedir']
    todo_file = base + todo_filename

    with open(todo_file, 'w+') as todo:
        for c in contents[content_start+1: ]:
            todo.write( "%s\n%s\n\n"%(c['name'], c['cname']))
    pass


def get_new_folder(base='/home/za/myvid'):
    dirs_in_base_folder = [ os.path.join(base, name) for name in
            os.listdir(base) if os.path.isdir(
                os.path.join(base, name))]
    dirs_in_base_folder.sort()
    if len(dirs_in_base_folder) > 0:
        return dirs_in_base_folder[0]
    return None


def get_folder_from_working_log():
    folder = None
    try:
        folder = config.get('working_log', 'folder')
    except:
        folder = None
        pass

    if folder == 'unknown':
        return None

    return folder


def get_folder(base_folder):
    folder =  get_folder_from_working_log()
    if not folder or not os.path.isdir(folder):
        folder = get_new_folder(base_folder)

    config.set('working_log', 'folder', folder)
    write_working_log()
    return folder


def stop_signal_comes():
    stop = config.getint('basics', 'stop_at')
    if stop == 1:
        return True

    if stop == 0:
        return False
    else:
        stop = stop -1
        config.set('basics', 'stop_at', stop)
        write_working_log()

    return False


## get video file names and chinese names of the video from file 'cname'
# -The format of the file 'cname' is: 
#      first line of file name, 
#      followed by a line of Chinese title,
#      and empty line(s).
##
def read_chinese_title(cname):
    """read chinese title from 'cname' file.

    cname : the file contains chinese title for each video file.
    """
    with open(cname) as afile:
        file2str = afile.read()
        pass
    if not file2str:
        return []


    # One line file name, followed by one line Chinese video title, followed
    # by empty line(s):
    todos = re.split(r'\n[\n\s]*\n', file2str)

    # chop the file text to piece of 
    # one file name plus chinese name of the video
    filename_ctitle_dict = {}

    for p in todos:
        lines = p.split('\n')
        # filter out empty lines:
        my_lines = filter( lambda x: x.strip(), lines)

        # 1 line: name of the file
        # 2 line: chinese name of it
        # If it's not two lines pair, we drop it:
        if len(my_lines) == 2:
            #one = dict(name=my_lines[0], cname=my_lines[1])
            #one = {my_lines[0] : my_lines[1]}
            filename_ctitle_dict[my_lines[0]] = my_lines[1]
        pass

    return filename_ctitle_dict


def prepare_files(folder):
    files = os.listdir(folder)

    title_filename = os.path.join(folder, chinese_title_filename)
    kv_name_title = read_chinese_title(title_filename)

    pieces = []
    for filename in files:
        if not kv_name_title.has_key(filename):
            continue
        
        chinese_title = kv_name_title[filename]

        longtitle = chinese_title
        ctitle    = chinese_title
        if len(chinese_title) > 60:
            ctitle    = chinese_title[:58]
        if kv_name_title.has_key(filename):
            one = dict(filename      = filename,
                       chinese_title = ctitle,
                       longtitle     = longtitle,
                       fullfilename  = os.path.join(folder, filename))
            pieces.append(one)

    return pieces
    pass


# dirty and quick on windows server 2008
def dirty_quick_files(folder):
    files = os.listdir(folder)

    pieces = []
    for filename in files:
        if not filename.endswith('webm'):
            continue
        
        chinese_title = filename

        longtitle = chinese_title
        ctitle    = chinese_title
        if len(chinese_title) > 60:
            ctitle    = chinese_title[:58]


        one = dict(filename      = filename,
                   chinese_title = ctitle,
                   longtitle     = longtitle,
                   fullfilename  = os.path.join(folder, filename))
        pieces.append(one)

    return pieces
    pass

def mocking(message='', duration=1, raise_exception=False):
    popup( "I am mocking...%s"%message )
    if raise_exception:
        raise Exception(message)
    time.sleep(duration)


def transfer_to_error_folder(fullfilename, filename, long_cname):
    errorv_folder = config.get('basics', 'errorv_folder')
    errorv_log = config.get('basics', 'errorv_log')

    newfilename = os.path.join(errorv_folder, filename)
    os.rename(fullfilename, newfilename)

    msg = "%s\n%s"%(filename, long_cname)
    appendlog(errorv_log, msg)
    pass


def do_one_file(filename, fullfilename, cname, long_cname):
    try:
        #mocking("uploading file and remove it in success, %s %s"%(fullfilename, long_cname))

        state = ''
        while state != 'finished':
            state = upload_one_file(fullfilename, filename, cname,long_cname)
        os.remove(fullfilename)

        #write_todo_file(j, startnumber, filename_videotitle_pairs)
    except:
        transfer_to_error_folder(fullfilename, filename, long_cname)
        # move the file to errorv, os.rename()

        logmsg = "exception in uploading file: %s\nwith long_cname: %s \n"%(fullfilename, long_cname)
        writelog( logmsg)
        restart_firefox()
        pass

    logmsg = "fullfilename: \n" + fullfilename + "\ncname: " + cname
    writelog( logmsg)

    pass


def do_one_folder(folder):
    # prepare file informations
    # remove empty folder
    # loop over one file uploading

    # no need to record file name, finish one, remove one, 
    # in case error happen, mv the file to 'errorv' folder, and log it.

    file_infos = prepare_files(folder)
    for fi in file_infos:
        filename = fi['filename']
        fullfilename = fi['fullfilename']
        cname = fi['chinese_title']
        long_cname = fi['longtitle']

        do_one_file(filename, fullfilename, cname, long_cname)
        pass

    ## testing, check file_infos:
    '''
    with open('/tmp/ttesta', 'wb') as testfile:
        for fi in file_infos:
            testfile.write( fi['filename'] + "\n")
            testfile.write( fi['chinese_title'] + "\n")

            print fi['filename']
            print fi['fullfilename']
            print fi['chinese_title']
            print fi['longtitle']
    '''
    pass


def loop_over_folders():
    """This automatically loop over all folders in 'base_folder'
    """
    folder = get_folder(base_folder)
    while folder:
        # do one folder, and stop at stop signal:
        #popup( "do one folder: %s"%folder)
        do_one_folder(folder)
        shutil.rmtree(folder)

        folder = get_folder(base_folder)
        pass
    pass



##########################
### tests:


def test_config():
    popup( "log_filename: %s"%log_filename)
    popup( "todo_filename: %s"%todo_filename)
    popup( "chinese_title_filename: %s"%chinese_title_filename)

    #config.set('working_log', 'filename', 'thisisthefilename')
    #config.set('working_log', 'timelog', get_asctime())
    #write_working_log()
    pass

## comment out after testing:
test_config()
#print get_folder()
#print prepare_files('/home/za/myvid/aa')
#do_one_folder('/home/za/myvid/aa')
#loop_over_folders()

### do the job:
'''
wait(0)
'''

#loop_over_folders()


