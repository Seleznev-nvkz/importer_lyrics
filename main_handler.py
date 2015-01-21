import sys
import codecs
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT
from fnmatch import filter as type_filter
from wikia_handler import get_wikia_lyrics

if sys.platform == 'win32':
    QUERY_FILE = 'C:\\temp\\music_query.txt'
else:
    QUERY_FILE = '/tmp/music_query.txt'

exists_query = lambda x=QUERY_FILE: x if os.path.isfile(x) else None


# class CallApi:
#
#     token = None
#     uid = None
#
#     def __init__(self, email='drdiablo@bk.ru', password='Manson123', app_id='4570062', scope='audio'):
#         self.token, self.uid = vk_auth.auth(email=email,
#                                             password=password,
#                                             client_id=app_id,
#                                             scope=scope)
#
#     def get_this_shit(self, method, params):
#         params.append(("access_token", self.token))
#         url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
#         return json.loads(urllib2.urlopen(url).read()).get('response')
#
#     def _search(self, params):
#         params.append(('count', 10))
#         params.append(('lyrics', 1))
#         return self.get_this_shit('audio.search', params)
#
#     def _lyrics(self, params):
#         response = self.get_this_shit('audio.getLyrics', params)
#         return response.get('text', None)
#
#     def lyrics_handler(self, params):
#         search_response = self._search(params)
#         if search_response[0]:
#             for item in search_response[1:]:
#                 item_lyrics = self._lyrics([('lyrics_id', item.get('lyrics_id'))]) or ''
#                 if len(item_lyrics) > 75:
#                     return {
#                         'lyrics': item_lyrics,
#                         'title': item.get('title'),
#                         'artist': item.get('artist'),
#                         'url': item.get('url')
#                     }
#         return {}


def get_track(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.replace('\n', '')


def readable_title(file_path):
    id3 = EasyID3(file_path)
    artist, title = id3.get('artist'), id3.get('title')
    if artist and title:
        return artist[0], title[0]
    return ' ', file_path.split('/')[-1].split('.')[0]


def text_into_mp3(file_path, text):
    id3 = ID3(file_path)
    if len(id3.getall(u"USLT")):
        id3.delall(u"USLT")
        id3.save()
    id3[u"USLT"] = USLT(encoding=3, lang=u'eng', desc=text, text=text)
    id3.save()
    return 'success'


def create_query(path):
    """
    :param path: string with path of music directory
    :return: string - tmp file with query
             int - count of music files on query file
    """
    count = 0
    query_file = codecs.open(QUERY_FILE, 'w', 'utf-8', errors='ignore')
    for root, dir_names, file_names in os.walk(path):
        for filename in type_filter(file_names, '*.mp3'):
            query_file.write('%s\n' % os.path.join(root, filename).decode('utf-8'))
            count += 1
    query_file.close()
    return QUERY_FILE, count


def file_handler(current_file, rewrite=True):
    """ read -> get -> import """
    if not rewrite:
        if len(ID3(current_file).getall(u"USLT")):
            return 'exists'
    artist, song = readable_title(current_file)
    lyrics = get_wikia_lyrics(artist, song)
    return text_into_mp3(current_file, lyrics)