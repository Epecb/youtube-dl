# coding: utf-8

from __future__ import unicode_literals


import re
import json
from collections import OrderedDict
from ..utils import urlencode_postdata

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
        # api url
        # https://api.animevost.org/v1/playlist --data 'id=1943'

        api_url = 'https://api.animevost.org/v1/playlist'
        data_req = 'id=%s'

        anime_id = self._search_regex(
            self._VALID_URL, url, 'anime id', flags=re.UNICODE)

        request_data = urlencode_postdata({
            'id': anime_id,
        })
        anime_page = self._download_webpage(api_url, anime_id, data=request_data)
        data = json.loads(anime_page)

        rgx = re.compile(r'^[0-9]+')
        data = sorted(data, key=lambda data: int(
            rgx.match(data.get('name')).group()))

        anime_title = url

        entries = self.__entries(data, anime_title)
        return self.playlist_result(entries, anime_id, anime_title)

    def __entries(self, data, anime_title):
        for i in data:
            yield self.url_result(i.get('hd'), '', anime_title, i.get('name'))


class AnimevostEntryIE(InfoExtractor):
    _VALID_URL = r'http://play.aniland.org/(.+)'
    _PLAYER_URL_PATTERN = r'http://play.aniland.org/%s'
    _FLASHVARS_PATTERN = r'download="invoice".*"(http:[^"]+)"'

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
