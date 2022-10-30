# coding: utf-8

from __future__ import unicode_literals


import re
# import json
# from collections import OrderedDict
# from ..utils import urlencode_postdata

from .common import InfoExtractor


class ColumbiaEDUIE(InfoExtractor):
    _TESTS = [{
        # 'url': 'http://127.0.0.1:8080/catalog/cul:wh70rxwg6m',
        'url': 'https://dlc.library.columbia.edu/catalog/cul:wh70rxwg6m',
        'info_dict': {
            'title': 'Oral history interview with Aleksei Aleksandrovich Gol\'denveizer 1966',
            'id': 'wh70rxwg6m',
        },
        'playlist_mincount': 2,
    }]
    # }, {

    # _VALID_URL = r'http://127\.0\.0\.1\:8080/catalog/cul:(?P<id>[\w\d]+)'
    _VALID_URL = r'https://dlc\.library\.columbia\.edu/catalog/cul:(?P<id>[\w\d]+)'
    _TITLE_PATTERN = r'<h3 id="child-viewer-title">(?P<title>[^<]*)<'
    _DATA_PATTERN = r'data-download-content-url="(?P<url>[^"]*)"'

    def _real_extract(self, url):
        page_id = self._match_id(url)

        web_page = self._download_webpage(url, page_id)

        data = re.findall(self._DATA_PATTERN, web_page)

        title = self._html_search_regex(
            self._TITLE_PATTERN, web_page, 'title', flags=re.UNICODE)
        # raise Exception("Stop")

        entries = self.__entries(data, title)
        return self.playlist_result(entries, page_id, title)

    def __entries(self, data, title):
        _PLAY_ID = r'https://dlc\.library\.columbia\.edu/catalog/cul:(?P<id>[\w\d]+)/'
        for url in data:
            id = re.search(_PLAY_ID, url).groups()[0]
            entry_url = url
            full_title = "%s - %s" % (id, title)
            yield self.url_result(entry_url, video_id=id, video_title=full_title)


# class AnimevostEntryIE(InfoExtractor):
#     _VALID_URL = r'http://play.aniland.org/(.+)'
#     _PLAYER_URL_PATTERN = r'http://play.aniland.org/%s'
#     _FLASHVARS_PATTERN = r'download="invoice".*"(http:[^"]+)"'

#     def _real_extract(self, url):
#         eid = url.split('/')[-1]

#         player_url = self._PLAYER_URL_PATTERN % eid
#         player_page = self._download_webpage(player_url, eid)

#         lnk = re.compile(self._FLASHVARS_PATTERN)
#         video_url = lnk.findall(player_page)[-1]

#         return {
#             'id': eid,
#             'url': video_url,
#             'ext': 'mp4',
#             'title': '',
#         }
