# encoding=utf-8
import os
import os.path
import re
import time

# settings:
chinese_title_filename = 'cname'
todo_filename = 'cname.todo'
logfile_name = '/home/za/tmp/sikulilog'

# make a unique and readable logfile name
def get_asctime():
    asct = time.asctime()
    ascta = asct.replace(' ', '_')
    return ascta

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
filedirs = [
        {'cname_file':'/home/za/myvid/cnamea', 'basedir':'/home/za/myvid/va/'},
        {'cname_file':'/home/za/myvid/cnameb', 'basedir':'/home/za/myvid/vb/'},
        {'cname_file':'/home/za/myvid/cnamec', 'basedir':'/home/za/myvid/vc/'},
        {'cname_file':'/home/za/myvid/cnamed', 'basedir':'/home/za/myvid/vd/'},
        {'cname_file':'/home/za/myvid/cnamee', 'basedir':'/home/za/myvid/ve/'},
        {'cname_file':'/home/za/myvid/cnamef', 'basedir':'/home/za/myvid/vf/'},
        {'cname_file':'/home/za/myvid/cnameg', 'basedir':'/home/za/myvid/vg/'},
        {'cname_file':'/home/za/myvid/cnameh', 'basedir':'/home/za/myvid/vh/'},
        {'cname_file':'/home/za/myvid/cnamei', 'basedir':'/home/za/myvid/vi/'},
        {'cname_file':'/home/za/myvid/cnamej', 'basedir':'/home/za/myvid/vj/'} ]

def writelog(msg=''):
    with open(logfile_name, 'a+') as logfile:
        logfile.write ( "\n")
        logfile.write ( get_asctime() )
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
    pass


## get video file names and chinese names of the video from file 'cname?'
# -The format of the file 'cname' is: first line of file name, followed by a
#  line of Chinese title, and empty line(s).
##
def chop_to_filename_ctitle_pieces(cname_file):
    '''
    afile = open(cname_file, 'r')
    file2str = afile.read()
    afile.close()
    '''

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
        '''
        my_lines = []
        for l in lines:
            striped = l.strip()
            if striped:
                my_lines.append(striped)
                pass
            pass
            '''

        # 1 line: name of the file
        # 2 line: chinese name of it
        # If it's not two lines pair, we drop it:
        if len(my_lines) == 2:
            one = dict(name=my_lines[0], cname=my_lines[1])
            chops.append(one)
        pass

    return chops


def check_uploading(fullfilename):
    if exists("1362377204647.png"):
        return 'finished'
    
    if exists("EMM2H17BkfFE.png"):
        click(Pattern("cancel_56ioerror.png").targetOffset(8,-6))
        writelog("error: " + fullfilename)
        return "error_io_56"

    if exists("Stopscript_jserror.png"):
        click("Stopscript_jserror.png")
        writelog("error: " + fullfilename)
        return "error_js_stop_script"


    # If upload error:
    if exists("1362414190386.png"):
        writelog("error: " + fullfilename)
        # try small cross:
        click("1362832524146.png")

        #click("1362414218067.png")
        return "error_io_56"

    if exists(Pattern("uploading_flag.png").similar(0.88)):
        return "uploading"

    return 'finished'


def safe_guards(cname):
    # safeguard, the following clicks must be done to pass.
    # If failed to select 'tag', do again:
    if exists("i.png"):
        #click("gcodagcoc.png")
        click("i.png")
        type("goodagood ")
        
    if exists(Pattern("red_tag_warning.png").targetOffset(1,8)):
        click(Pattern("red_tag_warning.png").targetOffset(1,8))
        type("goodagood ")
        
    if exists("iiEiB.png"):
        doubleClick(Pattern("HQ.png").targetOffset(38,0))
        wait(2)
        type(Key.BACKSPACE)
        for i in range(200):
            type(Key.DELETE)    
        paste(cname)        
        #click("gcodagcoc.png")

    # If failed to select 'category', do again:
    if exists("9n.png"):
        click("9n.png")

        #wait("1362294194835.png", 22)
        #click("1362292270230.png")
        #wait("Bi7i.png",22)
        
        wait("ifiHHHi.png",22)
        click("ifiHHHi.png")
        pass

    # 56.com get length limit:
    if exists("iIBFEF60f.png"):
        doubleClick(Pattern("HQ.png").targetOffset(38,0))
        for i in range(200):
            type(Key.DELETE)
            
        paste(cname)
        pass
    # ^ The above is safeguards.
    

def fileselector(fullfilename):
    wait("QgmengpE.png",90)
    

    ## file selector might change:
    if exists("filesystem.png"):
        click("filesystem.png")
        #type('/')
    else:
        #wait("IEza.png", 60)
        click("IEza.png")
        
    #if exists("Location.png"):
    #    click("Location-1.png")


    type(fullfilename)
    type(Key.ENTER)


    pass

