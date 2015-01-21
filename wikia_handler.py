import urllib2
import requests
import re
from bs4 import BeautifulSoup, NavigableString
from urllib import urlencode


def get_wikia_lyrics(artist, song):
    params = urlencode([('artist', artist), ('song', song), ('fmt', 'json')])
    data = urllib2.urlopen("http://lyrics.wikia.com/api.php?%s" % params).read()
    match = re.search("'url':'([^']+)'", data)
    if not match:
        return 'Api not found'
    response = requests.get(match.group(1))

    div = re.search(r"<div class='lyricbox'>", response.text)
    if not div:
        return 'text not found on page'

    soup = BeautifulSoup(response.text)
    lyricbox = soup.find('div', "lyricbox")
    if not lyricbox:
        return 'text content not found'

    lyrics = ''
    for c in lyricbox.contents:
        text = unicode(c).strip()
        if type(c) == NavigableString:
            lyrics += text.strip()
        elif text.startswith('<br'):
            lyrics += '\n'
    return lyrics.strip()