# encoding=utf-8
import os.path
import re
import time

# make a unique and readable logfile name
def get_asctime():
    asct = time.asctime()
    ascta = asct.replace(' ', '_')
    return ascta

logfile = open('/tmp/sikulilog', 'a+')

filedir = [
        {'cname_file':'/tmp/cnamea', 'basedir':'/tmp/va/'},
        {'cname_file':'/tmp/cnameb', 'basedir':'/tmp/vb/'},
        {'cname_file':'/tmp/cnamec', 'basedir':'/tmp/vc/'},
        {'cname_file':'/tmp/cnamed', 'basedir':'/tmp/vd/'},
        {'cname_file':'/tmp/cnamee', 'basedir':'/tmp/ve/'},
        {'cname_file':'/tmp/cnamef', 'basedir':'/tmp/vf/'},
        {'cname_file':'/tmp/cnameg', 'basedir':'/tmp/vg/'},
        {'cname_file':'/tmp/cnameh', 'basedir':'/tmp/vh/'} ]

def writelog(logfile=None, msg=''):
    if logfile:
        logfile.write ( "\n")
        logfile.write ( msg)
        logfile.write("\n")
        #logfile.flush()
    pass

## get video file names and chinese names of the video from file 'cname?'
def get_vfile_names(cname_file):
    afile = open(cname_file, 'r')
    file2str = afile.read()
    afile.close()

    todos = re.split(r'\n[\n\s]*\n', file2str)

    # chop the file text to piece of one file name plus chinese name of the
    # video
    chops = []
    for p in todos:
        lines = p.split('\n')
        my_lines = []
        for l in lines:
            striped = l.strip()
            if striped:
                my_lines.append(striped)
                pass
            pass

        # 1 line: name of the file
        # 2 line: chinese name of it
        if len(my_lines) == 2:
            one = dict(name=my_lines[0], cname=my_lines[1])
            chops.append(one)
        pass

    return chops


def upload_one_file(fullfilename, filename, cname):


    wait("125DiJ4.png",180)
    click("125DiJ4-1.png")
    wait("Rec.png",180)
    click("RecentlyUsed.png")


    type('/')
    type(fullfilename)
    type(Key.ENTER)



    wait("1362291927720.png", 60)
    click(Pattern("HQ.png").targetOffset(38,0))
    
    paste(cname)

    click("goodagood.png")
    click("2B.png")
    click("TTaiiF1f.png")

    paste(cname)
    type(Key.ENTER)
    paste(filename)
    type(Key.ENTER)
    
    click("9n.png")
    wait("1362294194835.png", 22)
    
    click("1362292270230.png")
    click("1362292324719.png")

    waitVanish("1362291940020.png", 18000)
    wait("1362292473113.png", 60)
    click("1362292480018.png")
    
    

    #---------
    #click("here.png")
    #type(Key.ENTER)
    #type('fullfilename : ')
    #paste(fullfilename)
    #type(Key.ENTER)
    #type('cname : ')
    #paste(cname)
    #type(Key.ENTER)

    pass


def loop_over_dirs():
    i = 0
    number_of_cname_file = len(filedir)

    while True:

        cname_file = filedir[i]['cname_file']
        base       = filedir[i]['basedir']
        if not os.path.exists( cname_file ):
            writelog ( logfile, "file-not-exist: " + cname_file)
            logfile.close()
            return

        vfilename_cnames = get_vfile_names(cname_file)

        for f in vfilename_cnames:
            fullfilename = base + f['name']
            cname = f['cname']
            filename = f['name']

            upload_one_file(fullfilename, filename, cname)

            logmsg = "fullfilename: \n" + fullfilename + "\ncname: " + cname
            writelog(logfile, logmsg)

        i = i + 1
        if i == number_of_cname_file:
            i = 0
        
### do the job:
loop_over_dirs()
logfile.close()