def upload_one_file(fullfilename, filename, cname, longname=''):
    if longname == '':
        longname = cname

    wait("125DiJ4.png",240)
    click("to_select_video2upload_DiJ4-1.png")
    #waitVanish("125DiJ4-1.png", 30)  #after click, this should vanish?
    

    fileselector(fullfilename)

    wait("save_128.png", 128)
    
    doubleClick(Pattern("HQ.png").targetOffset(38,0))
    wait(2)
    type(Key.BACKSPACE)
    for i in range(200):
        type(Key.DELETE)    
    paste(cname)

    # sometime, tag of 'goodagood' not appears
    if exists("goodagood.png"):
        click("goodagood.png")
        
    wait(3)
    click("2B.png")
    #click("TTaiiF1f.png")
    click(Pattern("Mi.png").targetOffset(51,0))
    
    wait(3)

    paste(longname)
    type(Key.ENTER)
    paste(filename)
    type(Key.ENTER)
    
    click("9n.png")
    wait("1362294194835.png", 22)
    click("1362292270230.png")
    #wait("travel_catlog.png",22)
    #click("travel_catlog.png")

    #wait("zongyi_catlog.png",22)
    #click("zongyi_catlog.png")
    
    # safe guards:
    safe_guards(cname)

    # save all info:
    click("save_l238.png")

    # When there is a progress bar changing, do let sikuli waiting dynamic images:    
    wait(3)  # can we wait less?
    
    # This works fine in normal, but failed oncy to catch error:
    # waitVanish("E19IJfFP4EJ9.png", 6800)
    
    # try to check more area, BUT failed to found uploading error:    
    #waitVanish("9I9IJfFP1EJI.png", 6800)
    # try to include the more text in the pic. :
    #waitVanish("iI7FPUl9IJf4.png", 6800)

    state = check_uploading(fullfilename)
    while state.startswith("uploading"):
        time.sleep(5)
        state = check_uploading(fullfilename)
    if state != "finished":
        return 'error'


    wait("keepuploadinga.png", 256)
    click("toclick_to_uploading.png")  # failed a few time, not found this
    return 'finished'
    

def write_todo_file(content_start, dir_start, contents):
    base       = filedirs[dir_start]['basedir']
    todo_file = base + todo_filename

    with open(todo_file, 'w+') as todo:
        for c in contents[content_start+1: ]:
            todo.write( "%s\n%s\n\n"%(c['name'], c['cname']))
    pass

def get_filename_title_pairs(number=0):
    #cname_file = filedirs[number]['cname_file']

    ## Note, we need the base dir name ends with '/':
    base       = filedirs[number]['basedir']
    cname_file = base + chinese_title_filename
    todo_file  = base + todo_filename

    if os.path.exists( todo_file ):
        filename_title_pairs = chop_to_filename_ctitle_pieces( todo_file )
        for one in filename_title_pairs:
            one['fullfilename'] = base + one['name']
        return filename_title_pairs
    
    # If arrived here, we are going to use cname_file freshly:
    if not os.path.exists( cname_file ):
        writelog ( "file-not-exist: " + cname_file)
        return []

    filename_title_pairs = chop_to_filename_ctitle_pieces(cname_file)
    for one in filename_title_pairs:
        one['fullfilename'] = base + one['name']
    return filename_title_pairs


def loop_over_dirs(startnumber=0):
    number_of_cname_file = len(filedirs)

    while True:
        filename_videotitle_pairs = get_filename_title_pairs(startnumber)
        ## stop when no more file need to do:
        if not filename_videotitle_pairs:
            return

        number_of_files = len(filename_videotitle_pairs)
        for j in range(number_of_files):
            f = filename_videotitle_pairs[j]

            fullfilename = f['fullfilename']
            cname = f['cname']
            longname = ''
            if len(cname) > 60:
                longname = cname
                cname = cname[:58]
            filename = f['name']

            state = ''
            while state != 'finished':
                state = upload_one_file(fullfilename, filename, cname,
                        longname)

            logmsg = "fullfilename: \n" + fullfilename + "\ncname: " + cname
            writelog( logmsg)

            write_todo_file(j, startnumber, filename_videotitle_pairs)
            os.remove(fullfilename)

        startnumber = startnumber + 1
        if startnumber == number_of_cname_file:
            startnumber = 0
        
### do the job:
wait(0)
# a-0, b-1, c-2, d-3, e-4, f-5, g-6, h-7, i-8, j-9:
loop_over_dirs(9)


##########################
### tests:

def test_loop_over_dirs(startnumber=1):
    """ copy from loop_over_dirs, for testing.
    """
    number_of_cname_file = len(filedirs)

    while True:
        filename_videotitle_pairs = get_filename_title_pairs(startnumber)
        if not filename_videotitle_pairs:
            return

        number_of_files = len(filename_videotitle_pairs)

        for j in range(number_of_files):
            f = filename_videotitle_pairs[j]

            fullfilename = f['fullfilename']
            cname = f['cname']
            if len(cname) > 60:
                cname = cname[:59]
            filename = f['name']

            print "fullfilename: %s \n cname: %s \n filename %s \n\n" %(
                    fullfilename, cname, filename)

            #upload_one_file(fullfilename, filename, cname)
            time.sleep(15)
            #os.remove(fullfilename)

            logmsg = "fullfilename: \n" + fullfilename + "\ncname: " + cname
            writelog( logmsg)

            write_todo_file(j, startnumber, filename_videotitle_pairs)

        startnumber = startnumber + 1
        if startnumber == number_of_cname_file:
            startnumber = 0
        
    pass

## comment out after testing:
#test_loop_over_dirs(0)
