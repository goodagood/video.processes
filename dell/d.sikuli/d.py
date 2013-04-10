# encoding=utf-8
#import jya
#from jya import get_file_names





import re



def get_file_names():
    afile = open("/home/za/myvid/a/cname", 'r')
    file2str = afile.read()
    afile.close()

    todos = re.split(r'\n[\n\s]*\n', file2str)

    chops = []
    test_a = []
    for p in todos:
        lines = p.split('\n')
        my_lines = []
        for l in lines:
            striped = l.strip()
            if striped:
                my_lines.append(striped)
                pass
            pass

        test_a.append(my_lines)
        # 1 line: name of the file
        # 2 line: chinese name of it
        if len(my_lines) == 2:
            one = dict(name=my_lines[0], cname=my_lines[1])
            chops.append(one)
        pass

    return chops

####################
base = '/home/za/myvid/a/'

#wait(3)
files = get_file_names()

for f in files:
    fullfilename = base + f['name']
    
    wait("125DiJ4.png", 120)
    click("wiNfihi.png",180)
    wait("RecentlyUsed.png",180)
    click("1362289867994.png")
    

    

    type('/')
    type(fullfilename)
    type(Key.ENTER)
    
    wait("1362229772148.png", 60)

    click(Pattern("EEE.png").targetOffset(35,0))
    
    
    paste(f['cname'])
    
    click("goodagood.png")    
    
    click("a5fBJ.png")
    click("iREvHma9HiRK.png")
    paste(f['cname'])
    type(Key.ENTER)    
    type(fullfilename)
    type(Key.ENTER)
    
    click("i3MQ51.png")

    click("FE1.png")
#    click("1iNi.png")

    


    click("1362229992740.png")
    waitVanish("1362231569796.png", 18000)
    
    
    wait("1362230139530.png", 60)
    click("1362230139530.png")
    
    
