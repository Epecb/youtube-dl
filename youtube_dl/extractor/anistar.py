# coding: utf-8

from __future__ import unicode_literals


import re
import urllib
# from ..utils import urlencode_postdata

from .common import InfoExtractor


class AnistarIE(InfoExtractor):
    _TESTS = [{
        'url': 'https://v2.astar.bz/9012-dreyfuyuschiy-dom-ame-wo-tsugeru-hyouryuu-danchi.html',
        'info_dict': {
            'id': '9012',
        },
        'playlist_mincount': 1,
    }, {
        'url': 'https://v2.astar.bz/8933-limonnye-devochki-shoujo-ramune.html',
        'info_dict': {
            'id': '8933',
        },
        'playlist_mincount': 4,
    }, {
        'url': 'https://v2.astar.bz/8821-ariya-blagoslovenie-aria-the-benedizione.html',
        'info_dict': {
            'id': '8821',
        },
        'playlist_mincount': 1,
    }]

    _VALID_URL = r'https?://(?:www\.)?v2\.astar\.bz/(?P<id>[^-]+)'

    # _TITLE_PATTERN = r'<meta property="og:title" content="([-\s\d\w/:«»#;.,!?&()]+)\['
    _DATA_PATTERN = r'playlst=\[(.*?)\];'

    _SERIES = r'\{.+?\}'
    _TITLE = r'title:(.*)'
    _FILE = r'file:(.*)'
    _HASH = r'.*video/(.*)/360.*'

    def _real_extract(self, url):

        api_url = 'https://v2.astar.bz/test/player2/videoas.php?id={id}'
        # api_url = 'http://localhost:12345/test/player2/videoas.php%3fid%3d{id}'
        m3u8_template = 'https://sf2.an-media.org/video/{hash}/720.mp4/index.m3u8'

        anime_id = self._match_id(url)

        anime_page = self._download_webpage(api_url.format(id=anime_id), anime_id)
        tmp = re.compile(self._DATA_PATTERN, re.DOTALL)
        series_pat = re.compile(self._SERIES, re.DOTALL)
        a_page = tmp.search(anime_page).group(1)
        a_page = re.sub('\t', '', a_page)
        # print(a_page)
        series = series_pat.findall(a_page)
        pl = []
        for i in series:
            series_name = re.sub(
                r'[,"]', '', re.findall(self._TITLE, i)[0]
            )
            m3u8_url = m3u8_template.format(hash=re.search(self._HASH,
                                            urllib.parse.unquote(
                                                re.sub(
                                                    r'[,"]',
                                                    '',
                                                    re.findall(
                                                        self._FILE,
                                                        i)[0]
                                                )
                                            )
            )[1]
            )
            pl.append([series_name, m3u8_url])

        # for i in pl:
        #     print(i[0])
        #     print(i[1])
        # raise Exception("Stop")
        anime_title = url

        entries = self.__entries(pl, anime_title)
        return self.playlist_result(entries, anime_id)

    def __entries(self, data, anime_title):
        for i in data:
            yield self.url_result(i[1], '', anime_title, i[0])
