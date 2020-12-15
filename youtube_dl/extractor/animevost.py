# coding: utf-8

from __future__ import unicode_literals


import re
import json
from collections import OrderedDict

from .common import InfoExtractor


class AnimevostIE(InfoExtractor):
    _TESTS = [{
        'url': 'https://animevost.org/tip/tv/1864-renai-boukun.html',
        'info_dict': {
            'title': 'Любовь тирана / Renai Boukun',
            'id': '1864',
        },
        'playlist_mincount': 10,
    }, {

        'url': 'https://animevost.org/tip/tv-speshl/1854-ryuu-no-haisha.html',
        'info_dict': {
            'title': 'Драконий дантист / Ryuu no Haisha',
            'id': '1854',
        },
        'playlist_mincount': 2,
    }, {

        'url': 'https://animevost.org/tip/ova/1741-mahou-tsukai-no-yome-hoshi-matsu-hito.html',
        'info_dict': {
            'title': 'Невеста чародея ОВА / Mahou Tsukai no Yome: Hoshi Matsu Hito',
            'id': '1741',
        },
        'playlist_mincount': 2,
    }, {
        'url': 'https://animevost.org/tip/ona/1797-huyao-xiao-hongniang.html',
        'info_dict': {
            'title': 'Сводники духов: Лисьи свахи / Huyao Xiao Hongniang',
            'id': '1797',
        },
        'playlist_mincount': 57,
    }, {

        'url': 'https://animevost.org/tip/ona/page,1,8,1943-castlevania.html',
        'info_dict': {
            'title': 'Касльвания / Castlevania',
            'id': 'page,1,8,1943',
        },
        'playlist_mincount': 4,
    }]

    _VALID_URL = r'https://animevost\.org/tip/[-\w\d]+/([,\w\d]+)-[-\w\d]+\.html'
    _TITLE_PATTERN = r'<meta property="og:title" content="([-\s\d\w/:«»#;.,!?&()]+)\['
    _DATA_PATTERN = r'var data = \{([-()\d\w\s,":]+)\};'

    def _real_extract(self, url):
        anime_id = self._search_regex(
            self._VALID_URL, url, 'anime id', flags=re.UNICODE)

        anime_page = self._download_webpage(url, anime_id)
        anime_title = self._html_search_regex(
            self._TITLE_PATTERN, anime_page, 'anime title', flags=re.UNICODE)

        data_str = self._html_search_regex(
            self._DATA_PATTERN, anime_page, 'anime series', flags=re.UNICODE)
        if data_str[-1] == ',':
            data_str = data_str[:-1]
        data = json.loads("{%s}" % data_str, object_pairs_hook=OrderedDict)

        entries = self.__entries(data, anime_title)
        return self.playlist_result(entries, anime_id, anime_title)

    def __entries(self, data, anime_title):
        for ename, eid in data.items():
            entry_url = 'http://play.aniland.org/%s' % eid
            full_title = '%s - %s' % (anime_title, ename)
            yield self.url_result(entry_url, 'AnimevostEntry', eid, full_title)


class AnimevostEntryIE(InfoExtractor):
    _VALID_URL = r'http://play.aniland.org/(.+)'
    _PLAYER_URL_PATTERN = r'http://play.aniland.org/%s'
    _FLASHVARS_PATTERN = r'"file":".*(https?:[^ ]+)'

    def _real_extract(self, url):
        eid = url.split('/')[-1]

        player_url = self._PLAYER_URL_PATTERN % eid
        player_page = self._download_webpage(player_url, eid)

        lnk = re.compile(self._FLASHVARS_PATTERN)
        video_url = lnk.findall(player_page)[-1]

        return {
            'id': eid,
            'url': video_url,
            'ext': 'mp4',
            'title': '',
        }
