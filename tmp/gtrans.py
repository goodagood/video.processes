# encoding: utf-8
import urllib
import demjson

API_KEY = "AIzaSyD4d84eRXnsAj4I7zxIuwYBEGHKD5zal6w"
TRANSLATE_URL = "https://www.googleapis.com/language/translate/v2?key=" + API_KEY  # &q=hello%20world&source=en&target=de
DETECT_URL = "https://www.googleapis.com/language/translate/v2/detect?key=" + API_KEY  # &q=google+translate+is+fast


def unicode_urlencode(params):
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])


def make_request(url):
    return urllib.urlopen(url).read()


def quick_translate(text, target, source):
    try:
        return translate(text, target, source)["data"]["translations"][0]["translatedText"].replace('&#39;', "'")
    except:
        return ""


def translate(text, target, source):
    query_params = {"q": text, "source": source, "target": target}
    url = TRANSLATE_URL + "&" + unicode_urlencode(query_params)
    try:
        return demjson.decode(make_request(url))
    except:
        return {}


def quick_detect(text):
    try:
        return detect(text)["data"]["detections"][0][0]["language"]
    except:
        return ""


def detect(text):
    query_params = {"q": text}
    url = DETECT_URL + "&" + unicode_urlencode(query_params)
    try:
        return demjson.decode(make_request(url))
    except:
        return {}

if __name__ == '__main__':
    mstr = u"同じ部屋が1人用、2人用と出ていたが、2人用を1人で使用した。値段は60ユーロも違った。部屋のオファーの仕方がよくないのはないでしょうか。設定の仕方が問題がある。"
    mstr = u"I am testing google translation api, it cost, but what's the result?"
    print quick_translate(mstr, "zh-CN", 'en')

    #lang = quick_detect(mstr)
    #print lang
    #print quick_translate(mstr, "en", lang)

