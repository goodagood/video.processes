# encoding=utf-8

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


    wait("125DiJ4.png",180)
    click("125DiJ4-1.png")
    wait("Rec.png",180)
    click("RecentlyUsed.png")


    type('/')
    type(fullfilename)
    type(Key.ENTER)



    wait("1362291927720.png", 60)
    click(Pattern("HQ.png").targetOffset(38,0))
    
    paste(f['cname'])

    click("goodagood.png")
    click("2B.png")
    click("TTaiiF1f.png")

    paste(f['cname'])
    type(Key.ENTER)
    paste(f['name'])
    type(Key.ENTER)
    
    click("9n.png")
    wait("1362294194835.png", 22)
    
    click("1362292270230.png")
    click("1362292324719.png")

    waitVanish("1362291940020.png", 18000)
    wait("1362292473113.png", 60)
    click("1362292480018.png")
    
    
    
    
###


