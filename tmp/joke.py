
# encoding=utf-8
def jokelist(fn = '/tmp/webs'):
    filesize = os.path.getsize(fn)
    chunk = 12800

    raw_parts = []

    start = random.randint(0, filesize-chunk)
    with open(fn, 'rb') as jokefile:
        jokefile.seek(start)
        random_char = jokefile.read(chunk)
        raw_parts = random_char.split('==========') # =*10 is delimit
        # get rid of the 1st and the last, it might not be full joke:
        raw_parts = raw_parts[1:-1]
        pass

    return raw_parts

def rm_poo(jokelist):
    """Remove bad jokes.

    jokelist is a list of joke.
    """
    print type(jokelist)
    print len(jokelist)
    goodjokes = []
    for i in range(len(jokelist)):
        joke = jokelist[i]
        print i
        if joke.count("大便"):
            show( joke)
            if yesYES():
                continue
        if joke.count("群尸"):
            show( joke)
            if yesYES():
                continue
        if joke.count("呕吐"):
            show( joke)
            if yesYES():
                continue
            pass
        goodjokes.append(joke)
        pass
    return goodjokes



def yesYES():
    a = raw_input("y/Y for remove, others for no: ")
    a = a.strip()
    if a.find('y') or a.find('Y'):
        return True
    return False

def shrink(fn='/tmp/webs'):
    with open(fn, 'rb') as jokefile:
        random_char = jokefile.read()
        raw_parts = random_char.split('==========') # =*10 is delimit
        # get rid of the 1st and the last, it might not be full joke:
        pset = set(raw_parts)
        pass

    return list(pset)

def show(string):
    if len(string) > 1024:
        print string[:256]
        print "\n......\n"
        print string[-256:]
    else:
        print string

