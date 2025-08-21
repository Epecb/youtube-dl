# coding: utf-8

from __future__ import unicode_literals


import re
import json
# from collections import OrderedDict
# from ..utils import urlencode_postdata

from .common import InfoExtractor


class ColumbiaeduIE(InfoExtractor):
    _TESTS = [{
        # 'url': 'http://127.0.0.1:8080/catalog/cul:2280gb5pd5',
        'url': 'https://dlc.library.columbia.edu/catalog/cul:wh70rxwg6m',
        'info_dict': {
            'title': 'Oral history interview with Iurii Petrovich Denike (George Denicke) 1964',
            'id': '2280gb5pd5',
        },
        'playlist_mincount': 3,
    }]

    # _VALID_URL = r'http://127\.0\.0\.1\:8080/catalog/cul:(?P<id>[\w\d]+)'
    _VALID_URL = r'https://dlc\.library\.columbia\.edu/catalog/cul:(?P<id>[\w\d]+)$'
    _TITLE_PATTERN = r'<meta property="og:title" content="(?P<title>[^>]*)" />'
    _DATA_PATTERN = r'[\S]+[\s]data-download-content-url="(?P<url>[^"]*)"'

    def _real_extract(self, url):
        page_id = self._match_id(url)

        web_page = self._download_webpage(url, page_id)

        # data = re.findall(self._DATA_PATTERN, web_page)

        title = self._html_search_regex(
            self._TITLE_PATTERN, web_page, 'title', flags=re.UNICODE)

        rgx = r'data-manifest="([^"]*)"'
        manifest = re.search(rgx, web_page).group(1)
        # print(manifest)

        req = self._download_webpage(manifest, page_id)
        jdata = json.loads(req)

        data = []
        for item in jdata['items']:
            # title
            # print(json.dumps(item['label']['en'][0], indent=4))
            jtitle = item['label']['en'][0]
            # url
            # print(json.dumps(item['items'][0]['items'][0]['body']['id'], indent=4))
            jurl = item['items'][0]['items'][0]['body']['id']
            data.append([jtitle, jurl])

        entries = self.__entries(data, title)
        return self.playlist_result(entries, page_id, title)

    def __entries(self, data, title):
        # _PLAY_ID = r'https://dlc\.library\.columbia\.edu/catalog/cul:(?P<id>[\w\d]+)/'
        for url in data:
            # v_id = re.search(_PLAY_ID, url).groups()[0]
            v_id = url[0]
            entry_url = url[1]
            full_title = "%s - %s" % (v_id, title)
            yield self.url_result(url=entry_url, video_id=v_id, video_title=full_title)
