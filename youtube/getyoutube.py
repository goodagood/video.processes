import time

import gdata.youtube
import gdata.youtube.service

## results write to /tmp/fha
def getyoutube(kwords="african crowned crane", number=100, seconds=600):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = kwords
    query.max_results = 50
    query.racy = "exclude"
    #query.format = 5
    query.orderby = "relevance"

    cycles = number * 1.0 / 50.0
    if cycles > 1:
        cycles = int(cycles + 1.0)
    else:
        cycles = 1

    results = []
    for i in range(cycles):
        query.start_index = 1 + i * 50

        feed = client.YouTubeQuery(query)

        for entry in feed.entry:
            title = entry.title.text
            href = entry.GetHtmlLink().href.split('&')[0]
            dur = int( entry.media.duration.seconds )
            if dur < seconds:
                one = dict(title=title, href=href)
                results.append(one)
        time.sleep(10)

    fh = open('/tmp/fha', 'w+b')
    for one in results:
        fh.write(one['title'])
        fh.write("\n")
        fh.write(one['href'])
        fh.write("\n")
        fh.write("\n")
        
    return results


## results write to /tmp/ylessa
def getyoutubeless(kwords="sun bathing mizushima beach", number=10):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = kwords
    query.max_results = number
    query.racy = "exclude"
    #query.format = 5
    query.orderby = "relevance"

    '''
    cycles = number * 1.0 / 50.0
    if cycles > 1:
        cycles = int(cycles + 1.0)
    else:
        cycles = 1
    '''

    results = []

    query.start_index = 1

    feed = client.YouTubeQuery(query)

    for entry in feed.entry:
        title = entry.title.text
        href = entry.GetHtmlLink().href.split('&')[0]
        one = dict(title=title, href=href)
        results.append(one)

    with open('/tmp/ylessa', 'w+b') as fh:
        for one in results:
            fh.write(one['title'])
            fh.write("\n")
            fh.write(one['href'])
            fh.write("\n")
            fh.write("\n")
        
    return feed, results


